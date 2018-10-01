#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree
"""Preprocess function to filter/prepare Wikipedia docs."""

import regex as re
from html.parser import HTMLParser

PARSER = HTMLParser()
BLACKLIST = set(['23443579', '52643645'])  # Conflicting disambiguation pages


def preprocess(article):
    # Take out HTML escaping that WikiExtractor didn't clean
    # WikiExtractor is a Python script that extracts and cleans text from a Wikipedia database dump.
    for k, v in article.items():
        article[k] = PARSER.unescape(v)

    # Filter some disambiguation pages not caught by the WikiExtractor
    # Disambiguation means that the article title is ambiguous
    # For example, "Mercury" can refer to a chemical element, a planet, a Roman god, etc.
    # Should be: Mercury (element), Mercury (planet) and Mercury (mythology)
    if article['id'] in BLACKLIST:
        return None
    if '(disambiguation)' in article['title'].lower():
        return None
    if '(disambiguation page)' in article['title'].lower():
        return None

    # Take out List/Index/Outline pages (reason: mostly links)
    if re.match(r'(List of .+)|(Index of .+)|(Outline of .+)',
                article['title']):
        return None

    # Return doc with `id` set to `title`
    return {'id': article['title'], 'text': article['text']}
