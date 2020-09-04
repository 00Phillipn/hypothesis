# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2020 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

"""Try running `hypothesis write ...` on all available modules.

Prints a list of module names which caused some kind of internal error.

The idea here is to check that we at least don't crash on anything that
people actually ship, or at least only on the cases we know and don't
really care about - there are a lot of strange things in a python install.
Some have import-time side effects or errors so we skip them; others
just have such weird semantics that we don't _want_ to support them.
"""

import distutils.sysconfig as sysconfig
import multiprocessing
import os
import subprocess

skip = (
    "idlelib curses antigravity pip prompt_toolkit IPython .popen_ django. .test. "
    "execnet.script lib2to3.pgen2.conv tests. Cython. ~ - ._ libcst.codemod. "
    "modernize flask. sphinx. pyasn1 dbm.ndbm doctest"
).split()


def getmodules():
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    for top, _, files in os.walk(std_lib):
        for nm in files:
            if nm.endswith(".py") and nm not in ("__init__.py", "__main__.py"):
                modname = (
                    os.path.join(top, nm)[len(std_lib) + 1 : -3]
                    .replace(os.sep, ".")
                    .replace("site-packages.", "")
                )
                if not any(bad in modname for bad in skip):
                    yield modname


def write_for(mod):
    try:
        subprocess.run(
            ["hypothesis", "write", mod],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            universal_newlines=True,
        )
    except subprocess.SubprocessError as e:
        # Only report the error if we could load _but not process_ the module
        if (
            "Error: Found the '" not in e.stderr
            and "Error: Failed to import" not in e.stderr
        ):
            return mod


if __name__ == "__main__":
    print("# prints the names of modules for which `hypothesis write` errors out")
    with multiprocessing.Pool() as pool:
        for name in pool.imap(write_for, getmodules()):
            if name is not None:
                print(name, flush=True)
