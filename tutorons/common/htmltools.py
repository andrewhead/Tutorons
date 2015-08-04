#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from bs4 import BeautifulSoup
import re


logging.basicConfig(level=logging.INFO, format="%(message)s")


class HtmlDocument(BeautifulSoup):
    ''' Subclass of BeautifulSoup that cleans HTML documents for our processing purposes. '''

    def __init__(self, text, *args, **kwargs):
        filled = fill_empty_lines(text)
        super(self.__class__, self).__init__(filled, *args, **kwargs)


def fill_empty_lines(text, tag='p'):
    ''' Add empty element to empty lines of an HTML document. '''
    filled = re.sub('^$', '<{tag}></{tag}>'.format(tag=tag), text, flags=re.MULTILINE)
    return filled


def get_css_selector(tag):
    ''' Create a CSS selector that can choose this tag from the document. '''

    elements = []

    element = tag
    while element.name != '[document]':

        parent = element.parent
        type_siblings = parent.find_all(element.name, recursive=False)
        index = -1
        for i, s in enumerate(type_siblings):
            if id(s) == id(element):
                index = i + 1  # in CSS, nth-of-type index starts at 1
                break

        elements.insert(0, {'name': element.name, 'index': index})
        element = parent

    element_selectors = []
    for i, el in enumerate(elements):
        tag_name = el['name'].upper()
        if i == 0 and el['name'] == 'html':
            element_selectors.append(tag_name)
        else:
            element_selectors.append(
                '%s:nth-of-type(%d)' % (tag_name, el['index'])
            )
    return ' > '.join(element_selectors)
