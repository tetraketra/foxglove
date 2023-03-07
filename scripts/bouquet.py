# Imports & Declarations # ---------------------------------------------------------
import numpy as np
import fileinput
from more_itertools import collapse, split_at
from dataclasses import dataclass, field, asdict
from operator import itemgetter

RESERVED_TYPE_SYMBOLS = [*"AaBbLl"]
RESERVED_EXPANSION_SYMBOLS = ["X"]



# Public Classes # -----------------------------------------------------------------
@dataclass
class region:
    """
    Constructs a frame object with position, dimensions, and type.

    Args:
    - `pos: tuple[int, int]`, the (y, x) position of the region in the frame from the frame's top-left.
    - `dims: tuple[int, int]`, the (y, x) span of the region from its top-left.
    - `type: str`, the region type as a member of `RESERVED_TYPE_SYMBOLS`.
    """
    type: str
    pos: tuple[int, int]
    dims: tuple[int, int]


@dataclass
class frame:
    """
    Construct a frame object with a name, data array, and configs. Sorting defaults to
    `("type", "pos", "dims")` order, but may be overwritten as wanted using a `tuple` of
    region attribute keys.

    Args:
    - `name: str`, the name of the frame. Only for convenience; does nothing internally.
    - `data: np.ndarray`, the frame's data in `U1` array format.
    - `config: dict`, the optional frame config options. `fixed_size` is determined automatically.
    """    
    name: str
    data: np.ndarray
    config: dict
    regions: region = field(init = False, repr = True)
    region_sort_order: tuple = ("type", "pos", "dims")
    
    def __post_init__(self):
        symbols_in_frame = np.intersect1d(RESERVED_TYPE_SYMBOLS, self.data)
        self.regions = collapse([_all_regions_of_type_from_frame_data(self.data, type) for type in symbols_in_frame])
        self.regions = sorted(self.regions, key = lambda x: itemgetter(*self.region_sort_order)(asdict(x)))
        
        self.config = {**self.config, "fixed_size":(not np.intersect1d(RESERVED_EXPANSION_SYMBOLS, self.data))}



# Public Functions # ---------------------------------------------------------------
def file_to_frames(file_path: str) -> list[frame]:
    """
    Converts a `.bqt` file to a list of `frame` objects.

    Args:
    - `file_path: str`, absolute file path to a `.bqt` file.

    Returns:
    - `frame_list: list[frame]`, List of `frame` objects.
    """
    
    bqt_file = (line for line in map(lambda x: x.strip("\n\t"), fileinput.input(file_path)) if line != "")
    chunks = ([*split_at(c, lambda x: x == "CONFIG")] for c in split_at(bqt_file, lambda x: x == "END") if c != [])
    return [frame(c[0][0][6:], _chunk_to_ndarray(c[0][1:]), _chunk_to_dict(c[1]) if len(c) >= 2 else {}) for c in chunks]



# Private Functions # --------------------------------------------------------------
def _all_regions_of_type_from_frame_data(data: np.ndarray, type: str) -> list[region]:
    """
    Find all regions of a type inside of a numpy array of characters. Intended for use in frame generation.

    Args:
    - data (np.ndarray): The frame.data to search in.
    - type (str): The type (reserved character) to search for a region of.

    Returns:
    - region_list (list[region]): List of regions found in the frame.data of a particular type.
    """    

    regions, coords_in_regions = [], []

    while True:
        reg_wspan, reg_hspan = 0, 0
        reg_start = ()
        
        for iy, ix in np.ndindex(data.shape):
            in_existing_region = (iy, ix) in coords_in_regions

            if not reg_start and data[iy, ix] == type and not in_existing_region:
                reg_start = (iy, ix)
            
            elif reg_start and (data[iy, ix] != type or ix + 1 == data.shape[1]) and not in_existing_region:
                reg_wspan = ix - reg_start[1] + int(ix + 1 == data.shape[1])
                
                while reg_hspan := reg_hspan + 1:
                    if iy + 1 >= data.shape[0]: break
                    if data[iy := iy + 1, ix - 1] != type: break
                break
        else:
            break

        coords_in_regions.extend((coord[0] + reg_start[0], coord[1] + reg_start[1]) for coord in np.ndindex(reg_hspan, reg_wspan))
        regions.append(region(type, reg_start, (reg_hspan, reg_wspan)))

    return regions


def _chunk_to_ndarray(chunk: list[str]) -> np.ndarray:
    return np.array(chunk).view("U1").reshape(len(chunk), -1)
def _chunk_to_dict(arg_list: list) -> dict:
    return {arg[0]:arg[1].strip() for arg in map(lambda x: x.split(":"), arg_list)}