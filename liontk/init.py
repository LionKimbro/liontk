"""init.py  -- initialization routines for liontk

init()  -- call this once, and only once, to set up
"""

from symbols import *

import guitalk
import gui


def init():
    """call setup routines for all modules

    Calls the setup() routines in all other modules, in the
    appropriate order, to setup liontk.
    """
    guitalk.setup()  # must come FIRST, contacts Tcl/Tk
    gui.setup()  # issues global GUI setup commands to Tcl/Tk


