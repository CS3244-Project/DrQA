import regex as re
import logging
import argparse
import json
import time
import os
import pickle

from multiprocessing import Pool as ProcessPool
from multiprocessing.util import Finalize
from functools import partial
from drqa import retriever, tokenizers
from drqa.retriever import utils

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s: [ %(message)s ]',
                            '%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', type=str, default=None)
    parser.add_argument('output', type=str, default=None)
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--doc-db', type=str, default=None,
                        help='Path to Document DB')
    args = parser.parse_args()

    # start time
    start = time.time()

    # read all the data and store it
    logger.info('Reading data ...')
    questions = []
    contexts = []
    with open(args.dataset, "rb") as f:
        questions, contexts, depts = pickle.load(f) 
    assert len(questions) ==  len(contexts) and len(questions) == len(depts)

    # get the closest docs for each question.
    logger.info('Initializing ranker...')
    ranker = retriever.get_class('tfidf')(tfidf_path=args.model, strict=False)

    dept2idx = {}
    idx2dept = {}

    for d in depts:
        if d not in dept2idx:
            idx = len(dept2idx)
            dept2idx[d] = idx
            idx2dept[idx] = d

    dept_dataset = []

    for i in range(len(contexts)):
        q_vec = ranker.text2spvec(questions[i])
        c_vec = ranker.text2spvec(contexts[i])
        dept_idx = dept2idx[depts[i]]
        dept_dataset.append([q_vec, dept_idx])
        dept_dataset.append([v_vec, dept_idx])

    with open(args.output, "rb") as f:
        pickle.dump(dept_dataset, f)
