"""tree.py  -- develops abstract tree model


The "tree" is fairly complex;
Hence the need for the program in the first place.

It's specified in two places:
1. in the "Windows Tree" page's text panel,
2. in the "Gridding" page's text panel, -- with different keys

The authoritative definition for the tree is from the Windows Tree Panel.

Here's an example tree definition:


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


The depth of each window is specified by 2-space indentation.  The
type of the window is specified within brackets, defaulting to
"ttk::frame"

  (default)   ttk::frame
  [lf]        ttk::labelframe
  [lbl]       ttk::label
  [btn]       ttk::button
  [ent]       ttk::entry
  [chk]       ttk::checkbutton
  [lbox]      tk::listbox

If there is a text parameter for the type, it is specified in
quotation marks.

And if there is a variable, it is expressed within less than (<)
greater than (>) characters.  An optional initial value can be
specified following an internal colon (:) character.


The data for the tree is kept within an indexed tree like so:


"""


from symbols import *


g = {LN: "",  # working memory for line interpretation and manipulation
     LNNO: None,  # line number working on
     NODE: None,  # node presently constructing (via node_create)
     NEXTID: 1}

parts = {}  # parts read out from ln_split_parts

S = []  # stack of nodes at levels last seen

all_nodes = []  # list of all nodes, in order constructed

types_text = {
    FRAME: "ttk::frame",
    LABELFRAME: "ttk::labelframe",
    LABEL: "ttk::label",
    BUTTON: "ttk::button",
    ENTRY: "ttk::entry",
    CHECKBUTTON: "ttk::checkbutton",
    LISTBOX: "tk::listbox",
    TEXT: "tk::text",
    CANVAS: "tk::canvas",
    TREE: "ttk::treeview",
    SCROLLBAR: "ttk::scrollbar"
}

read_types = {
    None: FRAME,
    "f": FRAME,
    "lf": LABELFRAME,
    "lbl": LABEL,
    "btn": BUTTON,
    "ent": ENTRY,
    "chk": CHECKBUTTON,
    "lbox": LISTBOX,
    "txt": TEXT,
    "c": CANVAS,
    "tree": TREE,
    "-": SCROLLBAR,  # ARG: HORZ
    "|": SCROLLBAR  # ARG: VERT
}


def reset():
    g[LN] = None
    g[NODE] = None
    parts.clear()
    del S[:]
    all_nodes[:] = []
    g[NEXTID] = 1

def node_create():
    """Create a new, blank node."""
    g[NODE] = {  # these are listed in order of parsing
        LN: g[LN],
        LNNO: g[LNNO],
        DEPTH: None,      # int, levels deep
        PARENT: None,     # dict, for parent node of this node
        CHILDREN: [],     # list of dict, for child nodes of this node
        NAME: None,       # str, name of this window
        ID: None,         # str, full and unique name of this window
        TYPE: None,       # sym, node's type (FRAME, LABELFRAME, LABEL, BUTTON, ENTRY, CHECKBUTTON, LISTBOX)
        ARG: None,        # str, argument after node's type was specified (ex: [ent:4])
        TEXT: None,       # str, node's text content
        VAR: None,        # str, node's variable
        VARDEFAULT: None, # (val,) or None, a default value for the variable (note: (None,) means default is None, and None means no default)
        LASTNONSCROLLBAR: None,  # the specific non-scrollbar that this scrollbar modifies
        SCROLLBAR: {VERT: None, HORZ: None},  # specific scroll-bars that this modifies
        RAW: None,        # str, node's raw creation-line additions

        # -------------- gridding.py uses these:
        ROW: None,
        COL: None,
        ROWSPAN: None,
        COLSPAN: None,
        STICKY: None
    }
    all_nodes.append(g[NODE])

def toplevel_nodes():
    return [n for n in all_nodes if n[PARENT] is None]

def grouped_order():
    """Return the nodes in sets.
    
    The space between sets is noted with None.
    """
    L = []
    todo = []
    for n in toplevel_nodes():
        L.append(n)
        todo.append(n)
    if L:
        L.append(None)  # blank line
    while todo:
        n = todo.pop(0)
        L.extend(n[CHILDREN])
        if n[CHILDREN]:
            L.append(None)
            todo[:] = n[CHILDREN] + todo
    return L

def last_non_scrollbar():
    for n in reversed(all_nodes):
        if n[TYPE] != SCROLLBAR:
            return n
    return None


def ln_split_parts_basic(s):  # adapted from snippets: SPRT
    qmarks = '<> "" {} [] () 「」 『』'.split()
    D = {k: [] for k in qmarks}
    qmarks_open = {qm[0]: qm for qm in qmarks}
    qmarks_close = {qm[1]: qm for qm in qmarks}
    s_rstrip = s.rstrip()
    s = s_rstrip.lstrip()
    D[INDENT] = len(s_rstrip)-len(s)
    D[TEXT] = []
    state = TEXT
    escaping = False
    acc = []
    for ch in s:
        if escaping == True:
            acc.append(ch)
            escaping = False
        else:
            if ch == "\\":
                escaping = True
                continue  # jump back to the for ch...
            elif ((ch in qmarks_open and state == TEXT) or
                  (ch in qmarks_close and state == qmarks_close[ch])):
                x = "".join(acc).strip()
                if x or (state != TEXT):  # note empty entries for non-TEXT
                    D[state].append(x)
                del acc[:]
                state = qmarks_open[ch] if state == TEXT else TEXT
            else:
                acc.append(ch)
    if state == TEXT:
        x = "".join(acc).strip()
        if x:
            D[TEXT].append(x)
    return D

def ln_split_parts():
    parts.clear()
    parts.update(ln_split_parts_basic(g[LN]))


def parse_depth():
    """Parse out depth."""
    g[NODE][DEPTH] = parts[INDENT] // 2

def parse_parent():
    """Parse parent.

    Truncates S to the parents level, too.
    And then affixes myself.
    """
    n = g[NODE]
    if not S:
        n[PARENT] = None
        S.append(n)
    else:
        my_level = n[DEPTH]
        parent_level = my_level-1
        if parent_level < len(S):
            n[PARENT] = S[parent_level]
            n[PARENT][CHILDREN].append(n)
            del S[my_level:]
            S.append(g[NODE])

def has(k, i):
    """Return whether there is an i'th item for key k in PARTS."""
    return i < len(parts[k])

def val(k, i):
    """Return the i'th item for key k in PARTS."""
    return parts[k][i]


def assigned_name():
    n = g[NEXTID]
    g[NEXTID] += 1
    return "anon" + str(n)

def parse_name():
    """Parse out node name.
    
    Also calculates out ID.
    """
    n = g[NODE]
    if has(TEXT, 0):
        n[NAME] = val(TEXT, 0)  # first thing listed is the name
    else:
        n[NAME] = assigned_name()
    if n[PARENT] is not None:
        n[ID] = n[PARENT][ID] + "." + n[NAME]
    else:
        n[ID] = n[NAME]

def parse_type():
    """Parse out node type."""
    n = g[NODE]
    if not has("[]", 0):
        n[TYPE] = read_types.get(None)  # None HERE means "the default"
    else:
        s = val("[]", 0)
        if ":" in s:
            s, rest = s.split(":", 1)
            n[ARG] = rest
        n[TYPE] = read_types.get(s, None)  # None HERE means "unrecognized"
        if n[TYPE] == SCROLLBAR:
            if s == "|":
                n[TYPE] = SCROLLBAR
                n[ARG] = VERT
            if s == "-":
                n[TYPE] = SCROLLBAR
                n[ARG] = HORZ
            n0 = last_non_scrollbar()  # get the node that this scrollbar attaches to
            n[LASTNONSCROLLBAR] = n0  # that's the one I scroll
            n0[SCROLLBAR][n[ARG]] = n  # ...and it scrolls me

def parse_text():
    """Parse out text."""
    g[NODE][TEXT] = val('""', 0) if has('""', 0) else None

def parse_var():
    """Parse out variable."""
    if has('<>', 0):
        s = val('<>', 0)
        if ":" in s:
            s, rest = s.split(":", 1)
            g[NODE][VARDEFAULT] = (rest,) if rest else (None,)
        g[NODE][VAR] = s

def parse_raw():
    """Parse out raw additions."""
    if has('()', 0):
        g[NODE][RAW] = val('()', 0)

def parse_line():
    """Parse g[LN] for all details about g[NODE]."""
    if not g[LN].strip():
        return  # blank line; ignore
    node_create()
    ln_split_parts()
    parse_depth()
    parse_parent()
    parse_name()
    parse_type()
    parse_text()
    parse_var()
    parse_raw()
    if g[NODE][TEXT] and g[NODE][TYPE] == FRAME:  # convenience hack
        g[NODE][TYPE] = LABEL


def readlines(s):
    reset()
    for g[LNNO], g[LN] in enumerate(s.split("\n")):
        parse_line()


def populate_tree():
    """Populate the cue'd tree widget."""
    import gui
    store_open_closed()
    gui.tclexec("$w delete [$w children {}]")
    for n in all_nodes:
        gui.poke("tmpp", n[PARENT][ID] if n[PARENT] else "")  # parent
        gui.poke("tmpi", n[ID])  # ID
        gui.poke("tmpn", n[NAME])  # name
        gui.poke("tmpty", types_text[n[TYPE]] if n[TYPE] else "X")  # type
        gui.poke("tmpt", n[TEXT] or "-")  # text
        gui.poke("tmpv", n[VAR] or "-")  # variable
        try:
            gui.tclexec("$w insert $tmpp end -id $tmpi -text $tmpn -values [list $tmpty $tmpt $tmpv]")
        except:
            pass  # this can happen if it already exists
    restore_open_closed()
    mem_open.clear()


mem_open = {}  # memory of whether a given node was opened or closed in the GUI

def store_open_closed():
    import gui
    for n in all_nodes:
        gui.poke("tmpi", n[ID])
        if gui.tclexec("$w exists $tmpi") == "1":
            mem_open[n[ID]] = {"true": "1",
                               "1": "1",
                               "false": "0",
                               "0": "0"}[gui.tclexec("$w item $tmpi -open")]

def restore_open_closed():
    import gui
    for n in all_nodes:
        gui.poke("tmpi", n[ID])
        if n[ID] not in mem_open:
            gui.tclexec("$w item $tmpi -open 1")  # default to open!
        else:
            if gui.tclexec("$w exists $tmpi") == "1":
                gui.tclexec("$w item $tmpi -open "+mem_open[n[ID]])


def generate():
    import gui
    L = []
    for n in all_nodes:
        if n[TYPE] == FRAME:
            words = ["ttk::frame", n[ID]]
        elif n[TYPE] == LABELFRAME:
            words = ["ttk::labelframe", n[ID]]
            if n[TEXT]:
                words.extend(["-text", gui.quote(n[TEXT])])
        elif n[TYPE] == LABEL:
            words = ["ttk::label", n[ID]]
            if n[TEXT]:
                words.extend(["-text", gui.quote(n[TEXT])])
        elif n[TYPE] == BUTTON:
            words = ["ttk::button", n[ID]]
            if n[TEXT]:
                words.extend(["-text", gui.quote(n[TEXT])])
            if n[VAR]:
                words.extend(["-command", n[VAR]])
        elif n[TYPE] == ENTRY:
            words = ["ttk::entry", n[ID]]
            if n[ARG]:
                words.extend(["-width", n[ARG]])
            if n[VAR]:
                words.extend(["-textvariable", n[VAR]])
                # TODO: setting default values
        elif n[TYPE] == CHECKBUTTON:
            words = ["ttk::checkbutton", n[ID]]
            if n[TEXT]:
                words.extend(["-text", gui.quote(n[TEXT])])
            if n[VAR]:
                words.extend(["-variable", n[VAR], "-onvalue", "1"])
        elif n[TYPE] == LISTBOX:
            words = ["tk::listbox", n[ID]]
            if n[ARG]:
                multi = False
                if n[ARG][-1] == "*":
                    multi = True
                    n[ARG] = n[ARG][:-1]
                words.extend(["-height", n[ARG]])
                if multi:
                    words.extend(["-selectmode", "extended"])
                else:
                    words.extend(["-selectmode", "browse"])
            words.extend(["-exportselection", "0"])
        elif n[TYPE] == TEXT:
            words = ["tk::text", n[ID]]
            if n[ARG]:
                wh = n[ARG].split("x")
                if len(wh) >= 1:
                    words.extend(["-width", wh[0]])
                if len(wh) >= 2:
                    words.extend(["-height", wh[1]])
        elif n[TYPE] == CANVAS:
            words = ["tk::canvas", n[ID]]
            if n[ARG]:
                wh = n[ARG].split("x")
                if len(wh) >= 1:
                    words.extend(["-width", wh[0]])
                if len(wh) >= 2:
                    words.extend(["-height", wh[1]])
        elif n[TYPE] == TREE:
            words = ["ttk::treeview", n[ID]]
            if n[TEXT]:
                words.extend(["-columns", gui.quote(n[TEXT])])
            if n[ARG] == "*":
                words.extend(["-selectmode", "extended"])
            else:
                words.extend(["-selectmode", "browse"])
        elif n[TYPE] == SCROLLBAR:
            words = ["ttk::scrollbar", n[ID]]
            if n[ARG] == HORZ:
                cmd = gui.encase(n[LASTNONSCROLLBAR][ID] + " xview")
                words.extend(["-orient", "horizontal", "-command", cmd])
            else:
                cmd = gui.encase(n[LASTNONSCROLLBAR][ID] + " yview")
                words.extend(["-orient", "vertical", "-command", cmd])
        else:
            continue
        if n[SCROLLBAR][HORZ]:
            words.extend(["-xscrollcommand", gui.encase(n[SCROLLBAR][HORZ][ID] + " set")])
        elif n[SCROLLBAR][VERT]:
            words.extend(["-yscrollcommand", gui.encase(n[SCROLLBAR][VERT][ID] + " set")])
        # TODO: many other types, esp. TREE [tree] & TEXT [txt] & CANVAS [c], my favorites
        print(words)
        s = " ".join(words)
        if n[RAW]:
            s = s + " " + n[RAW]
        L.append(s)
    print("\n".join(L))

