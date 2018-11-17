#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Interactive mode for the tfidf DrQA retriever module."""

import argparse
import code # to facilitate read-eval-print loops (a.k.a. interactive interpreter prompt)
import prettytable # to print ASCII table
import logging
from drqa import retriever # based on drqa/retriever

prepare the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default=None) # specify the retriever model
args = parser.parse_args()

logger.info('Initializing ranker...')
ranker = retriever.get_class('tfidf')(tfidf_path=args.model) # TfidfDocRanker of the specified model


# ------------------------------------------------------------------------------
# Drop in to interactive
# ------------------------------------------------------------------------------


def process(query, k=1): # k specifies how many docs to display starting from the highest rank (rank 1)
    doc_names, doc_scores = ranker.closest_docs(query, k) # find documents that is the closest with the queries (in TFIDF weighted word vector space)
    table = prettytable.PrettyTable(
        ['Rank', 'Doc Id', 'Doc Score']
    )
    for i in range(len(doc_names)):
        table.add_row([i + 1, doc_names[i], '%.5g' % doc_scores[i]])
    print(table)

    # The result is something like this
    #
    # +------+-------------------------------+-----------+
    # | Rank |             Doc Id            | Doc Score |
    # +------+-------------------------------+-----------+
    # |  1   |       Question answering      |   327.89  |
    # |  2   |       Watson (computer)       |   217.26  |
    # |  3   |          Eric Nyberg          |   214.36  |
    # |  4   |   Social information seeking  |   212.63  |
    # |  5   | Language Computer Corporation |   184.64  |
    # +------+-------------------------------+-----------+

banner = """
Interactive TF-IDF DrQA Retriever
>> process(question, k=1)
>> usage()
"""


def usage():
    print(banner)

# start the interactive prompt
# locals() is a Python built-in function
# locals(): Update and return a dictionary representing the current local symbol table.
code.interact(banner=banner, local=locals())
