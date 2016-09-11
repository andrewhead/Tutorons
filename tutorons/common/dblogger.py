#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from tutorons.common.models import Block, ServerQuery
from tutorons.common.htmltools import get_css_selector
import datetime


logging.basicConfig(level=logging.INFO, format="%(message)s")


def _get_request_metadata(request):
    url = request.POST.get('origin')
    path = request.path_info
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = forwarded_for.split(',')[-1].strip() if forwarded_for \
        else request.META.get('REMOTE_ADDR')
    return url, path, ip


class DbLogger(object):

    def log_query(self, request):
        _, path, ip = _get_request_metadata(request)
        query = ServerQuery.objects.using('logging').create(ip_addr=ip, path=path)
        return query

    def log_region(self, request, query, region):

        url, path, ip = _get_request_metadata(request)
        region_type, request_method = request.path_info.split('/')[0:2]
        block_hash = hash(region.node)
        block_type = region.node.name

        # Make a record for the block of text that is being explained
        block, created = Block.objects.using('logging').get_or_create(
            url=url,
            block_type=block_type,
            block_hash=block_hash
        )
        if created:
            block.block_test = region.node
            block.save(using='logging')

        # Create and save a new region
        region = query.region_set.using('logging').create(
            block=block,
            node=get_css_selector(region.node),
            start=region.start_offset,
            end=region.end_offset,
            string=region.string,
            region_type=region_type,
            region_method=request_method
        )
        return region

    def update_server_end_time(self, query):
        query.end_time = datetime.datetime.now()
        query.save(using='logging')
