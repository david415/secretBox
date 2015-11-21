#!/usr/bin/env python

from setuptools import setup

__version__ = '0.0.1'
__author__ = 'David Stainton'
__contact__ = 'dstainton415@gmail.com'
__url__ = 'https://github.com/david415/secretbox'
__license__ = 'GPL'
__copyright__ = 'Copyright 2015'

setup(
    name='secretBox',
    description='cli for using nacl secret-box',
    version = __version__,
    long_description = open('README.rst', 'r').read(),
    author = __author__,
    author_email = __contact__,
    url = __url__,
    license = __license__,
    install_requires=open('requirements.txt', 'rb').read().split(),
    packages=['secretBox'],
    scripts=['bin/secretbox']
)
