#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.conf import settings
import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format="%(message)s")


class InvalidRegexException(Exception):

    def __init__(self, pattern, msg):
        self.pattern = pattern
        self.msg = msg


def visualize(pattern):

    escaped = pattern.replace('/', r'\/')  # Regexper requires forward-slashes are escaped
    res = requests.get(settings.REGEX_SVG_ENDPOINT, params={'pattern': escaped})

    soup = BeautifulSoup(res.content)

    if len(soup.select('g.root')) == 0:
        raise InvalidRegexException(pattern, "pattern failed to parse with Regexper")

    svg = str(soup.svg)
    return svg
