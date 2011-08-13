#!/usr/bin/env python

from setuptools import setup

setup(name='conqueue',
    version='0.1',
    description='conqueue is a queue manager library built on the top of redis.',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    url='http://github.com/emre/conqueue',
    package_dir={'': '.'},
    packages = ["conqueue", "conqueue.lib"],
)

