import os
import sys

# Used to circumvent “PEP8 – import not at top of file with sys.path”
bp = os.path.dirname(os.path.realpath('.')).split(os.sep)
path = os.sep.join(bp + ['code'])
sys.path.insert(0, path)
