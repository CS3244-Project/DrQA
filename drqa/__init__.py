#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
from pathlib import PosixPath # provides os.path functionality 
                              # on Unix and other POSIX compatible platforms.
                              # I think this is more for Windows

if sys.version_info < (3, 5):
    raise RuntimeError('DrQA supports Python 3.5 or higher.')

# path to the default trained model
DATA_DIR = (
    os.getenv('DRQA_DATA') or
    os.path.join(PosixPath(__file__).absolute().parents[1].as_posix(), 'data')
)

# TODO: Why?
from . import tokenizers
from . import reader
from . import retriever
from . import pipeline
