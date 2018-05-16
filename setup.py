from setuptools import setup

setup(
    name='pytest-flakes',
    description='pytest plugin to check source code with pyflakes',
    long_description=open("README.rst").read(),
    license="MIT license",
    version='3.0.0',
    author='Florian Schulze, Holger Krekel and Ronny Pfannschmidt',
    author_email='florian.schulze@gmx.net',
    url='https://github.com/fschulze/pytest-flakes',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
    ],
    py_modules=['pytest_flakes'],
    entry_points={'pytest11': ['flakes = pytest_flakes']},
    install_requires=['pytest-cache', 'pytest>=2.3.dev14', 'pyflakes'])
