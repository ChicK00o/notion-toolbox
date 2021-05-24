#!/usr/local/bin/python3

from datetime import datetime
import sys
import json
import argparse

from notion.collection import NotionDate

from notion_api import notion_api
from utils import app_url


try:
    collection = notion_api.change_date_database().collection

    parser = argparse.ArgumentParser(description='Add note')
    parser.add_argument('--tags', nargs='*', help='tags (CSV-style)')
    # parser.add_argument('--category', nargs='*', help='category (CSV-style)')
    parser.add_argument('--project', nargs='*', help='project (CSV-style)')
    parser.add_argument('--date', nargs='*', help='date')
    parser.add_argument('--rowid', nargs='*', help='rowid')
    parser.add_argument('--query', nargs=argparse.REMAINDER, help='query')
    args = parser.parse_args(sys.argv[1].split())

    query = ' '.join(args.query)

    row = collection.add_row()
    row.reason = query

    projectTags = []
    if args.project:
        project = ' '.join(args.project).split(',')
        row.project = project
    # if args.category:
    #     category = ' '.join(args.category).split(',')
    #     row.category = category
    if args.date:
        date = ' '.join(args.date)
        row.new_date = NotionDate(datetime.strptime(date, "%d/%m/%Y").date())
    if args.rowid:
        project_row = notion_api.get_row(' '.join(args.rowid))
        row.old_date = project_row.done_eta
        project_row.done_eta = row.new_date
        projectTags = project_row.tags
    if args.tags:
        tags = ' '.join(args.tags).split(',')
        row.tags = tags
        result = row.tags
        result.extend(x for x in projectTags if x not in result)
        row.tags = result
    else:
        row.tags = projectTags
    # Print out alfred-formatted JSON (modifies variables while passing query through)
    output = {
        "alfredworkflow": {
            "arg": query,
            "variables": {
                "url": app_url(row.get_browseable_url())
            }
        }
    }
    print(json.dumps(output))
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
