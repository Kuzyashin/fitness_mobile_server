# -*- coding: utf-8 -*-

##################################################################
# ALL INCLUDES OF SETTINGS FILES
#
# Add your new settings file here, order can be important
##################################################################
from .base import *
from .logging import *
from .apps import *
from .auth import *
from .datetime import *
from .languages import *
from .middlewares import *
from .static import *
from .templates import *
from .rest import *
from .swagger import *


try:
    from .local import *
except ImportError:
    from .production import *
    print("There is no local settings")