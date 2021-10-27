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

ttk::frame $top.n.f1 -width 300 -height 200
ttk::frame $top.n.f2 -width 300 -height 200
ttk::frame $top.n.f3 -width 300 -height 200
$top.n add $top.n.f1 -text "Windows Tree"
$top.n add $top.n.f2 -text "Gridding"
$top.n add $top.n.f3 -text "Output"


tk::text $top.n.f1.t -width 60 -height 50 -yscrollcommand "$top.n.f1.s set"
ttk::scrollbar $top.n.f1.s -orient vertical -command "$top.n.f1.t yview"
ttk::treeview $top.n.f1.tree -columns "type text var" -selectmode browse
ttk::label $top.n.f1.lbl -text {reference: window-name [lbl] [btn] [ent:#] [text:WxH] [chk] [lbox] [f] [lf] [c] [|] [-] -- "text" -- <variable> / <var:default>}

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


tk::text $top.n.f2.text -width 35 -height 60 -yscrollcommand "$top.n.f2.s1 set"
ttk::scrollbar $top.n.f2.s1 -orient vertical -command "$top.n.f2.text yview"
ttk::treeview $top.n.f2.tree -columns "grid span sticky" -selectmode browse -yscrollcommand "$top.n.f2.s2 set"
ttk::scrollbar $top.n.f2.s2 -orient vertical -command "$top.n.f2.tree yview"
ttk::frame $top.n.f2.f
ttk::button $top.n.f2.f.b1 -text "Clear & Populate" -command populate
ttk::label $top.n.f2.f.anon1 -text "reference: window-name \[col,row] <colspan,rowspan> {nsew}"

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
"""


# Data -- Preparatory Example Text


txt_example = """
$top
  f [lf] "ttk::frame"

    whf [lf] "Width & Height"
      t [lbl]
      r
        ch [chk]   <use_framew_frameh:1>
        l  [lbl]   "use -width:"
        e  [ent:4] <framew:300>
        l2 [lbl]   "and -height:"
        e2 [ent:4] <frameh:200>
      r2
        ch [chk]   <populateframe:0>
        l  [lbl]   "populate frame with example content"

    pad [lf] "Padding"
      t [lbl]
      r
        ch [chk]   <use_padding:1>
        l  [lbl]   "use -padding:"
        e  [ent:4] <framew:5>
      r2
        ch [chk]   <populateframe>
        l  [lbl]   "populate frame with example content"

    bor [lf] "Border"
      t [lbl]
      r
        ch [chk]   <use_border:1>
        l  [lbl]   "use -borderwidth:"
        e  [ent:4] <borderwidth:5>
        l2 [lbl]   "and -relief:"
        choice [lbox:5] "flat,sunken,solid,ridge,groove"
"""


# Functions -- Setup

def setup():
    gui.mkcmd("populate", populate)

def open_up():
    gui.toplevel_unique(".editor", "liontkcomposer2")
    gui.tclexec(tcl_code)
    gui.cue(".editor.n.f1.t")
    gui.text_set(txt_example)
    update()


# Callback -- repop(ulate)

def populate():
    """Clear & repopulate the Gridding text area."""
    gui.cue(".editor.n.f2.text")
    gridding.populate()
    

# Periodic Updates (every 100ms)

last_time = [None, None]

def update():
    gui.cue(".editor.n.f1.t")
    code = gui.text_get()
    if code != last_time[0]:
        last_time[0] = code
        tree.readlines(code)
        gui.cue(".editor.n.f1.tree")
        tree.populate_tree()
        tree.generate()
    gui.cue(".editor.n.f2.text")
    code = gui.text_get()
    if code != last_time[1]:
        last_time[1] = code
        gridding.readlines(code)
        gridding.generate()

