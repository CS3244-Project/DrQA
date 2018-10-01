#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""A script to convert the default WebQuestions dataset to the format:

'{"question": "q1", "answer": ["a11", ..., "a1i"]}'
...
'{"question": "qN", "answer": ["aN1", ..., "aNi"]}'

"""

import argparse
import re # for regular expression operations
import json

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str) # file path to read the input from
parser.add_argument('output', type=str) # file path to write the output to
args = parser.parse_args()

# Read dataset
with open(args.input) as f:
    dataset = json.load(f) # takes in a file and returns python object

# Iterate and write question-answer pairs
with open(args.output, 'w') as f:
    for ex in dataset:
        question = ex['utterance']
        answer = ex['targetValue']
        answer = re.findall( # return a non-repeating list of strings that matches the pattern
            r'(?<=\(description )(.+?)(?=\) \(description|\)\)$)', answer
        )
        answer = [a.replace('"', '') for a in answer]
        f.write(json.dumps({'question': question, 'answer': answer})) # python object into json
        f.write('\n')
