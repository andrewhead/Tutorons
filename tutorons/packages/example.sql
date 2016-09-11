-- SQL query for getting results_with_code field for a package.
-- Needs to be translated into Django's ORM; untested.
SELECT SUM(pages_with_code) / (SUM(pages_with_code) + SUM(pages_without_code))::decimal AS ratio
FROM (
  SELECT web_page_url, COUNT(page_has_code) AS pages_with_code, COUNT(page_missing_code) AS pages_without_code
  FROM (
    SELECT webpagecontent.url as web_page_url,
      webpagecontent.id AS web_page_content_id,
      BOOL_OR(CASE WHEN (compute_index IS NULL) THEN true ELSE NULL END) AS page_missing_code,
      BOOL_OR(CASE WHEN (compute_index = 3) THEN true ELSE NULL END) AS page_has_code
    FROM webpagecontent
    LEFT OUTER JOIN code ON web_page_id = webpagecontent.id
    JOIN searchresultcontent ON content_id = webpagecontent.id
    JOIN searchresult ON searchresult.id = search_result_id
    JOIN search ON search_id = search.id
    WHERE search.fetch_index = 13 AND package = 'nodemailer'
    GROUP BY webpagecontent.id
  ) AS pages_have_code
  JOIN searchresultcontent ON content_id = web_page_content_id
  JOIN searchresult ON searchresult.id = search_result_id
  JOIN search ON search_id = search.id
  WHERE search.fetch_index = 13
  GROUP BY web_page_url
) AS page_occurrences_with_code;

-- Extracted segment from above SQL query for some testing purposes.
SELECT webpagecontent.url as web_page_url, code.id AS code_id
FROM webpagecontent
LEFT OUTER JOIN code ON web_page_id = webpagecontent.id
JOIN searchresultcontent ON content_id = webpagecontent.id
JOIN searchresult ON searchresult.id = search_result_id
JOIN search ON search_id = search.id
WHERE search.fetch_index = 13 AND package = 'nodemailer'
ORDER BY web_page_url;

-- SQL query for getting the documented_since field for a package.
SELECT MIN(webpageversion.timestamp)
FROM webpageversion
JOIN searchresult ON searchresult.url = webpageversion.url
JOIN search ON search.id = searchresult.search_id
WHERE search.fetch_index = 13 AND package = 'nodemailer';

-- SQL query for getting the num_questions field for a package.
SELECT COUNT(*)
FROM (
  SELECT questionsnapshot.question_id, COUNT(*) AS cnt
  FROM questionsnapshot
  JOIN questionsnapshottag ON questionsnapshottag.question_snapshot_id = questionsnapshot.id
  JOIN tag ON tag.id = questionsnapshottag.tag_id
  WHERE questionsnapshot.fetch_index = 13 AND questionsnapshot.title LIKE '%nodemailer%'
  GROUP BY questionsnapshot.question_id
) AS unique_questions;

-- SQL query for getting response_time field for a package.
SELECT issueevent.created_at - issue.created_at as resp_time
FROM issueevent
JOIN issue ON issue.id = issueevent.issue_id
JOIN githubproject ON githubproject.id = issue.project_id
WHERE issue.fetch_index = 1 AND issueevent.fetch_index = 10 AND githubproject.fetch_index = 1 AND githubproject.name LIKE '%nodemailer%';

-- SQL query for getting resolution_time field for a package.
SELECT issue.closed_at - issue.created_at as res_time
FROM issue
JOIN githubproject ON issue.project_id = githubproject.id
WHERE issue.fetch_index = 1 AND githubproject.fetch_index = 1 AND githubproject.name LIKE '%nodemailer%';
