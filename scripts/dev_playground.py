# Imports # ------------------------------------------------------------------------
import bouquet as bqt
import numpy as np

# Testing # ------------------------------------------------------------------------
a = bqt.file_to_frames(r"/home/tetraketra/Documents/GitHub/foxglove/scripts/EXAMPLE.bqt")
print(a)


# If fixed size, just render in foxglove.
# If not fixed size, call the frame builder during rendering to recreate regions after expanding.