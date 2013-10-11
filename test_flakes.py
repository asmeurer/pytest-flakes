# coding=utf8
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
    result = testdir.runpytest("--flakes", "--ignore", testdir)
    assert "1: invalid syntax" in result.stdout.str()
    assert 'passed' not in result.stdout.str()
