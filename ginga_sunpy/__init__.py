<<<<<<< HEAD
=======
#from .SunPy import *

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''
    try:
        from .version import githash as __githash__
    except ImportError:
        __githash__ = ''
>>>>>>> 164c40fecd99baf9d1f5cb27064620ff454692d3
