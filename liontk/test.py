
import lsf
import liontk

from liontk.symbols import *


editor_code = """
ttk::panedwindow .editor.p -orient horizontal
ttk::frame .editor.p.l -width 300 -height 1000 -padding "5 5 0 5"
ttk::treeview .editor.p.l.tree -selectmode browse -yscrollcommand ".editor.p.l.s set"
ttk::scrollbar .editor.p.l.s -orient vertical -command ".editor.p.l.tree yview"
ttk::frame .editor.p.r -width 700 -height 1000
ttk::frame .editor.p.r.top -padding "0 5 5 0"
ttk::label .editor.p.r.top.title_lbl -text "title:"
ttk::entry .editor.p.r.top.ttl -width 80
ttk::label .editor.p.r.top.tell_node -text "node: n343"
ttk::label .editor.p.r.top.tell_parent -text "parent: n310"
ttk::label .editor.p.r.top.tell_children -text "children: n334 n385 n100"
ttk::frame .editor.p.r.middle -padding "0 5 5 0"
ttk::treeview .editor.p.r.middle.otherkeys -selectmode browse -yscrollcommand ".editor.p.r.middle.s set"
ttk::scrollbar .editor.p.r.middle.s -orient vertical -command ".editor.p.r.middle.otherkeys yview"
ttk::frame .editor.p.r.bottom -padding "0 5 5 5"
tk::text .editor.p.r.bottom.text -width 80 -height 40 -yscrollcommand ".editor.p.r.bottom.s set"
ttk::scrollbar .editor.p.r.bottom.s -orient vertical -command ".editor.p.r.bottom.text yview"

.editor.p add .editor.p.l
.editor.p add .editor.p.r


grid rowconfigure .editor 0 -weight 1
grid columnconfigure .editor 0 -weight 1

grid .editor.p -column 0 -row 0 -sticky {nsew}

grid rowconfigure .editor.p 0 -weight 1
grid columnconfigure .editor.p 0 -weight 0
grid columnconfigure .editor.p 1 -weight 1


# grid .editor.p.l -row 0 -column 0 -sticky {nsew}
# grid .editor.p.r -row 0 -column 1 -sticky {nsew}

grid rowconfigure .editor.p.l 0 -weight 1
grid columnconfigure .editor.p.l 0 -weight 1
grid columnconfigure .editor.p.l 1 -weight 0

grid rowconfigure .editor.p.r 0 -weight 0
grid rowconfigure .editor.p.r 1 -weight 0
grid rowconfigure .editor.p.r 2 -weight 1
grid columnconfigure .editor.p.r 0 -weight 1


grid .editor.p.l.tree -row 0 -column 0 -sticky nsew
grid .editor.p.l.s -row 0 -column 1 -sticky nsw

grid .editor.p.r.top -row 0 -column 0 -sticky we
grid .editor.p.r.middle -row 1 -column 0 -sticky w
grid .editor.p.r.bottom -row 2 -column 0 -sticky nsew

grid columnconfigure .editor.p.r.top 0 -weight 0
grid columnconfigure .editor.p.r.top 1 -weight 1
grid rowconfigure .editor.p.r.top 1 -weight 0

grid columnconfigure .editor.p.r.bottom 0 -weight 1
grid columnconfigure .editor.p.r.bottom 1 -weight 0
grid rowconfigure .editor.p.r.bottom 0 -weight 1

grid .editor.p.r.top.title_lbl -row 0 -column 0 -sticky w
grid .editor.p.r.top.ttl -row 0 -column 1 -sticky we
grid .editor.p.r.top.tell_node -row 1 -column 0 -rowspan 1 -columnspan 2 -sticky w
grid .editor.p.r.top.tell_parent -row 2 -column 0 -rowspan 1 -columnspan 2 -sticky w
grid .editor.p.r.top.tell_children -row 3 -column 0 -rowspan 1 -columnspan 2 -sticky w

grid .editor.p.r.middle.otherkeys -row 0 -column 0
grid .editor.p.r.middle.s -row 0 -column 1

grid .editor.p.r.bottom.text -row 0 -column 0 -sticky nsew
grid .editor.p.r.bottom.s -row 0 -column 1 -sticky nsw
"""

# local symbols

NEXTID = "NEXTID"

VIEWING = "VIEWING"

ID = "ID"
TITLE = "TITLE"
TEXT = "TEXT"


# globals

g = {NEXTID: 0,  # the next node ID# to assign
     VIEWING: None}  # the node ID that is being viewed presently, or None

def nextid(): g[NEXTID] += 1; return g[NEXTID]-1


# globals: nodes
#
# nodes data format:
#   ID: str ("n" + unique id# string, starting from 0) -- must be unique to the file; will be given to key "lsfid" in the LSF file
#   TITLE: str (no newline) -- will be used in LSF file, as the title (will not be a LSF key)
#   TEXT: str (multiline) -- will be in the LSF file, as the content of the LSF entry
#
# parent-child relationships are NOT kept within the nodes

nodes = []

parent_child_relationships = {}  # {node-id: [parent-id, child-1-id, child-2-id, child-3-id, ...], ...}


# working with nodes

def new_node():
    """Create a new node, totally blank.  Assign it the next node id.
    
    WARNING:
    * will NOT have parent-child relationship, which is REQUIRED for all but root node
    * will NOT have an entry in parent_child_relationships, which is REQUIRED for ALL nodes
    
    DO NOT CALL DIRECTLY.
    Instead, call either:
    * create_root_node()  -- and there should be only ONE for the entire editor
    * create_node(parent)  -- create a new node, and add it as a child to this parent
                              (this is usually what you will want to call)
    """
    D = {ID: "n"+str(nextid()),
         TITLE: "",
         TEXT: ""}
    nodes.append(D)
    return D

def find_node(nodeid):
    """Find a node by its string identifier."""
    for D in nodes:
        if D[ID] == nodeid:
            return D
    return None


def parent_child(parent, kid):
    """Establish a parent-child relationship, given two nodes.
    
    Breaks previously existing bonds.
    """
    H, p, k = parent_child_relationships, parent[ID], kid[ID]
    p0 = H.get(k, [None])[0]
    if p0 is not None: del H[p0][H[p0].index(k, 1)]
    H.setdefault(k, [None])[0] = p
    if p is not None: H.setdefault(p, [None]).append(k)

def root_node():
    """Return the first node found that has no parent."""
    H = parent_child_relationships
    for D in nodes:
        if H[D[ID]][0] is None:
            return D
    return None

def create_root_node():
    """Create the root node.  Should only be ONE for the entire editor session."""
    D = new_node()
    D[TITLE] = "first node"
    D[TEXT] = "(first node's text)"
    parent_child_relationships[D[ID]] = [None]

def create_node(parent):
    """Create a new node, and register it as a child to this parent."""
    D = new_node()
    D[TITLE] = "created node"
    D[TEXT] = "(new node default text)"
    parent_child(parent, D)
    return D


# initing/loading/saving LSF files

def setup_nodes():
    nodes[:] = []
    g[NEXTID] = 0
    create_root_node()

def setup_test_nodes():
    root = root_node()
    for title in ["FIRST", "SECOND", "THIRD"]:
        D = create_node(root)
        D[TITLE] = title
    D2 = create_node(D)
    D2[TITLE] = "a child of the third"

def load_lsf(p):
    root = root_node()
    for LSFD in lsf.loadfile(p):
        D = create_node(root)
        D[TITLE] = LSFD["TITLE"] or "(root node)"
        D[TEXT] = LSFD["BODY"]


# maintaining GUI tree display

def setup_tree_select_tracking():
    liontk.tclexec("bind .editor.p.l.tree <<TreeviewSelect>> tree_select")
    liontk.mkcmd("tree_select", tree_select)

def rebuild_gui_tree():
    print("rebuilding gui tree...")
    liontk.tclexec(".editor.p.l.tree delete [.editor.p.l.tree children {}]")
    S = [root_node()[ID]]
    while S:
        D = find_node(S.pop(0))
        L = parent_child_relationships[D[ID]]
        my_id = D[ID]
        if L[0] is None:
            parent_id = "{}"
        else:
            parent_id = L[0]
        quoted_title = liontk.quote(D[TITLE])
        liontk.tclexec(f".editor.p.l.tree insert {parent_id} end -id {my_id} -text {quoted_title}")
        print("inserted", my_id)
        for child in L[1:]:
            S.append(child)

def tree_select():
    selected = liontk.tclexec(".editor.p.l.tree selection")
    D = find_node(selected)
    if D:
        g[VIEWING] = D[ID]
        update_info_display()
    else:
        g[VIEWING] = None
        update_info_display()


# maintain information display

def update_info_display():
    """Info is displayed based on g[VIEWING]."""
    if g[VIEWING] is None:
        liontk.cue(".editor.p.r.top.ttl")
        liontk.text_set("")
        liontk.text_ro()
        liontk.cue(".editor.p.r.top.tell_node")
        liontk.text_set("node: -")
        liontk.cue(".editor.p.r.top.tell_parent")
        liontk.text_set("parent: -")
        liontk.cue(".editor.p.r.top.tell_children")
        liontk.text_set("children: -")
        liontk.cue(".editor.p.r.bottom.text")
        liontk.text_set("")
        liontk.text_ro()
    else:
        D = find_node(g[VIEWING])
        L = parent_child_relationships[D[ID]]
        liontk.cue(".editor.p.r.top.ttl")
        liontk.text_set(D[TITLE])
        liontk.text_rw()
        liontk.cue(".editor.p.r.top.tell_node")
        liontk.text_set("node: " + D[ID])
        liontk.cue(".editor.p.r.top.tell_parent")
        liontk.text_set("parent: " + (L[0] or "(root)"))
        liontk.cue(".editor.p.r.top.tell_children")
        if L[1:]:
            liontk.text_set("children: " + " ".join(L[1:]))
        else:
            liontk.text_set("children: (no children)")
        liontk.cue(".editor.p.r.bottom.text")
        liontk.text_set(D[TEXT])
        liontk.text_rw()


# changes to the content text

def setup_text_modification_tracking():
    liontk.tclexec("bind .editor.p.r.bottom.text <<Modified>> text_modified")
    liontk.mkcmd("text_modified", text_modified)

def text_modified():
    # read the text
    liontk.cue(".editor.p.r.bottom.text")
    D = find_node(g[VIEWING])
    D[TEXT] = liontk.text_get()
    # reset the modification flag -- if you don't, you only get notified once
    liontk.tclexec(".editor.p.r.bottom.text edit modified 0")


# GUI

def setup_editor():
    liontk.toplevel_unique(".editor")
    liontk.title("LSF Tree Editor")
    liontk.tclexec(editor_code)
    setup_tree_select_tracking()
    setup_text_modification_tracking()

def setup():
    liontk.setup()
    setup_editor()
    setup_nodes()
    # Initial Clearing
    g[VIEWING] = None
    update_info_display()
    # Test setup:
    ## setup_test_nodes()
    load_lsf("F:/Dropbox/python/research.txt")
    liontk.gui.tasks.append(lambda: rebuild_gui_tree())

def run():
    liontk.loop()


if __name__ == "__main__":
    setup()
    run()
