import sys


pytest_plugins = "pytester",


def test_unused_import(testdir):
    testdir.makepyfile("""
import sys
""")
    result = testdir.runpytest("--flakes")
    assert "'sys' imported but unused" in result.stdout.str()
    assert 'passed' not in result.stdout.str()


def test_syntax_error(testdir):
    testdir.makeini("""
[pytest]
python_files=check_*.py
""")
    testdir.makepyfile("""
for x in []
    pass
""")
    result = testdir.runpytest("--flakes", "--ignore", testdir.tmpdir)
    if sys.version_info >= (3, 10):
        assert "1: expected ':'" in result.stdout.str()
    else:
        assert "1: invalid syntax" in result.stdout.str()
    assert 'passed' not in result.stdout.str()


def test_noqa(testdir):
    testdir.makeini("""
[pytest]
python_files=check_*.py
""")
    testdir.makepyfile("""
import sys # noqa
import os
foo # pragma: no flakes
bar
""")
    result = testdir.runpytest("--flakes")
    assert "UnusedImport\n'sys' imported but unused" not in result.stdout.str()
    assert "UnusedImport\n'os' imported but unused" in result.stdout.str()
    assert "UndefinedName\nundefined name 'foo'" not in result.stdout.str()
    assert "UndefinedName\nundefined name 'bar'" in result.stdout.str()
    assert 'passed' not in result.stdout.str()


def test_pep263(testdir):
    testdir.makepyfile(b'\n# encoding=utf-8\n\nsnowman = "\xe2\x98\x83"\n'.decode("utf-8"))
    result = testdir.runpytest("--flakes")
    assert '1 passed in' in result.stdout.str()


def test_non_py_ext(testdir):
    testdir.makefile('', '#!/usr/bin/env python', 'import sys')
    result = testdir.runpytest('--flakes')
    assert "UnusedImport\n'sys' imported but unused" in result.stdout.str()
    assert 'passed' not in result.stdout.str()


def test_flakesignore(testdir):
    testdir.makeini("""
[pytest]
flakes-ignore = ImportStarUsed
""")
    testdir.makepyfile("""
from os import *
""")
    result = testdir.runpytest("--flakes")
    assert "ignoring ImportStarUsed" in result.stdout.str()
    assert "1: ImportStarUsed" not in result.stdout.str()
    assert 'passed' not in result.stdout.str()
