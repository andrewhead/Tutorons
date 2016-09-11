#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from django.test import Client, TestCase
from django.db import connection

logging.basicConfig(level=logging.INFO, format="%(message)s")

class PackageDetectionTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/packages/scan',
            data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)['regions']
        return regions

    def test_single_package(self):
        string = "<p>Use the nodemailer package to send emails.</p>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]

        self.assertEqual(r.start_offset, 8)
        self.assertEqual(r.end_offset, 17)
        self.assertEqual(r.string, 'nodemailer')

    def test_single_package_case_insensitive(self):
        # Case 1
        string = "<p>Try the MONGOOSE package in this case.</p>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]

        self.assertEqual(r.start_offset, 8)
        self.assertEqual(r.end_offset, 15)
        self.assertEqual(r.string, 'MONGOOSE')

        # Case 2
        string = "<p>Try the MongOOsE package in this case.</p>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]

        self.assertEqual(r.start_offset, 8)
        self.assertEqual(r.end_offset, 15)
        self.assertEqual(r.string, 'MongOOsE')

    def test_multiple_packages(self):
        string = "<p>Choose between mysql or KaRmA for this tutorial.</p>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 2)

        r0 = regions[0]
        self.assertEqual(r0.start_offset, 15)
        self.assertEqual(r0.end_offset, 19)
        self.assertEqual(r0.string, 'mysql')

        r1 = regions[1]
        self.assertEqual(r1.start_offset, 24)
        self.assertEqual(r1.end_offset, 28)
        self.assertEqual(r1.string, 'KaRmA')
