"""interact.py  -- core interactive window"""

import time
import sys

from symbols import *

import gui


tcl_code = """
grid columnconfigure .editor 0 -weight 1
grid rowconfigure    .editor 0 -weight 1

ttk::frame .editor.f
grid .editor.f -row 0 -column 0  -sticky nsew

grid columnconfigure .editor.f 0 -weight 1
grid columnconfigure .editor.f 1 -weight 0
grid columnconfigure .editor.f 2 -weight 1
grid rowconfigure .editor.f 0 -weight 4
grid rowconfigure .editor.f 1 -weight 1

tk::text       .editor.f.doc        -width 72 -height 70 -yscrollcommand ".editor.f.doc_scroll set"
ttk::scrollbar .editor.f.doc_scroll -orient vertical            -command ".editor.f.doc yview"
ttk::frame     .editor.f.cage -width 300 -height 300
tk::text       .editor.f.out         -width 72 -height 10

grid .editor.f.doc        -row 0 -rowspan 2 -column 0 -sticky nsew
grid .editor.f.doc_scroll -row 0 -rowspan 2 -column 1 -sticky nsew
grid .editor.f.cage       -row 0            -column 2 -sticky nsew
grid .editor.f.out        -row 1            -column 2 -sticky nsew

grid columnconfigure .editor.f.cage 0 -weight 1
grid rowconfigure    .editor.f.cage 0 -weight 1

ttk::frame .editor.f.cage.top

focus .editor.f.doc

menu .m
.m add cascade -label {File} -underline 0 -menu [menu .m.m0]
.m.m0 add command -label Exit -underline 1 -command ::exit

.m add cascade -label {Insert} -underline 0 -menu [menu .m.m1]
.m.m1 add command -label Frame -underline 0 -command ::ins_frame
.m.m1 add command -label Label -underline 0 -command ::ins_label
.m.m1 add command -label Button -underline 0 -command ::ins_button
.m.m1 add command -label Entry -underline 0 -command ::ins_entry
.m.m1 add command -label Checkbutton -underline 1 -command ::ins_checkbutton
.m.m1 add command -label Radiobutton -underline 2 -command ::ins_radiobutton
.m.m1 add command -label Combobox -underline 1 -command ::ins_combobox
.m.m1 add command -label Listbox -underline 1 -command ::ins_listbox
.m.m1 add separator
.m.m1 add command -label Tree -underline 1 -command ::ins_tree
.m.m1 add command -label Text -underline 0 -command ::ins_text
.m.m1 add command -label Canvas -underline 0 -command ::ins_canvas
.m.m1 add separator
.m.m1 add command -label {Top Relief} -underline 2 -command ::ins_toprelief
.m.m1 add command -label {Basic Setup} -underline 1 -command ::ins_basicsetup
.m.m1 add command -label {Menu} -underline 0 -command ::ins_menu
.m.m1 add command -label {Example} -underline 1 -command ::ins_example
.m.m1 add command -label {Example 2} -underline 8 -command ::ins_example2
.m.m1 add command -label {Example 3} -underline 8 -command ::ins_example3
.m.m1 add command -label {Style} -underline 0 -command ::ins_style

.editor configure -menu .m
"""


# Data -- Insertion Text

txt_frame = """
ttk::frame $top.f -padding 5 -relief raised
grid $top.f -row 0 -column 0  -sticky nsew
"""

txt_label = """
ttk::label $top.f.lbl -text "This is a label."
grid $top.f.lbl -row 0 -column 0
"""

txt_button = """
ttk::button $top.f.btn -text "This is a test."
grid $top.f.btn -row 0 -column 0
"""

txt_entry = """
ttk::entry $top.f.e0 -width 5 -state disabled
grid $top.f.e0 -row 3 -column 0 -columnspan 2 -sticky nsw
bind $top.f.e0 <Return> {calculate}
"""

txt_checkbutton = """
ttk::checkbutton $top.f.check
grid $top.f.check -row 0 -column 1
if {![$top.f.check instate selected]} {$top.f.check invoke}
"""

txt_combobox = """
ttk::combobox $top.f.cbox -state readonly -values [list "United States" Canada Australia]
$top.f.cbox set "United States"
grid $top.f.cbox -row 2 -column 0 -sticky nsew
bind $top.f.cbox <<ComboboxSelected>> {puts [$top.f.cbox get]}
"""

txt_tree = """
ttk::treeview $top.f.tree -height 6 -yscrollcommand "$top.f.s set"
grid $top.f.tree -row 2 -column 0 -columnspan 2 -sticky nsew

ttk::scrollbar $top.f.s -orient vertical -command "$top.f.tree yview"
grid $top.f.s -row 2 -column 3 -sticky nsew

set tktree $top.f.tree
$tktree insert {} end -id foo -text "foo"
$tktree insert {} end -id bar -text "bar"
$tktree insert {} end -id x -text "x"
$tktree insert {} end -id y -text "y"
$tktree insert {} end -id z -text "z"
$tktree insert {} end -id a -text "a"
$tktree insert {} end -id b -text "b"
$tktree insert {} end -id c -text "c"
$tktree insert {} end -id d -text "d"
$tktree insert {} end -id e -text "e"
"""

txt_text = """
tk::text $top.f.t -width 40 -height 10 -yscrollcommand "$top.f.s set"
grid $top.f.t -row 0 -column 0 -sticky nsew

ttk::scrollbar $top.f.s -orient vertical -command "$top.f.t yview"
grid $top.f.s -row 0 -column 1 -sticky nsew
"""

txt_canvas = """
tk::canvas $top.f.c -width 300 -height 200
grid $top.f.c -row 0 -column 0 -sticky nsew
$top.f.c create line 0 0 100 50
"""

txt_toprelief = """
$top configure -border 2 -relief sunken
"""

txt_basicsetup = """
grid columnconfigure $top 0 -weight 1
grid rowconfigure    $top 0 -weight 1

ttk::frame $top.f
grid $top.f -row 0 -column 0  -sticky nsew

grid columnconfigure $top.f 0 -weight 1
grid columnconfigure $top.f 1 -weight 1
grid columnconfigure $top.f 2 -weight 1
grid    rowconfigure $top.f 0 -weight 1
grid    rowconfigure $top.f 1 -weight 1
grid    rowconfigure $top.f 2 -weight 1
"""

txt_example = """
$top configure -border 2 -relief raise

ttk::frame $top.f -padding 5
grid $top.f -row 0 -column 0  -sticky nsew

ttk::button $top.f.btn -text "This is a test."
ttk::entry $top.f.entry -width 25
ttk::button $top.f.b3 -text "Submit"
ttk::button $top.f.b2 -text "This is NOT a test."

grid $top.f.btn   -row 0 -column 0
grid $top.f.b2    -row 1 -column 0
grid $top.f.entry -row 0 -column 1
grid $top.f.b3    -row 1 -column 1 -sticky nsew

ttk::treeview $top.f.tree -height 8
grid $top.f.tree -row 2 -column 0 -columnspan 2 -sticky nsew

set tktree $top.f.tree
$tktree insert {} end -id foo -text "foo"
$tktree insert {} end -id bar -text "bar"
$tktree insert {} end -id vector -text "vector" -open true
$tktree insert vector end -id x -text "x"
$tktree insert vector end -id y -text "y"
$tktree insert vector end -id z -text "z"
$tktree insert z end -id z2 -text "z2"

tk::canvas $top.f.c
grid $top.f.c -row 3 -column 0 -columnspan 2 -sticky nsew

set c $top.f.c

$c create rectangle 40.0 40.0 200.0 120.0 -disabledwidth 0 -width 2.0 -tags {Rectangle obj banka bankarect}
$c create text 120.0 60.0 -font {Arial 12} -text {Bank A:} -tags {text obj banka bankalbl}
$c create text 120.0 80.0 -font {Arial 12} -text BANKASTATUS -tags {text obj banka bankastatus}

$c create rectangle 40.0 140.0 200.0 220.0 -disabledwidth 0 -width 2.0 -tags {Rectangle obj bankb bankbrect}
$c create text 120.0 160.0 -font {Arial 12} -text {Bank B:} -tags {text obj bankb bankblbl}
$c create text 120.0 180.0 -font {Arial 12} -text BANKBSTATUS -tags {text obj bankb bankbstatus}

$c itemconfigure bankarect -outline blue -fill white
$c itemconfigure bankalbl -fill blue
$c itemconfigure bankastatus -fill red -text "Deposit Pending"

$c itemconfigure bankbrect -outline grey -fill grey80
$c itemconfigure bankblbl -fill white
$c itemconfigure bankbstatus -fill white -text "--None--" -font {Arial 9 italic}
"""

txt_example2 = """
ttk::frame $top.f -padding 5
grid $top.f -row 0 -column 0  -sticky nsew

ttk::labelframe $top.f.items -padding 5 -text "Items"
grid $top.f.items -row 0 -column 0  -sticky nsew

ttk::label $top.f.items.lbl1 -text "Name:"
ttk::label $top.f.items.lbl2 -text "Age:"
ttk::label $top.f.items.lbl3 -text "Description:"
ttk::entry $top.f.items.name -width 50
ttk::entry $top.f.items.age  -width 5
tk::text   $top.f.items.desc -width 40 -height 3

grid $top.f.items.lbl1 -row 0 -column 0 -sticky ne
grid $top.f.items.name -row 0 -column 1 -sticky ew
grid $top.f.items.lbl2 -row 1 -column 0 -sticky ne -pady "5 0"
grid $top.f.items.age  -row 1 -column 1 -sticky w -pady "5 0"
grid $top.f.items.lbl3  -row 2 -column 0 -sticky ne -pady "5 0"
grid $top.f.items.desc -row 2 -column 1 -sticky nsew -pady "5 0"
"""

txt_example3 = """
ttk::frame $top.f -padding 5 -relief raised
grid $top.f -row 0 -column 0 -sticky nsew

ttk::frame $top.f.buttons -border 5 -relief raised
grid $top.f.buttons -row 0 -column 0 -sticky nsew

ttk::button $top.f.buttons.btn -text "This is a test."
ttk::button $top.f.buttons.btn2 -text "This is another test."
ttk::button $top.f.buttons.btn3 -text "More"
ttk::button $top.f.buttons.btn4 -text "Buttons"
grid $top.f.buttons.btn -row 0 -column 0 -sticky nsew
grid $top.f.buttons.btn2 -row 1 -column 0 -sticky nsew
grid $top.f.buttons.btn3 -row 2 -column 0 -sticky nsew
grid $top.f.buttons.btn4 -row 3 -column 0 -sticky nsew

tk::canvas $top.f.buttons.c -width 100 -height 150
grid $top.f.buttons.c -row 4 -column 0 -sticky n

set c $top.f.buttons.c

$c create rectangle 10.0 10.0 30.0 30.0 -disabledwidth 0 -tags {Rectangle obj x}
$c create rectangle 40.0 10.0 60.0 30.0 -disabledwidth 0 -tags {Rectangle obj y}
$c create rectangle 70.0 10.0 90.0 30.0 -disabledwidth 0 -tags {Rectangle obj z}
$c create rectangle 10.0 40.0 30.0 60.0 -disabledwidth 0 -tags {Rectangle obj a}
$c create rectangle 40.0 40.0 60.0 60.0 -disabledwidth 0 -tags {Rectangle obj b}
$c create rectangle 70.0 40.0 90.0 60.0 -disabledwidth 0 -tags {Rectangle obj c}
$c create rectangle 10.0 70.0 30.0 90.0 -disabledwidth 0 -tags {Rectangle obj n1}
$c create rectangle 40.0 70.0 60.0 90.0 -disabledwidth 0 -tags {Rectangle obj n2}
$c create rectangle 70.0 70.0 90.0 90.0 -disabledwidth 0 -tags {Rectangle obj n3}
$c create text 20.0 20.0 -font {Arial 10 {}} -text X -tags {text obj txtx}
$c create text 50.0 20.0 -font {Arial 10 {}} -text Y -tags {text obj txty}
$c create text 80.0 20.0 -font {Arial 10 {}} -text Z -tags {text obj txtz}
$c create text 20.0 50.0 -font {Arial 10 {}} -text A -tags {text obj txta}
$c create text 50.0 50.0 -font {Arial 10 {}} -text B -tags {text obj txtb}
$c create text 80.0 50.0 -font {Arial 10 {}} -text C -tags {text obj txtc}
$c create text 20.0 80.0 -font {Arial 10 {}} -text 1 -tags {text obj txtn1}
$c create text 50.0 80.0 -font {Arial 10 {}} -text 2 -tags {text obj txtn2}
$c create text 80.0 80.0 -font {Arial 10 {}} -text 3 -tags {text obj txtn3}

$c itemconfigure y -fill lightgreen
$c itemconfigure c -fill cyan
$c itemconfigure n1 -fill yellow


tk::canvas $top.f.c -width 350 -height 280
grid $top.f.c -row 0 -column 1 -sticky nsew

grid rowconfigure $top.f 0 -weight 0

set c $top.f.c
$c create text 40.0 80.0 -anchor w -font {Arial 12 {}} -text {Create graphics with Tkpaint 2.0,
save the graphic to a tcl file,
and then copy the tcl code here
to create logical graphical elements
in your Canvas.} -tags {text obj utag6}
$c create oval 80.0 160.0 120.0 200.0 -disabledwidth 0 -fill #c0c0c0 -width 2.0 -tags {Circle obj leftmost}
$c create oval 200.0 160.0 240.0 200.0 -disabledwidth 0 -fill #c0c0c0 -width 2.0 -tags {Circle obj middle}
$c create oval 280.0 120.0 320.0 160.0 -disabledwidth 0 -fill #c0c0c0 -width 2.0 -tags {Circle obj higher}
$c create oval 280.0 200.0 320.0 240.0 -disabledwidth 0 -fill #c0c0c0 -width 2.0 -tags {Circle obj lower}
$c create line 120.0 180.0 200.0 180.0 -arrow last -arrowshape {14 17 5} -joinstyle miter -width 2.0 -tags {Line obj utag18}
$c create line 240.0 180.0 280.0 140.0 -arrow last -arrowshape {14 17 5} -joinstyle miter -width 2.0 -tags {Line obj utag20}
$c create line 240.0 180.0 280.0 220.0 -arrow last -arrowshape {14 17 5} -joinstyle miter -width 2.0 -tags {Line obj utag21}

$c xview moveto 0.1
$c yview moveto 0.0


$c itemconfigure lower -fill white
"""

txt_style = """
ttk::style configure Japanese.TButton -font "helvetica 12"
"""


# Functions -- Setup

def setup():
    gui.mkcmd("ins_frame", lambda: insert(txt_frame))
    gui.mkcmd("ins_label", lambda: insert(txt_label))
    gui.mkcmd("ins_button", lambda: insert(txt_button))
    gui.mkcmd("ins_entry", lambda: insert(txt_entry))
    gui.mkcmd("ins_checkbutton", lambda: insert(txt_checkbutton))
    gui.mkcmd("ins_combobox", lambda: insert(txt_combobox))
    gui.mkcmd("ins_tree", lambda: insert(txt_tree))
    gui.mkcmd("ins_text", lambda: insert(txt_text))
    gui.mkcmd("ins_canvas", lambda: insert(txt_canvas))
    gui.mkcmd("ins_toprelief", lambda: insert(txt_toprelief))
    gui.mkcmd("ins_basicsetup", lambda: insert(txt_basicsetup))
    gui.mkcmd("ins_example", lambda: insert(txt_example))
    gui.mkcmd("ins_example2", lambda: insert(txt_example2))
    gui.mkcmd("ins_example3", lambda: insert(txt_example3))
    gui.mkcmd("ins_style", lambda: insert(txt_style))

def open_up():
    gui.toplevel_unique(".editor", "Tk Live Editor")
    gui.tclexec(tcl_code)


# Functions -- Insertions

def insert(s):
    gui.poke("tmp", s)
    gui.tclexec(".editor.f.doc insert insert $tmp")


# Periodic Updates (every 100ms)

last_time = [None]

prep_tcl = """
destroy .editor.f.cage.top
ttk::frame .editor.f.cage.top
grid .editor.f.cage.top -row 0 -column 0
"""


def update():
    gui.cue(".editor.f.doc")
    code = gui.text_get()
    if code == last_time[0]:
        return
    else:
        last_time[0] = code
    gui.poke("top", ".editor.f.cage.top")
    gui.tclexec(prep_tcl)
    try:
        gui.tclexec(code)
        gui.cue(".editor.f.out")
        gui.text_set("OK")
    except:
        gui.cue(".editor.f.out")
        gui.text_set(repr(sys.exc_info()))
