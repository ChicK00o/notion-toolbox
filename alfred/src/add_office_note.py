#!/usr/local/bin/python3

import sys
import json
import argparse

from notion_api import notion_api
from utils import app_url


try:
    collection = notion_api.office_notes_database().collection

    parser = argparse.ArgumentParser(description='Add note')
    parser.add_argument('--tags', nargs='*', help='tags (CSV-style)')
    # parser.add_argument('--category', nargs='*', help='category (CSV-style)')
    parser.add_argument('--project', nargs='*', help='project (CSV-style)')
    parser.add_argument('--rowid', nargs='*', help='rowid')
    parser.add_argument('--status', nargs='*', help='status')
    parser.add_argument('--query', nargs=argparse.REMAINDER, help='query')
    args = parser.parse_args(sys.argv[1].split())

    query = ' '.join(args.query)

    row = collection.add_row()
    row.note = query

    projectTags = []

    if args.project:
        project = ' '.join(args.project).split(',')
        row.project = project
    # if args.category:
    #     category = ' '.join(args.category).split(',')
    #     row.category = category
    if args.status:
        status = ' '.join(args.status)
        row.status = status
    if args.rowid:
        project_row = notion_api.get_row(' '.join(args.rowid))
        row.old_rag = project_row.current_rag
        project_row.current_rag = row.new_rag
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
