"""
Project settings are separated to
base.py  - basic application specific settings
local.py - settings specific to an installation (this should never be saved in repository)
"""
import sys

from .base import *

SERVER_CONFIGURATION_DIR = '/etc/poeg'
sys.path.insert(0, SERVER_CONFIGURATION_DIR)

try:
    from poeg_conf import *
except ImportError:
    pass
finally:
    del sys.path[0]

# finally local settings overides all
# overrides anything
try:
    from .local import *
except ImportError:
    pass
