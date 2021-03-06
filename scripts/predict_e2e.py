#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""A script to make and save model predictions on an input dataset."""

import os
import time
import torch
import argparse
import logging
import json

from tqdm import tqdm
from drqa.reader import Predictor

from multiprocessing import Pool as ProcessPool
from multiprocessing.util import Finalize
from functools import partial
from drqa import retriever, tokenizers
from drqa.retriever import utils

PROCESS_TOK = None
PROCESS_DB = None


def init(tokenizer_class, tokenizer_opts, db_class, db_opts):
    global PROCESS_TOK, PROCESS_DB
    PROCESS_TOK = tokenizer_class(**tokenizer_opts)
    Finalize(PROCESS_TOK, PROCESS_TOK.shutdown, exitpriority=100)
    PROCESS_DB = db_class(**db_opts)
    Finalize(PROCESS_DB, PROCESS_DB.close, exitpriority=100)    

def retrieve_documents(doc_infos):
    global PROCESS_DB, PROCESS_TOK
    doc_ids, doc_scores = doc_infos
    contexts = [] 
    for doc in doc_ids:
        contexts.append(PROCESS_DB.get_doc_text(doc))
    return contexts

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', type=str, default=None,
                        help='SQuAD-like dataset to evaluate on')
    parser.add_argument('--reader-model', type=str, default=None,
                        help='Path to reader model to use')
    parser.add_argument('--embedding-file', type=str, default=None,
                        help=('Expand dictionary to use all pretrained '
                              'embeddings in this file.'))
    parser.add_argument('--out-dir', type=str, default='/tmp',
                        help=('Directory to write prediction file to '
                              '(<dataset>-<model>.preds)'))
    parser.add_argument('--reader-tokenizer', type=str, default=None,
                        help=("String option specifying tokenizer type to use "
                              "(e.g. 'corenlp')"))
    parser.add_argument('--num-workers', type=int, default=None,
                        help='Number of CPU processes (for tokenizing, etc)')
    parser.add_argument('--no-cuda', action='store_true',
                        help='Use CPU only')
    parser.add_argument('--gpu', type=int, default=-1,
                        help='Specify GPU device id to use')
    parser.add_argument('--batch-size', type=int, default=128,
                        help='Example batching size')
    parser.add_argument('--top-n', type=int, default=1,
                        help='Store top N predicted spans per example')
    parser.add_argument('--official', action='store_true',
                        help='Only store single top span instead of top N list')

    parser.add_argument('--doc-db', type=str, default=None,
                            help='Path to Document DB')
    parser.add_argument('--retriever-model', type=str, default=None,
                        help='Path to retriever model to use') 
    parser.add_argument('--n-docs', type=int, default=5)
    parser.add_argument('--match', type=str, default='string',
                        choices=['regex', 'string'])
    parser.add_argument('--retriever-tokenizer', type=str, default='regexp')

    args = parser.parse_args()
    t0 = time.time()

    args.cuda = not args.no_cuda and torch.cuda.is_available()
    if args.cuda:
        torch.cuda.set_device(args.gpu)
        logger.info('CUDA enabled (GPU %d)' % args.gpu)
    else:
        logger.info('Running on CPU only.')

    predictor = Predictor(
        model=args.reader_model,
        tokenizer=args.reader_tokenizer,
        embedding_file=args.embedding_file,
        num_workers=args.num_workers,
    )
    if args.cuda:
        predictor.cuda()
    
    # ------------------------------------------------------------------------------
    # Collect questions from dataset
    # ------------------------------------------------------------------------------

    questions = []
    qids = []
    with open(args.dataset) as f:
        data = json.load(f)['data']
        for article in data:
            for paragraph in article['paragraphs']:
                for qa in paragraph['qas']:
                    qids.append(qa['id'])
                    questions.append(qa['question'])

    # ------------------------------------------------------------------------------
    # Retrieve most relevant documents from dataset
    # ------------------------------------------------------------------------------

    ranker = retriever.get_class('tfidf')(tfidf_path=args.retriever_model)
    retrieved_doc_ids = ranker.batch_closest_docs(
            questions, k=args.n_docs, num_workers=args.num_workers
        )
    

    # define processes
    tok_class = tokenizers.get_class(args.retriever_tokenizer)
    tok_opts = {}
    db_class = retriever.DocDB
    db_opts = {'db_path': args.doc_db}
    processes = ProcessPool(
        processes=args.num_workers,
        initializer=init,
        initargs=(tok_class, tok_opts, db_class, db_opts)
    )

    contexts = processes.map(retrieve_documents, retrieved_doc_ids)   
    examples = []
    for i, question in enumerate(questions):
        context = contexts[i][0] if len(contexts[i]) > 0 else "_"
        examples.append((context, question))

    # ------------------------------------------------------------------------------
    # Read in dataset and make predictions.
    # ------------------------------------------------------------------------------

    results = {}
    for i in tqdm(range(0, len(examples), args.batch_size)):
        predictions = predictor.predict_batch(
            examples[i:i + args.batch_size], top_n=args.top_n
        )
        for j in range(len(predictions)):
        # Official eval expects just a qid --> span
            if args.official:
                results[qids[i + j]] = predictions[j][0][0]

            # Otherwise we store top N and scores for debugging.
            else:
                results[qids[i + j]] = [(p[0], float(p[1])) for p in predictions[j]]

    reader_model = os.path.splitext(os.path.basename(args.reader_model or 'default'))[0]
    retriever_model = os.path.splitext(os.path.basename(args.retriever_model or 'default'))[0]
    basename = os.path.splitext(os.path.basename(args.dataset))[0]
    outfile = os.path.join(args.out_dir, basename + '-' + reader_model + '-' + retriever_model + '-e2e.preds')

    logger.info('Writing results to %s' % outfile)
    with open(outfile, 'w') as f:
            json.dump(results, f)

    logger.info('Total time: %.2f' % (time.time() - t0))
