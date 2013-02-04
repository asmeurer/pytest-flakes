pytest-flakes
=============

py.test plugin for efficiently checking python source with pyflakes.


Usage
-----

install via::

    pip install pytest-flakes

if you then type::

    py.test --flakes

every file ending in ``.py`` will be discovered and run through pyflakes,
starting from the command line arguments.


Configuring pyflakes options per project and file
-------------------------------------------------

You may configure pyflakes-checking options for your project
by adding an ``flakes-ignore`` entry to your ``setup.cfg``
or ``setup.cfg`` file like this::

    # content of setup.cfg
    [pytest]
    flakes-ignore = UnusedImport

This would globally prevent complaints about two whitespace issues.
Rerunning with the above example will now look better::

    $ py.test -q --flakes
    collecting ... collected 1 items
    .
    1 passed in 0.01 seconds

If you have some files where you want to specifically ignore
some errors or warnings you can start a flakes-ignore line with
a glob-pattern and a space-separated list of codes::

    # content of setup.cfg
    [pytest]
    flakes-ignore =
        *.py UnusedImport
        doc/conf.py ALL


Running pyflakes checks and no other tests
------------------------------------------

You can also restrict your test run to only perform "flakes" tests
and not any other tests by typing::

    py.test --flakes -k flakes

This will only run tests that are marked with the "flakes" keyword
which is added for the flakes test items added by this plugin.


Notes
-----

The repository of this plugin is at https://github.com/fschulze/pytest-flakes

For more info on py.test see http://pytest.org

The code is partially based on Ronny Pfannschmidt's pytest-codecheckers plugin
and Holger Krekel's pytest-pep8.
