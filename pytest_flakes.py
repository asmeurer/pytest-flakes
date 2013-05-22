from pyflakes.checker import Binding, Assignment, Checker
import _ast
import re
import pytest


def assignment_monkeypatched_init(self, name, source):
    Binding.__init__(self, name, source)
    if name == '__tracebackhide__':
        self.used = True

Assignment.__init__ = assignment_monkeypatched_init


HISTKEY = "flakes/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--flakes', action='store_true',
        help="run pyflakes on .py files")
    parser.addini("flakes-ignore", type="linelist",
        help="each line specifies a glob pattern and whitespace "
             "separated pyflakes errors which will be ignored, "
             "example: *.py UnusedImport")


def pytest_sessionstart(session):
    config = session.config
    if config.option.flakes:
        config._flakesignore = Ignorer(config.getini("flakes-ignore"))
        config._flakesmtimes = config.cache.get(HISTKEY, {})


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.flakes and path.ext == '.py':
        flakesignore = config._flakesignore(path)
        if flakesignore is not None:
            return FlakesItem(path, parent, flakesignore)


def pytest_sessionfinish(session):
    config = session.config
    if hasattr(config, "_flakesmtimes"):
        config.cache.set(HISTKEY, config._flakesmtimes)


class FlakesError(Exception):
    """ indicates an error during pyflakes checks. """


class FlakesItem(pytest.Item, pytest.File):

    def __init__(self, path, parent, flakesignore):
        super(FlakesItem, self).__init__(path, parent)
        self.keywords["flakes"] = True
        self.flakesignore = flakesignore

    def setup(self):
        flakesmtimes = self.config._flakesmtimes
        self._flakesmtime = self.fspath.mtime()
        old = flakesmtimes.get(str(self.fspath), 0)
        if old == (self._flakesmtime, self.flakesignore):
            pytest.skip("file(s) previously passed pyflakes checks")

    def runtest(self):
        found_errors, out = check_file(self.fspath, self.flakesignore)
        if found_errors:
            raise FlakesError("\n".join(out))
        # update mtime only if test passed
        # otherwise failures would not be re-run next time
        self.config._flakesmtimes[str(self.fspath)] = (self._flakesmtime, self.flakesignore)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(FlakesError):
            return excinfo.value.args[0]
        return super(FlakesItem, self).repr_failure(excinfo)

    def reportinfo(self):
        if self.flakesignore:
            ignores = "(ignoring %s)" % " ".join(self.flakesignore)
        else:
            ignores = ""
        return (self.fspath, -1, "pyflakes-check%s" % ignores)


class Ignorer:
    def __init__(self, ignorelines, coderex=re.compile("[EW]\d\d\d")):
        self.ignores = ignores = []
        for line in ignorelines:
            i = line.find("#")
            if i != -1:
                line = line[:i]
            try:
                glob, ign = line.split(None, 1)
            except ValueError:
                glob, ign = None, line
            if glob and coderex.match(glob):
                glob, ign = None, line
            ign = ign.split()
            if "ALL" in ign:
                ign = None
            ignores.append((glob, ign))

    def __call__(self, path):
        l = set()
        for (glob, ignlist) in self.ignores:
            if not glob or path.fnmatch(glob):
                if ignlist is None:
                    return None
                l.update(set(ignlist))
        return l


def check_file(path, flakesignore):
    codeString = path.read()
    filename = unicode(path)
    errors = []
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError, value:
        (lineno, offset, text) = value.lineno, value.offset, value.text
        if text is None:
            errors.append("%s: problem decoding source" % filename)
        else:
            line = text.splitlines()[-1]

            if offset is not None:
                offset = offset - (len(text) - len(line))

            msg = '%s:%d: %s' % (filename, lineno, value.args[0])
            msg = "%s\n%s" % (msg, line)

            if offset is not None:
                msg = "%s\n%s" % (msg, "%s^" % (" " * offset))
            errors.append(msg)
        return 1, errors
    else:
        # Okay, it's syntactically valid.  Now check it.
        w = Checker(tree, filename)
        w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        lines = codeString.split('\n')
        for warning in w.messages:
            if warning.__class__.__name__ in flakesignore or lines[warning.lineno - 1].endswith('# noqa'):
                continue
            errors.append(
                '%s:%s: %s\n%s' % (
                    warning.filename,
                    warning.lineno,
                    warning.__class__.__name__,
                    warning.message % warning.message_args))
        return len(errors), errors
