"""Line Parsing"""


from symbols import *


g = {LN: None,  # working memory 
     LNNO: None,
     BODY: None,
     FN: None}  # call-back fn, per line

parts = {}  # Parts of a line


def ln_split_parts():  # adapted from snippets: SPRT
    s = g[LN]
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
    parts.clear()
    parts.update(D)


def has(k, i):
    """Return whether there's an i'th item for key k in parts."""
    return i < len(parts[k])

def val(k, i):
    """Return the i'th item for key k in PARTS."""
    return parts[k][i]


def reset():
    g.update({
        LN: None,
        LNNO: None,
        BODY: None,
        FN: None})

def parse(s, fn):
    reset()
    g[BODY], g[FN] = s, fn
    for g[LNNO], g[LN] in enumerate(s.split("\n")):
        parse_ln()

def parse_ln():
    if not g[LN].strip():
        return
    else:
        ln_split_parts()
        g[FN]()

