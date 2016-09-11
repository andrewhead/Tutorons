#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template.loader import get_template
from django.template import Context


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(package, description, documented_since, url, response_time, resolution_time, num_questions, results_with_code):
    package_template = get_template('package.html')
    context = {
        'package': package,
        'description': description,
        'documented_since': documented_since,
        'url': url,
        'response_time': response_time,
        'resolution_time': resolution_time,
        'num_questions': num_questions,
        'results_with_code': results_with_code
    }
    exp_html = package_template.render(Context(context))
    return exp_html
