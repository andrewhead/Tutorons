#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from bs4 import BeautifulSoup
from django.test import Client

logging.basicConfig(level=logging.INFO, format="%(message)s")


class PackageDatabaseQueryTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/packages/scan',
            data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)['regions']
        return regions

    def test_get_region(self):
        string = "<p>Use the nodemailer package to send emails.</p>"
        # string = "<html> <body> <code>abs(2)</code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]
        document = BeautifulSoup(r['document'])

        self.assertIn('nodemailer', document.text)

    def test_get_multiple_regions(self):
        string = "<p>Choose between mysql or KaRmA for this tutorial.</p>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 2)

        r0 = regions[0]
        document0 = BeautifulSoup(r0['document'])
        self.assertIn('mysql', document0.text)

        r1 = regions[1]
        document1 = BeautifulSoup(r1['document'])
        self.assertIn('karma', document1.text)
