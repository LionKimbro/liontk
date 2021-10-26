"""gridding.py  -- develop gridding page model

After the tree has been constructed (see: tree.py),
the user works on the placement of the nodes,
and the fine tuning of the placement of the nodes.


The user can perform three major operations:

  [Start Fresh] [Insert New] [Clear Obsolete]

These will blank the slate and populate the text area anew,
or insert only the new widgets not yet accounted for,
or clear away the old widgets that are no longer present in the tree.


However, the user has a list of widgets from the tree,
and now the user can specify the gridding placement.

  $top.f.b1 [0,0] <2x1> {nsew}

...means:

  grid $top.f.b1 -column 0 -row 0 -columnspan 2 -rowspan 1 -sticky nsew


Or more abbreivated:

  $top.f.b1 [0,0]

...means just:

  grid $top.f.b1 -column 0 -row 0


Here again, there is a generate() command, that gives the grid code
for the widgets.
"""

from symbols import *
import tree


g = {LN: None,  # present line, reading
     LNNO: None,  # present line number, reading
     NODE: None}  # the node working with

parts = {}  # parts read out from ln_split_parts


def has(k, i):
    """Return whether there is an i'th item for key k in PARTS."""
    return i < len(parts[k])

def val(k, i):
    """Return the i'th item for key k in PARTS."""
    return parts[k][i]


def first_word(ln):
    L = ln.split(None, 1)
    return L[0] if L else None

def widgets_in_order():
    """Identify the widgets, in their order, in the text area presently"""
    import gui
    return [first_word(ln) for ln in gui.text_get().split("\n")]


def populate():
    """Populate the gridding text area, (cued,) with the widget names."""
    import gui
    L = ["" if n is None else n[ID] for n in tree.grouped_order()]
    gui.text_set("\n".join(L)+"\n")


def node_locate():
    word = first_word(g[LN])
    for n in tree.all_nodes:
        if n[ID] == word:
            g[NODE] = n
            return True
    g[NODE] = None
    return False

def ln_split_parts():
    parts.clear()
    parts.update(tree.ln_split_parts_basic(g[LN]))

def parse_rowcol():
    if has('[]', 0):
        s = val('[]', 0)
        if "," in s:
            g[NODE][COL], g[NODE][ROW] = s.split(",", 1)

def parse_span():
    if has('<>', 0):
        s = val('<>', 0)
        if "," in s:
            g[NODE][COLSPAN], g[NODE][ROWSPAN] = s.split(",", 1)

def parse_sticky():
    if has('{}', 0):
        g[NODE][STICKY] = val('{}', 0)

def parse_line():
    if not g[LN].strip():
        return
    if not node_locate():
        return
    ln_split_parts()
    parse_rowcol()
    parse_span()
    parse_sticky()


def readlines(s):
    for g[LNNO], g[LN] in enumerate(s.split("\n")):
        parse_line()


#def generate():
#    import gui
#    L = []
#    for n in widgets_in_order():
        
