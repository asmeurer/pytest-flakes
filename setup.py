from setuptools import setup

setup(
    name='pytest-flakes',
    description='pytest plugin to check source code with pyflakes',
    long_description=open("README.rst").read(),
    license="MIT license",
    version='4.0.5',
    author='Florian Schulze, Holger Krekel and Ronny Pfannschmidt',
    url='https://github.com/asmeurer/pytest-flakes',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Testing',
    ],
    py_modules=['pytest_flakes'],
    entry_points={'pytest11': ['flakes = pytest_flakes']},
    install_requires=['pytest>=5', 'pyflakes'])
