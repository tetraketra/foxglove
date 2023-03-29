# Imports # ------------------------------------------------------------------------
import bouquet as bqt
from typing import Literal
import numpy as np

# Testing # ------------------------------------------------------------------------
a = bqt.file_to_frames(r"EXAMPLE.bqt")
#print(a[0])

# If fixed size, just render in foxglove.
# If not fixed size, call the frame builder during rendering to recreate regions after expanding.>

frame = a[1].data
resize = (10, 10) # (H, W)
#print(frame)

def _plop(source: np.ndarray, target: np.ndarray, pos: tuple[int, int]):
    for iy, ix in np.ndindex(source.shape):
        target[pos[0] + iy, pos[1] + ix] = source[iy, ix]
        
    return target

frame_with_empty = _plop(frame, np.empty((10,10), dtype = "<U1"), (0, 0))

def _expand(frame: np.ndarray, direction: Literal["horizontal", "vertical"]):
    