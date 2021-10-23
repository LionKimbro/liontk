"""guisys.py  -- GUI system

select(win)  -- select a window
  "win"  -- the tkinter name ("tkname") for a toplevel (ex: ".settings")
"""

import tkinter as tk

from symbols import *
from listdict import cue as list_cue
from listdict import val, val1, val01, req, srt
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN

import menubar


# Global Variables

g = {NEXTID: 1,
     TCL: {REQUEST: None, RESULT: None}}


def nextid():
    """Return NEXTID, auto-increment."""
    g[NEXTID] += 1
    return g[NEXTID]-1


# Global Variables -- Running Tasks

tasks = []

CLOSETOP="CLOSETOP"  # TYPE:CLOSETOP -- instructs to close TOPLEVEL
TOPLEVEL="TOPLEVEL"  # TOPLEVEL -- contains the toplevel window to close

CALL="CALL"  # TYPE:CALL -- instructs to call a specific fn
FN="FN"  # the function to call

EXIT="EXIT"  # TYPE:EXIT -- instructs to exit the program entirely


# Global Root & Functions -- Tk Fundamental

root = tk.Tk()

call = root.tk.call  # receives a list of literal strings
createcommand = root.tk.createcommand  # literal key?
tkeval = root.tk.eval  # direct; handled as a single string by tk


# Functions -- primary interfaces: peek, poke, tclexec, & mkcmd

def subst(tkname):
    """Perform substitutions on a tkname.
    
    This is most commonly used to resolve a full path.
    
    For example, "$top.foo" can substitute to "$tag1.foo".
    """
    return tkeval('subst '+tkname)

def peek(tkname):
    """Peek a value.
    
    For example, peek("w") -> ".settings" (or whatever)
    """
    return tkeval('set '+tkname)

def poke(tkname, s):
    """Poke a string value literally into tk.
    
    Note that when you use CALL, it doesn't perform $-substitutions.
    So I perform substitutions literally for the key, and then use that for the set call.
    """
    call('set', subst(tkname), s)  # use call, because it will work literally


def tclexec(tcl_code):
    """Run tcl code"""
    g[TCL][REQUEST] = tcl_code
    g[TCL][RESULT] = tkeval(tcl_code)
    return g[TCL][RESULT]

def mkcmd(tkname, fn):
    """Bind a tk command to a function"""
    createcommand(tkname, fn)


# Functions -- Tk main loop control

def loop():
    """Setup complete; Run main loop."""
    root.mainloop()


def after_idle():
    """Call mainloop_tasks() RIGHT AWAY, don't fuss for 100ms"""
    cancel()
    tclexec("after idle mainloop_tasks")


def schedule():
    """Schedule mainloop task, 100 ms into the future."""
    tclexec("set afterhandle [after 100 mainloop_tasks]")


def cancel():
    """Cancel the next scheduled mainloop task."""
    tclexec("after cancel $afterhandle")
    tclexec("unset afterhandle")


def mainloop_tasks():
    import interact
    interact.update()
    while tasks:
        D = tasks.pop()
        if D[TYPE] == CLOSETOP:
            cue(D[TOPLEVEL])
            tclexec("destroy $w")
            if not toplevels():
                task_exit()
                after_idle()
        elif D[TYPE] == CALL:
            D[FN]()
        elif D[TYPE] == EXIT:
            root.destroy()
    schedule()  # schedule the next run


# Functions -- main entry & debug

def debug():
    cancel()
    breakpoint()
    schedule()


# Functions -- Setup routine


def setup():
    tclexec("wm withdraw .")  # close initial tk window
    tclexec("option add *tearOff 0")  # turn off tear-off menus
    mkcmd("wm_delete_window", wm_delete_window)
    mkcmd("mainloop_tasks", mainloop_tasks)
    schedule()  # start the main loop


# Focus & Cue-ing

def cue(tkname=None):
    """Set tk's $w to tkname or currently focused window.
    
    Very importantly: tkname may contain substitutions, allowing for
    indirect referencing of window names.  For example, "$top.foo" can
    be used to point to a window on a top level identified by tcl
    variable "top".  (see: cue_top, for example)
    
    This is commonly used in the tcl_code executed to customize a
    newly created window.
    """
    if tkname is None:
        tkname = focused()
    else:
        tkname = subst(tkname)
    poke("w", tkname)

def cue_top():
    """Sets tk's $top to toplevel for $w."""
    poke("top", top())

def cur():
    return peek("w")

def top():
    """Returns the toplevel for $w."""
    return tclexec("winfo toplevel $w")

def name():
    """Returns the name of $w, alone, without parents"""
    return tclexec("winfo name $w")

def wtype():
    """Returns the "window type" of $w.
    
    Important notes:
    * "window type" is not a tk concept;
      rather, Tk refers to a window's "class";
      see "winfo class" for more on this context
    * "window type" is made up by me, and consists of a matching symbol;
      presently (2021-10-09), I support here the symbols:
        ENTRY, TEXT, and LISTBOX
    * if a matching symbol is not found, returns the window class, per Tk
    * HOWEVER: you should not use the window class --
      instead, I want you to extend symbols.py with a symbol to correspond
      with the window class, and that will be known as the window's "type"
    * because type is already used and essential to Python,
      I call the window type "wtype"
    """
    x = tclexec("winfo class $w")
    if x == "TEntry":
        return ENTRY
    elif x == "Text":
        return TEXT
    elif x == "Listbox":
        return LISTBOX
    else:
        return x

def children():
    """Return the path names of the children of $w, as a list"""
    return tclexec("winfo children $w").split()


def text_get():
    """Return text from the cue'd window."""
    wt = wtype()
    if wt == ENTRY:
        return tclexec("$w get")
    elif wt == TEXT:
        return tclexec("$w get 1.0 end")
    else:
        raise ValueError("$w type not recognized")

def text_set(s):
    """Set text into the cue'd window."""
    wt = wtype()
    if wt == ENTRY:
        poke("tmp", s)
        tclexec("$w delete 0 end")
        tclexec("$w insert 0 $tmp")
    elif wt == TEXT:
        poke("tmp", s)
        tclexec("$w delete 1.0 end")
        tclexec("$w insert 1.0 $tmp")
    else:
        raise ValueError("$w type not recognized")

def text_ro():
    """Make text in the cue'd window read-only."""
    wt = wtype()
    if wt == ENTRY:
        tclexec("$w configure -state readonly")  # can select, but not write
    elif wt == TEXT:
        tclexec("$w configure -state disabled")  # "readonly" doesn't exist for text
    else:
        raise ValueError("$w type not recognized")

def text_rw():
    """Make text in the cue'd window read-write."""
    wt = wtype()
    if wt == ENTRY:
        tclexec("$w configure -state normal")
    elif wt == TEXT:
        tclexec("$w configure -state normal")
    else:
        raise ValueError("$w type not recognized")

def text_see_end():
    """Put the end into view."""
    wt = wtype()
    if wt == TEXT:
        tclexec("$w see end")
    else:
        raise ValueError("$w type not recognized for text_see_end()")


def list_clear():
    tclexec("$w delete 0 end")

def list_add(s):
    poke("tmp", s)
    tclexec("$w insert end $tmp")

def list_set(L):
    list_clear()
    for x in L:
        list_add(x)

def list_selected():
    return tclexec("$w get [$w curselection]")
    

def set_win():
    """Don't call this for new code.
    
    This is for compatability with older code.
    It sets $win to the toplevel for w.
    """
    tclexec("set win [winfo toplevel $w]")

def cuekind(kind):
    """Cue a unique top-level, by kind.
    
    Note that it must be UNIQUE, otherwise behavior is undefined.
    """
    rec = record_for_kind(kind)
    assert rec[UNIQUE]
    cue(rec[TKNAME])


def tkname_to_top(tkname):
    poke("tmp", tkname)
    return tclexec("winfo toplevel $tmp")

def focused():
    """Return tkname of current Tk focused window.
    
    WARNING: While debugging, if the toplevel is no longer focused,
             you're going to get an empty string back, which,
             technically speaking, is correct.
    """
    return tclexec("focus")


# Top-Level Management

def lift():
    """Raise the cue'd window to the top level."""
    tclexec("focus $w")
    tclexec("raise [winfo toplevel $w]")

def title(ttl):
    """Reset the title of the cue'd window's toplevel."""
    poke("tmp", ttl)
    tclexec("wm title [winfo toplevel $w] $tmp")

def exists():
    """Return True if the cue'd window still exists."""
    return tclexec("winfo exists $w") == '1'

def toplevels():
    return tclexec("winfo children .").split()

def toplevel_unique(tkname, ttl):
    """Create or lift a unique toplevel.
    
    If it was already created:
      - the window is lifted,
      - returns False
    
    If it was NOT already created,
      - the window is created,
      - returns True (so you can do further preparations for it
    
    TODO: relocate title assignment, outside of this fn,
          matching toplevel_recurring;
     [ ] and then update the docs of toplevel_recurring,
         removing the explanation
    """
    cue(tkname)
    if exists():
        lift()
        return False
    else:
        tclexec("toplevel $w")
        cue_top()
        title(ttl)
        tclexec("wm protocol $w WM_DELETE_WINDOW wm_delete_window")
        menubar.attach()
        return True

def toplevel_recurring(tkname_prefix):
    """Create a new top-level, and set $top to, and return, its tkname.
    
    Because the titles of recurring windows are highly variable,
    title assignment is not bundled with this functionality.
    """
    tkname = tkname_prefix + str(nextid())
    cue(tkname)
    tclexec("toplevel $w")
    cue_top()
    tclexec("wm protocol $w WM_DELETE_WINDOW wm_delete_window")
    menubar.attach()
    return tkname

def wm_delete_window():
    """A top-level is being closed.  Is the program over?"""
    cue(); task_closetop(top())


# Task Creation

def task_closetop(toplevel):
    tasks.append({TYPE:CLOSETOP,
                  TOPLEVEL: toplevel})

def task_fn(fn):
    tasks.append({TYPE:CALL,
                  FN: fn})

def task_exit():
    tasks.append({TYPE:EXIT})

