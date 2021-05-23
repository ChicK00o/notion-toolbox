#!/usr/local/bin/python3

from datetime import datetime
import sys
import json

from notion.collection import NotionDate

from notion_api import notion_api
from notion_api import config


try:
    database = notion_api.tags_database()
    results = database.build_query().execute()

    tags = [{
        "uid": row.id,
        "title": row.title,
        "variables": {"tagName": row.title},
        "arg": row.get_browseable_url(),
        "match": row.title,
        "copy": row.title,
        "largetype": row.title
    } for row in results]

    doneTag = [{
        "uid": "done",
        "title": "Done",
        "variables": {"tagName": "Done"},
        "arg": "Done",
        "match": "Done",
        "copy": "Done",
        "largetype": "Done"
    }]

    with open(config.tags_file_path(), "w") as outfile:
        json.dump({"items": doneTag + tags}, outfile)

    # database = notion_api.office_category_database()
    # results = database.build_query().execute()

    # office_categories = [{
    #     "uid": row.id,
    #     "title": row.title,
    #     "variables": {"categoryName": row.title},
    #     "arg": row.get_browseable_url(),
    #     "match": row.title,
    #     "copy": row.title,
    #     "largetype": row.title
    # } for row in results]

    # with open(config.office_category_file_path(), "w") as outfile:
    #     json.dump({"items": office_categories}, outfile)

    database = notion_api.office_project_database()
    results = database.build_query().execute()

    office_projects = [{
        "uid": row.id,
        "title": row.title,
        "subtitle": row.status,
        "variables": {"projectname": row.title, "projectrowid" : row.id, "projectdate" : "Not Set" if not row.done_eta else row.done_eta.start.strftime("%d/%m/%Y")},
        "arg": row.get_browseable_url(),
        "match": row.title,
        "copy": row.title,
        "largetype": row.title,
        "hide": row.hide_in_search
    } for row in results]

    with open(config.office_project_file_path(), "w") as outfile:
        json.dump({"items": office_projects}, outfile)
    
    database = notion_api.office_quarter_database()
    results = database.build_query().execute()

    office_quarters = [{
        "uid": row.id,
        "title": row.title,
        "variables": {"quartername": row.title},
        "arg": row.get_browseable_url(),
        "match": row.title,
        "copy": row.title,
        "largetype": row.title
    } for row in results]

    with open(config.office_quarter_file_path(), "w") as outfile:
        json.dump({"items": office_quarters}, outfile)
    
    print(str(len(tags)) + " tags")
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
