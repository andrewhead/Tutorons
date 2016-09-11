#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
import string

from tutorons.common.extractor import Region
from tutorons.packages.packages import package_list

logging.basicConfig(level=logging.INFO, format="%(message)s")


class PackageExtractor(object):

    def extract(self, node):
        text = node.text.encode('ascii', 'ignore')
        regions = []
        char_index = 0

        for line in text.split('\n'):
            words = re.findall(r"\b[^\W\d_]+-?'?[^\W\d_]+\b", line)

            line_offset = 0
            for word in words:
                if word.lower() in package_list: # Picked up on a package name
                    position = string.index(line, word)
                    first_char = char_index + line_offset + position
                    last_char = char_index + line_offset + position + len(word) - 1
                    line_offset = position + 1

                    r = Region(node, first_char, last_char, word)
                    regions.append(r)
                    char_index += (len(line) + 1)  # every line has at least 1 char: the newline

        print(str(regions))

        return regions
