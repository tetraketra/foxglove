# Imports # ------------------------------------------------------------------------
import bouquet as bqt
from typing import Literal
import numpy as np

# Testing # ------------------------------------------------------------------------
a = bqt.file_to_frames(r"EXAMPLE.bqt")
#print(a[0])

# If fixed size, just render in foxglove.
# If not fixed size, call the frame builder during rendering to recreate regions after expanding.>
