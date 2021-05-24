#!/usr/local/bin/python3

import sys
import json
# import os

from notion.collection import NotionDate

from notion_api import notion_api
from notion_api import config
from utils import office_project_json


try:
    output = office_project_json()

    # category = os.getenv('category')

    if output is None:
        database = notion_api.office_project_database()
        results = database.build_query().execute()

        office_projects = [{
            "uid": row.id,
            "title": row.title,
            "subtitle": row.status,
            "variables": {"projectname": row.title, "projectrowid" : row.id, "projectdate" : "Not Set" if not row.done_eta else row.done_eta.start.strftime("%d/%m/%Y"), "projectrag" : row.current_rag},
            "arg": row.get_browseable_url(),
            "match": row.title,
            "copy": row.title,
            "largetype": row.title,
            "hide": row.hide_in_search
        } for row in results]

        with open(config.office_project_file_path(), "w") as outfile:
            json.dump({"items": office_projects}, outfile)
        
        print(json.dumps({"items": [x for x in office_projects if not x["hide"]]}))
    else:
        print(json.dumps({"items": [x for x in output["items"] if not x["hide"]]}))
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
