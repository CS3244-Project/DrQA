#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup, find_packages
import sys

# with open('README.md') as f:
#     readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='drqa',
    version='0.1.0',
    description='Reading Wikipedia to Answer Open-Domain Questions',
<<<<<<< HEAD
    long_description=readme,
=======
    long_description=None,
>>>>>>> 6382a147c8f4eccd69d8434962f87a73f650ad1f
    license=license,
    python_requires='>=3.5',
    packages=find_packages(exclude=('data')),
    install_requires=reqs.strip().split('\n'),
)
