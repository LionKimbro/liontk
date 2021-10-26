"""listdict.py  -- quickly search & filter a list of dictionaries

This is a general purpose system for navigating lists of dictionaries.
Original research notes can be found in Lion's research.txt file, LSF
entry #0K2.

I just find this more convenient than working with list
comprehensions, verifying that there is only one result, issuing sort
commands, and so on.

It's stateful and not thread safe, which I understand is not in style,
and people predict all kinds of doom; But, I haven't really
encountered the predicted demise, so I'm chalking that up to
superstition.


Import with:
-----------------------------------------------------------
from listdict import cue, val, val01, req, srt
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN

Example of use:

  cue(L)  # 1
  req("FOO", GR, 10)  # 2
  srt("NAME")  # 3
  show("NAME......... FOO.... BAR...............")  # 4

1. cue up a list of dictionaries, L

2. filter the list (doesn't replace L) to entries
   with a value for key "FOO" that is greater than 10;
   You could also express this as:
      req("FOO", lambda v: v > 10)
   ...or as:
      req(lambda D: D["FOO"] > 10)

3. sort the items by "NAME"

4. print the list of dictionary items;
   each item will have it's NAME, FOO, and BAR values printed out,
   as well as an index into the presently cue'd list
"""


EQ="EQ"  # equal to
NEQ="NEQ"  # not equal to
GT="GT"  # greater than
LT="LT"  # less than
GTE="GTE"  # greater than or equal to
LTE="LTE"  # less than or equal to
CONTAINS="CONTAINS"  # sub-collection contains item
NCONTAINS="NCONTAINS"  # sub-collection does NOT contain item
WITHIN="WITHIN"  # value within collection
NWITHIN="NWITHIN"  # value NOT within collection


fn_mappings = {EQ: lambda a,b: a==b,
               NEQ: lambda a,b: a!=b,
               GT: lambda a,b: a>b,
               LT: lambda a,b: a<b,
               GTE: lambda a,b: a>=b,
               LTE: lambda a,b: a<=b,
               CONTAINS: lambda a,b: b in a,
               NCONTAINS: lambda a,b: b not in a,
               WITHIN: lambda a,b: a in b,
               NWITHIN: lambda a,b: a not in b}


LIST = "LIST"

g = {LIST: []}


def cue(L):
    """Specify operations to continue on the specified list.
    
    This is always the first thing you call, when working on a list.
    """
    g[LIST] = L

def val():
    return g[LIST]

def length():
    return len(g[LIST])

def val1():
    """Require that there is one item, and return it."""
    if len(g[LIST]) == 1:
        return g[LIST][0]
    else:
        raise KeyError()

def val01(default=None):
    """Require that there is zero or one item, and return it."""
    if len(g[LIST]) == 0:
        return default
    elif len(g[LIST]) == 1:
        return g[LIST][0]
    else:
        raise KeyError


def req_fn(fn):
    cue([D for D in g[LIST] if fn(D)])

def req_fn2(k, fn):
    cue([D for D in g[LIST] if fn(D[k])])

def req_triple(k, relation, v):
    fn = fn_mappings[relation]
    cue([D for D in g[LIST] if fn(D[k], v)])

def req_matchall(D):
    for k,v in D.items():
        cue([D for D in g[LIST] if D[k] == v])

def req(*args, **kw):
    """Constrain down the list to meet some requirements.

    Does NOT modify the originating list, but does re-que to the
    resulting list.
    
    This can be called in several different ways.  In the example
    below, we'll cull the list down to those dictionaries that have
    D["x"] == 5.

    1. req(fn)              -- ex: req(lambda D: D["x"] == 5)
    2. req(k, fn)           -- ex: req("x", lambda x: x == 5)
    3. req(k, relation, v)  -- ex: req("x", EQ, 5)
    4. req(**kw)            -- ex: req(x=5)
    
    Or consider D["y"] > 10:

    1. req(fn)              -- ex: req(lambda D: D["y"] > 10)
    2. req(k, fn)           -- ex: req("y", lambda y: y > 10)
    3. req(k, relation, v)  -- ex: req("y", GT, 10)
    4. req(**kw)            -- CANNOT BE EXPRESSED;
                               this form can only be used for equality checks

    Or consider D["type"] == "foo" and D["name"] == "bar"

    0. (Python List Comp:)  -- ex: L = [D for D in L if D["type"] == "foo" and D["name"] == "bar"]
    1. req(fn)              -- ex: req(lambda D: D["type"] == "foo" and D["name"] == "bar")
    2. req(k, fn)           -- ex: req("type", lambda s: s=="foo")
                                   req("name", lambda s: s=="bar")
                                   (this form can only be used via serial calls)
    3. req(k, relation, v)  -- ex: req("type", EQ, "foo")
                                   req("name", EQ, "bar")
                                   (this form can only be used via serial calls)
    4. req(**kw)            -- ex: req(type="foo", name="bar")
    """
    if kw:
        req_matchall(kw)
    elif len(args) == 1:
        req_fn(*args)
    elif len(args) == 2:
        req_fn2(*args)
    elif len(args) == 3:
        req_triple(*args)
    else:
        raise TypeError


def srt(k, reverse=False):
    """Sort the list on a key.  WARNING: Operates in-place."""
    g[LIST].sort(key=lambda D: D[k], reverse=reverse)


def map(x):
    """Return the result of doing something to each list item.
    
    Note -- does NOT cue the result by default;
            wrap the call in cue(...) if you want to do that.
    
    map(fn)  --> returns result of applying fn to each item
    map(str) --> returns result of key lookup for each item
    """
    if isinstance(x, str):
        return [D[x] for D in g[LIST]]
    else:
        return [x(D) for D in g[LIST]]


def show(spec):
    """print dictionaries per a spec;
    
    example spec:
      "KEY1............. KEY2........................... KEY3......"
    
    based on snippets.py, entry DLPR: Dictionary List Print
    """
    print("NDX "+spec)
    specL = [(word.rstrip("."), len(word)) for word in spec.split()]
    for i, D in enumerate(g[LIST]):
        pieces = [str(D.get(key, "NONE")).ljust(length)[:length] for (key,length) in specL]
        print("{:>2}. ".format(i)+" ".join(pieces))
