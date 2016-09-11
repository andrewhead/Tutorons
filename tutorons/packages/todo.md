# Package Tutoron: Future Work

## Overall pipeline
In `detect.py`, the Tutoron uses a regex to look for words in the web page's content. It looks to see if any of the words match a word in the list of packages that we support (see next item below).

In `explain.py`, we perform on-the-fly queries to the `fetcher` database as well as a simple HTTP request to get the data we need to display on the Tutoron. While developing, I noticed a slight lag in having the Tutoron display for packages, when compared relatively to the other 4 Tutorons above it in the `home.html`.

## Support more packages
The list (set, really) of supported packages are pulled from the `Search` table. If we want to support more packages with this tutoron, we should pull more data into the `Search` table along with other related tables with the corresponding information.

## Update Django models as needed
`models.py` contains all Django models that we need for a package Tutoron. If we need to access other tables in the `fetcher` database, we may need to add additional models. Furthermore, depending on the queries that we need to write, we may need to add more fields to the models (but not necessarily to the tables themselves).

The main example I've seen of this so far is in adding ForeignKey fields in order to work with Django's high level abstraction of table joins. You can see how this is done within the `SearchResult` model with the `web_page_version` ForeignKey field. In particular, I expect we'll need to make a number of modifications to the models as they currently stand in order to support the complicated query for getting the `results_with_code` value for a specific package.

Each model has an embedded `class Meta` in order to explicitly tell it which table in `fetcher` to use; otherwise, it will prepend the application name to the table (e.g. `tutorons_webpagecontent`) and try to access it, which causes an error.

I've included the StackOverflow post Andrew linked to me previously down below under Useful Links and Resources.

## Useful Links and Resources
[Django: Aggregation](https://docs.djangoproject.com/en/1.9/topics/db/aggregation/)
[Django: Executing Queries](https://docs.djangoproject.com/en/1.9/topics/db/queries/)
[StackOverflow: Performing "Joins"](http://stackoverflow.com/questions/31735717/join-and-query-django-models-on-non-primary-key-relationship#answer-31735867)
