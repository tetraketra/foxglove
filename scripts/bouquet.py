# Imports & Declarations # ---------------------------------------------------------
from dataclasses import dataclass, field, asdict
from more_itertools import collapse, split_at
from operator import itemgetter
from typing import Literal
import numpy as np
import fileinput

RESERVED_TYPE_SYMBOLS = [*"AaBbLl"]
RESERVED_CUT_SYMBOL = "X"
#np.set_printoptions(edgeitems=30, linewidth=100000)



# Public Classes # -----------------------------------------------------------------
@dataclass
class cut:
    """
    Constructs a cut object with orientation (horizontal or vertical) and weight.

    Args:
    - `orientation: Literal["Horizontal", "Vertical"]`, if the cut is horizontal 
    (for vertical scaling) or vertical (for horizontal scaling). 
    - `pos: int`, a number determining horizontal or vertical axis position.
    """
    
    orientation: Literal["Horizontal", "Vertical"]
    pos: int
    

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
    `("type", "pos", "dims")` order, but may be overwritten as wanted using a tuple of
    region attribute keys.

    Args:
    - `name: str`, the name of the frame. Only for convenience; does nothing internally.
    - `data: np.ndarray`, the frame's data in U1 array format.
    - `config: dict`, the optional frame config options. `fixed_size` is determined automatically.
    """
    
    name: str
    data: np.ndarray
    config: dict
    region_sort_order: tuple = ("type", "pos", "dims") #subset any order
    dims: tuple[int, int] = field(init = False, repr = True) #auto-generated
    regions: region = field(init = False, repr = True) 
    cuts: list[cut] = field(init = False, repr = True) 

    def __post_init__(self):
        symbols_in_frame = np.intersect1d(RESERVED_TYPE_SYMBOLS, self.data)
        self.regions = collapse([_all_regions_of_type_from_frame_data(self.data, type) for type in symbols_in_frame])
        self.regions = sorted(self.regions, key = lambda x: itemgetter(*self.region_sort_order)(asdict(x)))

        self.dims = self.data.shape

        self.config = {**self.config, "fixed_size":(not any(np.intersect1d(RESERVED_CUT_SYMBOL, self.data)))}

        vertical_cut_positions = [i for i, x in enumerate(self.data[0,:]) if x == RESERVED_CUT_SYMBOL]
        horizontal_cut_positions = [i for i, x in enumerate(self.data[:,0]) if x == RESERVED_CUT_SYMBOL]
        vertical_cuts = [cut("Vertical", int(vc_pos)) for vc_pos in vertical_cut_positions]
        horizontal_cuts = [cut("Horizontal", int(vc_pos)) for vc_pos in horizontal_cut_positions]
        self.cuts = vertical_cuts + horizontal_cuts

    def render(self, *data) -> np.ndarray:
        pass



# Public Functions # ---------------------------------------------------------------
def file_to_frames(file_path: str) -> list[frame]:
    """
    Converts a `.bqt` file to a list of frame objects.

    Args:
    - `file_path: str`, absolute file path to a `.bqt` file.

    Returns:
    - `frame_list: list[frame]`, a list of frame objects.
    """

    # list of strings ("lines") => list of lists of strings ("sections") => list of frames
    # `len(c) >= 2`` accounts for config-less frames

    lines = (line for line in map(lambda x: x.strip("\n\t"), fileinput.input(file_path)) if line != "")
    sections = ([*split_at(l, lambda x: x.strip() == "CONFIG")] for l in split_at(lines, lambda x: x.strip() == "END") if l != [])
    return [frame(s[0][0][6:], _strlist_to_ndarray(s[0][1:]), _strlist_to_dict(s[1]) if len(s) >= 2 else {}) for s in sections]



# Private Functions # --------------------------------------------------------------
def _all_regions_of_type_from_frame_data(data: np.ndarray, type: str) -> list[region]:
    """
    Find all regions of a type inside of a numpy array of characters. Intended for use in frame generation.

    Args:
    - `data: np.ndarray`, the frame.data to search in.
    - `type: str`, the type (any reserved character) to search for a region of.

    Returns:
    - `region_list: list[region]`, the list of regions found in the frame.data of a particular type.
    """

    regions, coords_in_regions = [], []

    while True:
        reg_wspan, reg_hspan = 0, 0
        reg_pos = ()

        for iy, ix in np.ndindex(data.shape):
            in_existing_region = (iy, ix) in coords_in_regions

            if not reg_pos and data[iy, ix] == type and not in_existing_region:
                reg_pos = (iy, ix)
                
                while reg_hspan := reg_hspan + 1:
                    if iy + 1 >= data.shape[0]: break
                    if data[iy := iy + 1, reg_pos[1]] != type: break

                while reg_wspan := reg_wspan + 1:
                    if ix + 1 >= data.shape[1]: break
                    if data[reg_pos[0], ix := ix + 1] != type: break
                    
                break

        else:
            break

        reg_coords = ((reg_pos[0] + coord[0], reg_pos[1] + coord[1]) for coord in np.ndindex(reg_hspan, reg_wspan))
        coords_in_regions.extend(reg_coords)

        regions.append(region(type, reg_pos, (reg_hspan, reg_wspan)))

    return regions


def _strlist_to_ndarray(str_list: list[str]) -> np.ndarray:
    """Converts a rectangular `list[str]` to an `ndarray` of type `U1`."""
    return np.array(str_list).view("U1").reshape(len(str_list), -1)


def _strlist_to_dict(arg_list: list[str]) -> dict:
    """Converts a `list[str]` of format `["arg:val", "arg2:val2", ...]` to a `dict`."""
    return {arg[0]:arg[1].strip() for arg in map(lambda x: x.split(":"), arg_list)}



######################################################################

a = file_to_frames(r"EXAMPLE.bqt")
#print(a[0])

# If fixed size, just render in foxglove.
# If not fixed size, call the frame builder during rendering to recreate regions after expanding.>

frame_obj = a[1]
framedata = a[1].data
resize = (10, 10) # (H, W)
#print(frame_obj)
#print(framedata)

def _plop(source_framedata: np.ndarray, target_framedata: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    for iy, ix in np.ndindex(source_framedata.shape):
        target_framedata[pos[0] + iy, pos[1] + ix] = source_framedata[iy, ix]
        
    return target_framedata

framedata = _plop(framedata, np.empty((10,10), dtype = "<U1"), (0, 0))
#print(framedata)

def _expand(framedata: np.ndarray, framecuts: list[cut], direction: Literal["Jorizontal", "Vertical"]) -> np.ndarray:
    if direction == "Horizontal":
        v_cuts_positions = [sfc.pos for sfc in framecuts if sfc.orientation == "Horizontal"]
        print(v_cuts_positions)

    return framedata

expanded_framedata = _expand(framedata, frame_obj.cuts, "Horizontal")
#print(frame_obj.cuts)
print(expanded_framedata)

"""
I'll keep a running "amount left" that resets when they all run out. So imagine I've 
handed out the first two cuts and now the running counts are 2:4:5. Divide each by the 
number of total original weights (13) and you get 0.15:38.5:46.2. I hand out one expansion 
to the highest-weighted cut, then recalculate and go again. This ensures that the frame 
expands according to the weights, even if you don't expand enough to hand out a LCM of 
expansions .
"""
