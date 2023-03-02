from .wrapping import Wrapper
from .typing import ishashable, issequence
from .cp import classproperty
from .infix import Infix
from .attr import attributor

import os
import appdirs
import warnings
from typing import Optional

__version__ = "1.0.18"
__description__ = "Common developer utilities and base classes to support other dewloosh packages."

# catch annoying numpy/vtk future warning:
warnings.simplefilter(action='ignore', category=FutureWarning)

# If available, a local vtk-data instance will be used for examples
DEWLOOSH_DATA_PATH: Optional[str] = None
if 'DEWLOOSH_DATA_PATH' in os.environ:
    DEWLOOSH_DATA_PATH = os.environ['DEWLOOSH_DATA_PATH']
    if not os.path.isdir(DEWLOOSH_DATA_PATH):
        warnings.warn(
            f"DEWLOOSH_DATA_PATH: {DEWLOOSH_DATA_PATH} is an invalid path")
    if not os.path.isdir(os.path.join(DEWLOOSH_DATA_PATH, 'Data')):
        warnings.warn(
            f"DEWLOOSH_DATA_PATH: {os.path.join(DEWLOOSH_DATA_PATH, 'Data')} does not exist")

# allow user to override the examples path
if 'DEWLOOSH_USERDATA_PATH' in os.environ:
    USER_DATA_PATH = os.environ['DEWLOOSH_USERDATA_PATH']
    if not os.path.isdir(USER_DATA_PATH):
        raise FileNotFoundError(
            f'Invalid DEWLOOSH_USERDATA_PATH at {USER_DATA_PATH}')
else:
    USER_DATA_PATH = appdirs.user_data_dir('DEWLOOSH')
    try:
        # Set up data directory
        os.makedirs(USER_DATA_PATH, exist_ok=True)
    except Exception as e:
        warnings.warn(
            f'Unable to create `DEWLOOSH_USERDATA_PATH` at "{USER_DATA_PATH}"\n'
            f'Error: {e}\n\n'
            'Override the default path by setting the environmental variable '
            '`DEWLOOSH_USERDATA_PATH` to a writable path.'
        )
        USER_DATA_PATH = ''

EXAMPLES_PATH = os.path.join(USER_DATA_PATH, 'examples')
try:
    os.makedirs(EXAMPLES_PATH, exist_ok=True)
except Exception as e:
    warnings.warn(
        f'Unable to create `EXAMPLES_PATH` at "{EXAMPLES_PATH}"\n'
        f'Error: {e}\n\n'
        'Override the default path by setting the environmental variable '
        '`DEWLOOSH_USERDATA_PATH` to a writable path.'
    )
    EXAMPLES_PATH = ''


# Set a parameter to control default print format for floats outside
# of the plotter
FLOAT_FORMAT = "{:.3e}"
