from setuptools import setup

setup(
    name='pytest-flakes',
    description='pytest plugin to check source code with pyflakes',
    long_description=open("README.rst").read(),
    version='0.2',
    author='Florian Schulze, Holger Krekel and Ronny Pfannschmidt',
    author_email='florian.schulze@gmx.net',
    url='https://github.com/fschulze/pytest-flakes',
    py_modules=['pytest_flakes'],
    entry_points={'pytest11': ['flakes = pytest_flakes']},
    install_requires=['pytest-cache', 'pytest>=2.3.dev14', 'pyflakes'])
