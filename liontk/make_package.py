"""make_package.py  -- make the liontk package, available for distribution

This code was only made to function from the liontk/ directory.


This was constructed by working through:

  https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""

import shutil
import webbrowser
from pathlib import Path


PATH="PATH"
TEST="TEST"

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


setup_cfg = """
[metadata]
name = liontk
version = 2022.1.3
author = Lion Kimbro
author_email = lionkimbro@gmail.com
description = a Python Tcl/TK GUI system that emphasizes direct direct use of tcl
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/LionKimbro/liontk
project_urls =
    Source Folder on Github = https://github.com/LionKimbro/liontk/liontk
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

# REMOVE LONG DESCRIPTION (NOT PROVIDING)
setup_cfg = "\n".join([ln for ln in setup_cfg.splitlines() if not ln.startswith("long_description")])


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


def copyin(fname, src=None):
    """Copy file from local dir into g[PATH]
    
    src: an over-ride source (NOT the given fname, from the immediate directory)
    """
    if src is None:
        src = fname
    shutil.copy(src, g[PATH] / fname)


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
    
    package/
      src/
        liontk/
          symbols.py
          init.py
          tcltalk.py
          gui.py
    """
    mkdir("package", stick=True)
    writein("pyproject.toml", pyproject_toml)
    if not g[TEST]:
        writein("setup.cfg", setup_cfg)
    else:
        writein("setup.cfg", username_patch(setup_cfg))
    mkdir("package/src")
    mkdir("package/src/liontk", stick=True)
    for fname in ["symbols.py",
                  "init.py",
                  "tcltalk.py",
                  "gui.py"]:
        copyin(fname)
    touch("__init__.py")
    copyin("LICENCE", "../LICENSE")


def destroy_directory_layout():
    """Inverse of make_directory_layout.
    
    Destroys all contents within the constructed directory layout.
    """
    shutil.rmtree("package")


def menu_001():
    while True:
        print()
        print()
        print("  1.  DELETE package/ directory")
        print("  2.  CREATE package/ directory [TEST]")
        print("  3.  CREATE package/ directory [REAL]")
        print("  7.  OPEN WEBSITE")
        print("  9.  QUIT")
        print()
        print("> ", end="")
        result = input().upper()
        print()
        print()
        if result in {"1", "DEL", "DELETE", "RM", "ERASE"}:
            return 1
        elif result in {"2", "TEST"}:
            return 2
        elif result in {"3", "REAL"}:
            return 3
        elif result in {"7", "WEB", "URL", "WEBSITE", "HELP"}:
            return 7
        elif result in {"9", "Q", "X", "QUIT", "EXIT", "XIT"}:
            return 9
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
    while result != 9:
        result = menu_001()
        if result == 1:
            print("destroying older layout")
            try:
                destroy_directory_layout()
            except FileNotFoundError:
                print("<not found>")
            print("older layout destroyed")
        elif result == 2:
            g[TEST] = True
            tell_making_directory()
        elif result == 3:
            g[TEST] = False
            tell_making_directory()
        elif result == 7:
            webbrowser.open(url_packaging_projects)

