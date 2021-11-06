"""interact.py  -- core interactive window"""

from symbols import *
import gui
import tree
import gridding


tcl_code = """
grid rowconfigure    $top 0 -weight 1
grid columnconfigure $top 0 -weight 1

ttk::notebook $top.n
grid $top.n -row 0 -column 0 -sticky nsew

ttk::frame $top.n.f1
ttk::frame $top.n.f2 -width 300 -height 200
ttk::frame $top.n.f3 -width 300 -height 200
$top.n add $top.n.f1 -text "Windows Tree"
$top.n add $top.n.f2 -text "Gridding"
$top.n add $top.n.f3 -text "Output"


tk::text $top.n.f1.t -width 60 -height 40 -yscrollcommand "$top.n.f1.s set"
ttk::scrollbar $top.n.f1.s -orient vertical -command "$top.n.f1.t yview"
ttk::treeview $top.n.f1.tree -columns "type text var" -selectmode browse
ttk::label $top.n.f1.lbl -text {reference: window-name [lbl] [btn] [ent:#] [txt:WxH] [chk] [lbox] [f] [lf] [c] [|] [-] -- "text" -- <variable> / <var:default>}

grid $top.n.f1.t -row 0 -column 0 -sticky nsew
grid $top.n.f1.s -row 0 -column 1 -sticky nsew
grid $top.n.f1.tree -row 0 -column 2 -sticky nsew
grid $top.n.f1.lbl -row 1 -column 0 -columnspan 3 -sticky nsew

set w $top.n.f1.tree
$w column #0 -width 200 -anchor w
$w heading #0 -text "Window" -anchor w
$w column type -width 100 -anchor w
$w heading type -text "Type" -anchor w
$w column text -width 100 -anchor w
$w heading text -text "Text" -anchor w
$w column var -width 100 -anchor w
$w heading var -text "Var" -anchor w


grid columnconfigure $top.n.f1 0 -weight 1
grid columnconfigure $top.n.f1 1 -weight 0
grid columnconfigure $top.n.f1 2 -weight 1
grid rowconfigure $top.n.f1 0 -weight 1
grid rowconfigure $top.n.f1 1 -weight 0


tk::text $top.n.f2.text -width 35 -height 40 -yscrollcommand "$top.n.f2.s1 set"
ttk::scrollbar $top.n.f2.s1 -orient vertical -command "$top.n.f2.text yview"
ttk::treeview $top.n.f2.tree -columns "grid span sticky" -selectmode browse -yscrollcommand "$top.n.f2.s2 set"
ttk::scrollbar $top.n.f2.s2 -orient vertical -command "$top.n.f2.tree yview"
ttk::frame $top.n.f2.f
ttk::button $top.n.f2.f.b1 -text "Clear & Populate" -command populate
ttk::label $top.n.f2.f.anon1 -text "reference: window-name \[col,row] <colspan,rowspan> {nsew}"

set w $top.n.f2.tree
$w column #0 -width 200 -anchor w
$w heading #0 -text "Window" -anchor w
$w column grid -width 100 -anchor w
$w heading grid -text "Grid" -anchor w
$w column span -width 100 -anchor w
$w heading span -text "Span" -anchor w
$w column sticky -width 100 -anchor w
$w heading sticky -text "Sticky" -anchor w

grid $top.n.f2.text -row 0 -column 0 -sticky nsew
grid $top.n.f2.s1   -row 0 -column 1 -sticky nsew
grid $top.n.f2.tree -row 0 -column 2 -sticky nsew
grid $top.n.f2.s2   -row 0 -column 3 -sticky nsew
grid $top.n.f2.f    -row 1 -column 0 -columnspan 3 -sticky w
grid $top.n.f2.f.b1     -row 0 -column 0 -sticky w
grid $top.n.f2.f.anon1  -row 1 -column 0 -sticky w

grid columnconfigure $top.n.f2 0 -weight 1
grid columnconfigure $top.n.f2 1 -weight 0
grid columnconfigure $top.n.f2 2 -weight 1
grid columnconfigure $top.n.f2 3 -weight 0
grid rowconfigure $top.n.f2 0 -weight 1
grid rowconfigure $top.n.f2 1 -weight 0


tk::toplevel .toplevel
ttk::frame .toplevel.topframe
"""


# Data -- Preparatory Example Text


txt_example = """
$top
  f [lf] "ttk::frame"

    whf [lf] "Width & Height"
      t [lbl] "This is a test."
      r
        ch [chk]   <use_framew_frameh:1>
        l  [lbl]   "use -width:"
        e  [ent:5] <framew:300>
        l2 [lbl]   "and -height:"
        e2 [ent:5] <frameh:200>
      r2
        ch [chk]   <populateframe:0>
        l  [lbl]   "populate frame with example content"

    pad [lf] "Padding"
      t [lbl] "Padding intro text."
      r
        ch [chk]   <use_padding:1>
        l  [lbl]   "use -padding:"
        e  [ent:4] <framew:5>
      r2
        ch [chk]   <populateframe>
        l  [lbl]   "populate frame with example content"

    bor [lf] "Border"
      t [lbl] "Border intro text."
      r
        ch [chk]   <use_border:1>
        l  [lbl]   "use -borderwidth:"
        e  [ent:4] <borderwidth:5>
        l2 [lbl]   "and -relief:"
        choice [lbox:5] "flat,sunken,solid,ridge,groove"
""".lstrip()

grid_example = """
$top {nsew}

$top.f [0,0] {nsew}

$top.f.whf [0,0] {nsew}
$top.f.pad [1,0] {nsew}
$top.f.bor [1,1] {nsew}

$top.f.whf.t [0,0] {nsew}
$top.f.whf.r [0,1] {nsew}
$top.f.whf.r2 [0,2] {nsew}

$top.f.whf.r.ch [0,0] {nsew}
$top.f.whf.r.l [1,0] {nsew}
$top.f.whf.r.e [2,0] {nsew}
$top.f.whf.r.l2 [1,1] {nsew}
$top.f.whf.r.e2 [2,1] {nsew}

$top.f.whf.r2.ch [0,0] {nsew}
$top.f.whf.r2.l [1,0] {nsew}

$top.f.pad.t [0,0] {nsew}
$top.f.pad.r [0,1] {nsew}
$top.f.pad.r2 [0,2] {nsew}

$top.f.pad.r.ch [0,0] {nsew}
$top.f.pad.r.l [1,0] {nsew}
$top.f.pad.r.e [2,0] {nsew}

$top.f.pad.r2.ch [0,0] {nsew}
$top.f.pad.r2.l [1,0] {nsew}

$top.f.bor.t [0,0] {nsew}
$top.f.bor.r [0,1] {nsew}

$top.f.bor.r.ch [0,0] {nsew}
$top.f.bor.r.l [1,0] {nsew}
$top.f.bor.r.e [2,0] {nsew}
$top.f.bor.r.l2 [1,1] {nsew}
$top.f.bor.r.choice [2,1] {nsew}
""".lstrip()


# Functions -- Setup

def setup():
    gui.mkcmd("populate", populate)

def open_up():
    gui.toplevel_unique(".editor", "liontkcomposer2")
    gui.tclexec(tcl_code)
    gui.cue(".editor.n.f1.t")
    gui.text_set(txt_example)
    gui.cue(".editor.n.f2.text")
    gui.text_set(grid_example)
    update()


# Callback -- repop(ulate)

def populate():
    """Clear & repopulate the Gridding text area."""
    gui.cue(".editor.n.f2.text")
    gridding.populate()
    

# Periodic Updates (every 100ms)

last_time = [None, None]

def update():
    change_found = False
    gui.cue(".editor.n.f1.t")
    code = gui.text_get()
    if code != last_time[0]:
        change_found = True
        last_time[0] = code
        tree.reset()  # reset all nodes
        tree.readlines(code)
        gui.cue(".editor.n.f1.tree")
        tree.populate_tree()
        tree.generate()
    gui.cue(".editor.n.f2.text")
    code = gui.text_get()
    if code != last_time[1]:
        tree.reset_gridding()
        change_found = True
        last_time[1] = code
        gridding.readlines(code)
        gui.cue(".editor.n.f2.tree")
        gridding.populate_tree()
        gridding.generate()
    if change_found:
        gui.tclexec("destroy .toplevel.topframe")
        gui.tclexec("ttk::frame .toplevel.topframe")
        gui.poke("top", ".toplevel.topframe")
        for ln in tree.g[TCL].splitlines():
            try:
                gui.tclexec(ln)
            except:
                pass
        for ln in gridding.g[TCL].splitlines():
            try:
                gui.tclexec(ln)
            except:
                pass

