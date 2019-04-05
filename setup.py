"""Setup script for setuptools.
Also installs included versions of third party libraries, if those libraries
are not already installed.
"""
from __future__ import print_function

import sys

from setuptools import find_packages
from setuptools import setup

import hangoutstools


if (3, 1) <= sys.version_info < (3, 4):
    print('hangoutstools requires python3 version >= 3.4.', file=sys.stderr)
    sys.exit(1)

install_requires = [
    'validators>=0.12.4',
]

long_desc = """
hangoutstools provides message helpers for Google Hangouts Chat
"""

version = hangoutstools.__version__

setup(
    name='hangoutstools',
    version=version,
    description='Google hangouts chat message helpers',
    long_description=long_desc,
    author='Croud Ltd',
    author_email='jscrobinson@gmail.com',
    url='http://github.com/CroudTech/python-module-hangouts-chat-tools/',
    install_requires=install_requires,
    packages=find_packages(exclude=('tests*',)),
    license='Apache 2.0',
    keywords='google hangouts chat messages',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
    ],
)