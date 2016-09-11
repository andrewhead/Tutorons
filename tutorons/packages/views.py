#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.common.scanner import NodeScanner
from tutorons.packages.detect import PackageExtractor
from tutorons.packages.explain import explain as package_explain
from tutorons.packages.render import render as package_render
from tutorons.packages.packages import package_list
from tutorons.common.dblogger import DbLogger
from tutorons.common.views import pagescan, snippetexplain


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DbLogger()


@csrf_exempt
@pagescan
def scan(html_doc):
    package_extractor = PackageExtractor()
    package_scanner = NodeScanner(package_extractor, ['p'])
    regions = package_scanner.scan(html_doc)
    rendered_regions = []
    for r in regions:
        # log_region(r, origin)
        explanation = package_explain(r.string)
        if explanation is not None:
            description, documented_since, url, response_time, resolution_time, num_questions, results_with_code = explanation
            document = package_render(r.string, description, documented_since, url, response_time, resolution_time, num_questions, results_with_code)
            rendered_regions.append((r, document))
    # db_logger.update_server_end_time(qid)
    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):
    error_template = get_template('error.html')

    if text in package_list:
        hdr, exp, url = package_explain(text)
        explanation = package_render(text, hdr, exp, url)
    else:
        logging.error("Error processing package %s", text)
        explanation = error_template.render(Context({'text': text, 'type': 'package'}))

    return explanation
