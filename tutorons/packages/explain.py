#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.core.cache import cache as dcache
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models, connection
from django.contrib.postgres.aggregates import general
from tutorons.packages.models import WebPageVersion, WebPageContent, Search, SearchResult, SearchResultContent, Code, QuestionSnapshotTag, IssueEvent, Issue, IssueComment
import cache
import logging
import slumber
import time

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(message)s")
default_requests_session = cache.get_session(timeout=1)
default_requests_session.headers['User-Agent'] =\
    "Andrew Head (for academic analysis) <andrewhead@eecs.berkeley.edu, Austin Le (for academic" +\
    " analysis) <austinhle@berkeley.edu>"

DOCUMENTED_SINCE_SUFFIX = '__documented'
RESPONSE_TIME_SUFFIX = '__response'
RESOLUTION_TIME_SUFFIX = '__resolution'
NUM_QUESTIONS_SUFFIX = '__questions'
RESULTS_WITH_CODE_SUFFIX = '__results_with_code'

def make_request(method, *args, **kwargs):
    MAX_ATTEMPTS = 5
    RETRY_DELAY = 30
    try_again = True
    attempts = 0
    res = None

    def log_error(err_msg):
        logging.warn(
            "Error (%s) For API call %s, Args: %s, Kwargs: %s",
            str(err_msg), str(method), str(args), str(kwargs)
        )

    while try_again and attempts < MAX_ATTEMPTS:
        try:
            res = method(*args, **kwargs)
            if hasattr(res, 'status_code') and res.status_code not in [200]:
                log_error(str(res.status_code))
                res = None
            try_again = False
        except (slumber.exceptions.HttpNotFoundError):
            log_error("Not Found")
            try_again = False
        except slumber.exceptions.HttpServerError:
            log_error("Server 500")
            try_again = False
        except requests.exceptions.ConnectionError:
            log_error("ConnectionError")
        except requests.exceptions.ReadTimeout:
            log_error("ReadTimeout")

        if try_again:
            logging.warn("Waiting %d seconds for before retrying.", int(RETRY_DELAY))
            time.sleep(RETRY_DELAY)
            attempts += 1

    return res


def explain(package):
    NPM_url = "https://www.npmjs.com/package/{pkg}".format(pkg=package)
    res = make_request(default_requests_session.get, NPM_url)
    if res is not None:
        page = BeautifulSoup(res.content, 'html.parser')
        readme = str(page.select('div#readme')[0])
        description = page.select('p.package-description')[0].text
        url = NPM_url

    documented_since = get_documented_since(package)

    response_time, resolution_time = get_response_time(package), get_resolution_time(package)

    num_questions = get_num_questions(package)

    results_with_code = get_results_with_code(package)

    return description, documented_since, url, response_time, resolution_time, num_questions, results_with_code


def get_documented_since(p):
    documented_since = dcache.get(p + DOCUMENTED_SINCE_SUFFIX)
    if documented_since is not None:
        return documented_since

    documented_since = (SearchResult.objects
        .filter(search_id=models.F('search__id'))
        .filter(web_page_version__url=models.F('url'))
        .filter(search__fetch_index=13)
        .filter(search__package=p)
        .aggregate(models.Min('web_page_version__timestamp'))['web_page_version__timestamp__min']
    )
    dcache.set(p + DOCUMENTED_SINCE_SUFFIX, documented_since, None)
    return documented_since


def get_response_time(p):
    from django.db import connection
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    for model in seen_models:
        print(str(model))

    response_time = dcache.get(p + RESPONSE_TIME_SUFFIX)
    if response_time is not None:
        return response_time

    response_times = (IssueComment.objects
        .filter(issue_id=models.F('issue__id'))
        .filter(issue__project_id=models.F('issue__project__id'))
        .filter(issue__project__fetch_index=1)
        .filter(issue__fetch_index=1)
        .filter(fetch_index=4)
        .filter(issue__project__name__icontains=p)
        .filter(~models.Q(user_id=models.F('issue__user_id')))
        .annotate(t1=models.F('created_at'))
        .annotate(t2=models.F('issue__created_at'))
    )

    total_seconds = 0
    num_valid = 0
    for t in response_times:
        if t.t1 is not None and t.t2 is not None:
            total_seconds += (t.t1 - t.t2).seconds
            num_valid += 1

    if num_valid == 0:
        response_time = 'Not enough data'
    else:
        seconds = total_seconds // num_valid
        hours = seconds // (60 * 60)
        minutes_divisor = seconds % (60 * 60)
        minutes = minutes_divisor // 60
        seconds = minutes_divisor % 60
        response_time = '{0} hours, {1} minutes, {2} seconds'.format(hours, minutes, seconds)

    dcache.set(p + RESPONSE_TIME_SUFFIX, response_time, None)
    return response_time


def get_resolution_time(p):
    resolution_time = dcache.get(p + RESPONSE_TIME_SUFFIX)
    if resolution_time is not None:
        return resolution_time

    resolution_times = (Issue.objects
        .filter(project_id=models.F('project__id'))
        .filter(fetch_index=1)
        .filter(project__fetch_index=1)
        .filter(project__name__icontains=p)
    )

    total_seconds = 0
    num_valid = 0
    for t in resolution_times:
        if t.closed_at is not None and t.created_at is not None:
            total_seconds += (t.closed_at - t.created_at).seconds
            num_valid += 1

    seconds = total_seconds // num_valid
    hours = seconds // (60 * 60)
    minutes_divisor = seconds % (60 * 60)
    minutes = minutes_divisor // 60
    seconds = minutes_divisor % 60

    resolution_time = '{0} hours, {1} minutes, {2} seconds'.format(hours, minutes, seconds)
    dcache.set(p + RESOLUTION_TIME_SUFFIX, resolution_time, None)
    return resolution_time


def get_num_questions(p):
    num_questions = dcache.get(p + NUM_QUESTIONS_SUFFIX)
    if num_questions is not None:
        return num_questions

    unique_questions = (QuestionSnapshotTag.objects
        .filter(question_snapshot_id=models.F('question_snapshot__id'))
        .filter(question_snapshot__fetch_index=13)
        .filter(tag_id=models.F('tag__id'))
        .filter(tag__tag_name__icontains=p)
        .annotate(num_tags=models.Count('question_snapshot__id'))
    )

    num_questions = len(unique_questions)
    dcache.set(p + NUM_QUESTIONS_SUFFIX, num_questions, None)
    return num_questions


def get_results_with_code(p):
    return ""

    # results_with_code = dcache.get(p + RESULTS_WITH_CODE_SUFFIX)
    # if results_with_code is not None:
    #     return results_with_code
    #
    # cursor = connection.cursor()
    # cursor.execute(
    #     """
    #     SELECT SUM(pages_with_code) / (SUM(pages_with_code) + SUM(pages_without_code)) AS ratio
    #     FROM (
    #         SELECT web_page_url, COUNT(page_has_code) AS pages_with_code, COUNT(page_missing_code) AS pages_without_code
    #         FROM (
    #             SELECT webpagecontent.url as web_page_url,
    #               webpagecontent.id AS web_page_content_id,
    #               BOOL_OR(CASE WHEN (compute_index IS NULL) THEN true ELSE NULL END) AS page_missing_code,
    #               BOOL_OR(CASE WHEN (compute_index = 3) THEN true ELSE NULL END) AS page_has_code
    #             FROM webpagecontent
    #             LEFT OUTER JOIN code ON web_page_id = webpagecontent.id
    #             JOIN searchresultcontent ON content_id = webpagecontent.id
    #             JOIN searchresult ON searchresult.id = search_result_id
    #             JOIN search ON search_id = search.id
    #             WHERE search.fetch_index = 13 AND package = %s
    #             GROUP BY webpagecontent.id
    #             ) AS pages_have_code
    #           JOIN searchresultcontent ON content_id = web_page_content_id
    #           JOIN searchresult ON searchresult.id = search_result_id
    #           JOIN search ON search_id = search.id
    #           WHERE search.fetch_index = 13
    #           GROUP BY web_page_url
    #     ) AS page_occurrences_with_code
    #     """,
    #     [p]
    # )
    #
    # results = cursor.fetchall()
    # results_with_code = results[0][0]
    # dcache.set(p + RESULTS_WITH_CODE_SUFFIX, results_with_code, None)
    # return results_with_code
