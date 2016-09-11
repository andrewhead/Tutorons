#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import requests_cache
import time
import urlparse


logging.basicConfig(level=logging.INFO, format="%(message)s")
CACHE_NAME = 'packages'
requests_cache.install_cache(CACHE_NAME)


def clean_url(url):
    '''
    Clean URL so that we don't show any parameters passed in.
    This is to avoid showing any authorization parameters.
    REUSE: from http://stackoverflow.com/questions/8567171/scrapy-query-string-removal.
    '''
    parsed = urlparse.urlparse(url)
    return parsed.scheme + '://' + parsed.netloc + parsed.path


def throttle_hook(timeout=1.0):
    '''
    Hook for throttling requests if not in cache.
    Snippet from http://requests-cache.readthedocs.org/en/latest/user_guide.html#usage.
    '''
    def hook(response, *args, **kwargs):
        if not getattr(response, 'from_cache', False):
            logging.info(
                "Content for %s has not been fetched or is out of date.  Fetching.",
                clean_url(response.url)
            )
            time.sleep(timeout)
        else:
            logging.info(
                "Found recent, cached content for %s",
                clean_url(response.url)
            )
        return response
    return hook


def get_session(timeout=1.0):
    session = requests_cache.CachedSession(expire_after=60*60*24*7)
    session.hooks = {'response': throttle_hook(timeout)}
    return session
