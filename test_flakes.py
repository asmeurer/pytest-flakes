# coding=utf8
pytest_plugins = "pytester",


def test_unused_import(testdir):
    testdir.makepyfile("""
import sys
""")
    result = testdir.runpytest("--flakes")
    assert "'sys' imported but unused" in result.stdout.str()
    assert 'passed' not in result.stdout.str()
