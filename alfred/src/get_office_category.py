#!/usr/local/bin/python3

import sys
import json

from notion_api import notion_api
from notion_api import config
from utils import office_category_json


try:
    output = office_category_json()

    if output is None:
        database = notion_api.office_category_database()
        results = database.build_query().execute()

        office_categories = [{
            "uid": row.id,
            "title": row.title,
            "variables": {"categoryName": row.title},
            "arg": row.get_browseable_url(),
            "match": row.title,
            "copy": row.title,
            "largetype": row.title
        } for row in results]

        with open(config.office_category_file_path(), "w") as outfile:
            json.dump({"items": office_categories}, outfile)
        print(json.dumps({"items": office_categories}))
    else:
        print(json.dumps(output))
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
