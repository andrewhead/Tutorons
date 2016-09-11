#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import django
import json
import unittest
from django.test import Client
from tutorons.common.models import Block, ServerQuery, Region

logging.basicConfig(level=logging.INFO, format="%(message)s")


class DbLoggerTest(django.test.TestCase):
    def setUp(self):
        self.client = Client()

    def get_python_regions(self, document, url="www.test.com"):
        resp = self.client.post(
            '/python/scan',
            data={'origin': url, 'document': document})
        regions = json.loads(resp.content)
        return regions

    def get_css_regions(self, document, url="www.test.com"):
        resp = self.client.post(
            '/css/scan',
            data={'origin': url, 'document': document})
        regions = json.loads(resp.content)
        return regions

    def test_single_region(self):
        string = "<html> <body> <code>abs(2)</code> </body> </html>"
        Block.objects.using('logging').all().delete();
        ServerQuery.objects.using('logging').all().delete();
        Region.objects.using('logging').all().delete();
        self.get_python_regions(string)
        b = Block.objects.using('logging').all()[0]
        q = ServerQuery.objects.using('logging').all()[0]
        r = Region.objects.using('logging').all()[0]
        self.assertEqual(b.block_type, 'code')
        self.assertEqual(q.path, '/python/scan')
        self.assertEqual(r.start, 0)
        self.assertEqual(r.end, 2)

    def test_multiple_regions(self):
        string = "<html> <body> <code>abs(2)\nlen('fdsjkfds')\nbin(1)</code> </body> </html>"
        Region.objects.using('logging').all().delete();
        self.get_python_regions(string)
        r = Region.objects.using('logging').all()
        self.assertEqual(len(r), 3)

    def test_multiple_queries(self):
        string = "<html> <body> <code>abs(2)\nlen('fdsjkfds')\nbin(1)</code> </body> </html>"
        Block.objects.using('logging').all().delete();
        ServerQuery.objects.using('logging').all().delete();
        self.get_python_regions(string)
        self.get_python_regions(string)
        b = Block.objects.using('logging').all()
        self.assertEqual(len(b), 1)
        q = ServerQuery.objects.using('logging').all()
        self.assertEqual(len(q), 2)

    def test_multiple_documents(self):
        string = "<html> <body> <code>abs(2)\nlen('fdsjkfds')\nbin(1)</code> </body> </html>"
        Block.objects.using('logging').all().delete();
        self.get_python_regions(string)
        self.get_python_regions(string, "test1.com")
        b = Block.objects.using('logging').all()
        self.assertEqual(len(b), 2)

    def test_multiple_tutorons(self):
        string = '\n'.join([
            "<html>",
            "  <body>",
            "    <code>abs(2)\nlen('fdsjkfds')</code>",
            "    <code>h1 {color: navy; margin-left: 20px;}</code>",
            "  </body>",
            "</html>"
        ])
        ServerQuery.objects.using('logging').all().delete();
        self.get_python_regions(string)
        self.get_css_regions(string)
        q = ServerQuery.objects.using('logging').all()
        self.assertNotEqual(q[0].path, q[1].path)
