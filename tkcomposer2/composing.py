"""composing.py  -- composing tcl command strings incrementally"""


from symbols import *


words = []  # assembling words for the generator
L = []  # list of lines composed

g = None  # connect this up to a dictionary that features g[NODE]


def reset(D):
    global g
    del L[:]
    del words[:]
    g = D

def total_join():
    return "\n".join(L)+"\n"


def add_words(*L):
    words.extend(L)

def start_widget(constructor):
    add_words(constructor, g[NODE][ID])

def keep_quoted(option, key):
    import gui
    if g[NODE][key]:
        add_words(option, gui.quote(g[NODE][key]))

def keep_text():
    keep_quoted("-text", TEXT)

def keep(option, key, also=[]):
    if g[NODE][key]:
        add_words(option, g[NODE][key])
        words.extend(also)

def keep_wh():
    if g[NODE][ARG]:
        wh = g[NODE][ARG].split("x")
        if len(wh) >= 1:
            add_words("-width", wh[0])
        if len(wh) >= 2:
            add_words("-height", wh[1])

def end_sentence():
    try:
        L.append(" ".join(words) + (g[NODE][RAW] or ""))
    except:
        breakpoint()
    del words[:]
    return L[-1]


def blankline():
    L.append("")

