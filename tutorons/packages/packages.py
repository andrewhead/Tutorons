#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.db import connection
import sys

# List of packages that our Tutoron supports.
# This list is pulled from all packages for which data has been collected in the Search table.

if 'test' in sys.argv:
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT(package) FROM search")

    results = cursor.fetchall()

    package_list = set()
    for package in results:
        if package[0]:
            # Call str() on each package in the list to convert from unicode string to regular string.
            package_list.add(str(package[0]).lower())
else:
    # Test list of packages, since we can't access the Search table to get a list of packages in test environments.
    test_packages = ['nodemailer', 'mysql', 'karma', 'mongoose']
    package_list = set(test_packages)

print('Currently supporting the following packages: ' + str(package_list))
