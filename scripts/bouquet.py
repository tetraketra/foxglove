# Imports & Declarations # ---------------------------------------------------------
import numpy as np
import fileinput
from more_itertools import collapse, split_at, chunked


RESERVED_TYPE_SYMBOLS = [*"AaBbLl"]
RESERVED_EXPANSION_SYMBOLS = ["X"]



# Public Classes # -----------------------------------------------------------------
class region():
    def __init__(self, start: tuple[int, int], dims: tuple[int, int], type: str):
        self.start = start
        self.dims = dims
        self.type = type

    def __repr__(self):
        return f"REGION({self.type} at {self.start} of size {self.dims})"

class frame():
    def __init__(self, name: str, data: np.ndarray, config: dict):
        self.name = name
        self.data = data
        self.config = {**config, "fixed_size":(not np.intersect1d(RESERVED_EXPANSION_SYMBOLS, self.data))}
        self.regions = sorted(collapse([_all_regions_of_type_from_frame_data(data, type) for type in np.intersect1d(RESERVED_TYPE_SYMBOLS, self.data)]), key = lambda x: (x.type, x.start))

    def __repr__(self):
        return f"FRAME('{self.name}', {self.config}):\n{self.data} \n{[r for r in self.regions]}"

    def get_param(self, param: str):
        pass #TODO: make args that should be of a particular type (e.g. int) return as such



# Public Functions # ---------------------------------------------------------------
def file_to_frames(file_path: str) -> list[frame]:
    """Converts a `.bqt` file to a list of `frame()` objects.

    Args:
        file_path (str): Absolute file path to a `.bqt` file.

    Returns:
        frame_list (list[frame]): List of `frame()` objects.
    """
    
    bqt_file = (line for line in map(lambda x: x.strip("\n\t"), fileinput.input(file_path)) if line != "")
    chunks = ([*split_at(c, lambda x: x == "CONFIG")] for c in split_at(bqt_file, lambda x: x == "END") if c != [])
    return [frame(chunk[0][0][6:], _chunk_to_ndarray(chunk[0][1:]), _chunk_to_dict(chunk[1]) if len(chunk) >= 2 else {}) for chunk in chunks]



# Private Functions # --------------------------------------------------------------
def _all_regions_of_type_from_frame_data(data: np.ndarray, type: str) -> list[region]:
    """Find all regions of a type inside of a numpy array of characters. Intended for use in frame generation.

    Args:
        data (np.ndarray): The frame.data to search in.
        type (str): The type (reserved character) to search for a region of.

    Returns:
        region_list (list[region]): List of regions found in the frame.data of a particular type.
    """    

    regions = []
    coords_in_region = []

    while True:
        region_topleft = ()
        region_width = 0
        region_height = 0
        
        for iy, ix in np.ndindex(data.shape):
            in_existing_region = (iy, ix) in coords_in_region

            if not region_topleft and data[iy, ix] == type and not in_existing_region:
                region_topleft = (iy, ix)
            
            elif region_topleft and (data[iy, ix] != type or ix + 1 == data.shape[1]) and not in_existing_region:
                region_width = ix - region_topleft[1] + int(ix + 1 == data.shape[1])
                
                while region_height := region_height + 1:
                    if iy + 1 >= data.shape[0]: break
                    if data[iy := iy + 1, ix - 1] != type: break
                break
        else:
            break

        coords_in_region.extend((coord[0] + region_topleft[0], coord[1] + region_topleft[1]) for coord in np.ndindex(region_height, region_width))
        regions.append(region(region_topleft, (region_height, region_width), type))

    return regions

def _chunk_to_ndarray(chunk: list[str]) -> np.ndarray:
    return np.array(chunk).view("U1").reshape(len(chunk), -1)
def _chunk_to_dict(arg_list: list) -> dict:
    return {arg[0]:arg[1].strip() for arg in map(lambda x: x.split(":"), arg_list)}