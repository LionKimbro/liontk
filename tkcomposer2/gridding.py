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

import lineparsing
from lineparsing import has, val

import tree


g = {NODE: None}  # the node working with


def populate():
    """Populate the gridding text area, (cued,) with the widget names."""
    import gui
    L = ["" if n is None else n[ID] for n in tree.peers_order()]
    gui.text_set("\n".join(L)+"\n")


def node_locate():
    if has(TEXT, 0):
        word = val(TEXT, 0)
        for n in tree.all_nodes:
            if n[ID] == word:
                g[NODE] = n
                return True
    g[NODE] = None
    return False

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
    if not node_locate():
        return
    parse_rowcol()
    parse_span()
    parse_sticky()


def readlines(s):
    lineparsing.parse(s, parse_line)


# Generation

words = []  # assembling words for the generator

def add_words(*L):
    words.extend(L)

def keep(option, key):
    if g[NODE][key]:
        words.extend([option, g[NODE][key]])

def final_join():
    return " ".join(words)


def generate():
    import gui
    L = []
    for g[NODE] in tree.peers_order():
        if n is None:
            L.append("")
            continue
        add_words("grid", n[ID])
        keep("-row", ROW)
        keep("-column", COL)
        keep("-rowspan", ROWSPAN)
        keep("-columnspan", COLSPAN)
        keep("-sticky", STICKY)
        L.append(final_join())
    print()
    print("\n".join(L))

