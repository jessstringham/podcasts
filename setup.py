#!/usr/bin/python
import os
from setuptools import setup, find_packages

setup(
    name='podcaster',
    version='0.1',
    test_suite="tests",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data = {
        '': ['LICENSE', 'README.md5', 'RELEASE']
    },
)