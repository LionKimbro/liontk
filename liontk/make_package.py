"""make_package.py  -- make the liontk package, available for distribution

This code was only made to function from the liontk/ directory.


UPDATE:
  This does not presently (2022-01-03) work, in this directory,
  because I've changed the project to be package based, rather than
  module based.  It'll need to be adapted if it is going to be made to
  work with packaging in mind.


This was constructed by working through:

  https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""

import shutil
import webbrowser
from pathlib import Path


PATH="PATH"
TEST="TEST"

DELETE = "DELETE"
CREATETEST = "CREATETEST"
CREATEREAL = "CREATEREAL"
WEB = "WEB"
CLEAN = "CLEAN"
QUIT = "QUIT"


g = {PATH: None,  # Path object (or None); set by mkdir(p, stick=True)
     TEST: False}  # true in TEST generation mode


url_packaging_projects = "https://packaging.python.org/en/latest/tutorials/packaging-projects/"

pyproject_toml = """
[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
""".strip()+"\n"


readme_md = """
This Python package provides an alternative approach to working with Tcl/Tk GUI code from Python.  It makes use of tkinter to communicate with Tcl/Tk, but does not otherwise use the class wrappers provided by tkinter.

It is not presently documented, but there are [hints on how to use it available in the repository's notes.txt file.](https://raw.githubusercontent.com/LionKimbro/liontk/main/liontk/notes.txt)
"""

setup_cfg = """
[metadata]
name = liontk
version = 2022.1.22
author = Lion Kimbro
author_email = lionkimbro@gmail.com
description = a Python Tcl/TK GUI system that emphasizes direct direct use of tcl
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/LionKimbro/liontk
project_urls =
    Source Folder on Github = https://github.com/LionKimbro/liontk/tree/main/liontk
    Bug Tracker = https://github.com/LionKimbro/liontk/issues
classifiers =
    Development Status :: 2 - Pre-Alpha
    Programming Language :: Python :: 3
    Programming Language :: Tcl
    Intended Audience :: Developers
    License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent
    Topic :: Software Development :: User Interfaces

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.6

[options.packages.find]
where = src
""".strip()+"\n"


def username_patch(s):
    def patched(ln):
        if ln.startswith("name = "):
            return ln+"-lionkimbro"
        else:
            return ln
    return "\n".join([patched(ln) for ln in setup_cfg.splitlines()])


notice_test = """
CREATED package/ directory;

Now, build the package:

  cd package/
  python -m build
                   * if this doesn't work,
                     python -m pip install --upgrade build

And then to upload to the TEST REPOSITORY,

  python -m twine upload --repository testpypi dist/*

  [username:] __token__
  [password:] pypi-__token__
  (see link below for information on aquiring a token)

Review web page at:

    https://test.pypi.org/project/liontk-lionkimbro

Review installation via:

  python -m pip install --index-url https://test.pypi.org/simple/ --no-deps liontk-lionkimbro

FOR MORE INFORMATION, SEE:

  https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""

notice_real = """
CREATED package/ directory;

Now, build the package:

  cd package/
  python -m build

/!\\ And then to upload to the REAL REPOSITORY, /!\\

  python -m twine upload dist/*

  [username:] __token__
  [password:] pypi-__token__
  (see link below for information on aquiring a token)

Review web page at:

    https://pypi.org/project/liontk  [I THINK!!]

Review installation via:

  python -m pip install liontk
"""


def mkdir(relpath, stick=False):
    p = Path(relpath)
    p.mkdir(parents=False, exist_ok=False)
    if stick:
        g[PATH] = p


def copyin(fname, src=None, srcdir=None):
    """Copy file from local dir into g[PATH]
    
    src: an over-ride source (NOT the given fname, from the immediate directory)

    fname  -- the name of the file to transfer
    src  -- a mask on the name of the file to transfer (local)
    srcdir  -- a specific directory to read the source from
    """
    if src is None:
        src = fname
    if srcdir is None:
        srcdir = Path(".")
    else:
        srcdir = Path(srcdir)
    shutil.copy(srcdir / src, g[PATH] / fname)


def writein(fname, content):
    """Write a file into g[PATH]."""
    f = (g[PATH] / fname).open("w", encoding="utf-8")
    f.write(content)
    f.close()


def touch(fname):
    """Create file with no contents.
    
    Used to create the __init__.py file.
    """
    (g[PATH] / fname).touch()


def make_directory_layout():
    """Create the directory layout for the package.
    
    Reversed with destroy_directory_layout.
    
    package/  -- equivalent "packaging_tutorial" in the tutorial
      src/
        liontk/
          symbols.py
          init.py
          tcltalk.py
          gui.py
    """
    mkdir("package", stick=True)  # equivalent "packaging_tutorial" in tutorial
    writein("pyproject.toml", pyproject_toml)
    writein("README.md", readme_md)
    if not g[TEST]:
        writein("setup.cfg", setup_cfg)
    else:
        writein("setup.cfg", username_patch(setup_cfg))
    mkdir("package/src")
    mkdir("package/src/liontk", stick=True)
    for fname in ["symbols.py",
                  "init.py",
                  "tcltalk.py",
                  "gui.py",
                  "__init__.py"]:
        copyin(fname, srcdir="liontk")
    touch("__init__.py")
    copyin("LICENSE", "../LICENSE")


def destroy_directory_layout():
    """Inverse of make_directory_layout.
    
    Destroys all contents within the constructed directory layout.
    """
    shutil.rmtree("package")

def destroy_cachedir():
    """Destroy the liontk/__pycache__/ that pops up."""
    try:
        shutil.rmtree("liontk/__pycache__")
        print("destroyed liontk/__pycache__")
    except:
        print("(already cleaned liontk/__pycache__)")


def menu_001():
    while True:
        print()
        print()
        print("  1.  DELETE package/ directory")
        print("  2.  CREATE package/ directory [TEST]")
        print("  3.  CREATE package/ directory [REAL]")
        print("  7.  OPEN WEBSITE")
        print("  8.  CLEAN environment")
        print("  9.  QUIT")
        print()
        print("> ", end="")
        result = input().upper()
        print()
        print()
        if result in {"1", "DEL", "DELETE", "RM", "ERASE"}:
            return DELETE
        elif result in {"2", "TEST"}:
            return CREATETEST
        elif result in {"3", "REAL"}:
            return CREATEREAL
        elif result in {"7", "WEB", "URL", "WEBSITE", "HELP"}:
            return WEB
        elif result in {"8", "CLEAN"}:
            return CLEAN
        elif result in {"9", "Q", "X", "QUIT", "EXIT", "XIT"}:
            return QUIT
        else:
            print("Not recognized: ", result)

def tell_making_directory():
    print("creating directory layout",
          "[TEST]" if g[TEST] else "[REAL]")
    try:
        make_directory_layout()
        print("directory layout created")
        print("notice:")
        print("-"*70)
        if g[TEST]:
            print(notice_test)
        else:
            print(notice_real)
        print("-"*70)
    except FileExistsError:
        print("<already created>")

if __name__ == "__main__":
    result = None
    while result != QUIT:
        result = menu_001()
        if result == DELETE:
            print("destroying older layout")
            try:
                destroy_directory_layout()
            except FileNotFoundError:
                print("<not found>")
            print("older layout destroyed")
        elif result == CREATETEST:
            g[TEST] = True
            tell_making_directory()
        elif result == CREATEREAL:
            g[TEST] = False
            tell_making_directory()
        elif result == WEB:
            webbrowser.open(url_packaging_projects)
        elif result == CLEAN:
            destroy_cachedir()

