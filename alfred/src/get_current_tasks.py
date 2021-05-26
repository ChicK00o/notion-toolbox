#!/usr/local/bin/python3

from datetime import date, datetime, timedelta
import sys
import json

from notion_api import notion_api
from utils import app_url, fast_tags_for_task


try:
    tasks = [{
        "uid": row.id,
        "title": "[" + row.status + "] " + row.title,
        "subtitle": ("" if not row.do_date else ("✅ Complete" if row.status == "Done" else ("❗Today" if datetime.now().date() == row.do_date.start else ("🚫 Overdue" if datetime.now().date() > row.do_date.start else ("🔷 Attention" if (datetime.now() + timedelta(days=7)).date() > row.do_date.start else "📡 Future"))))) + " Tags: " + fast_tags_for_task(row),
        "variables": {"taskName": row.title, "url": app_url(row.get_browseable_url())},
        "arg": row.get_browseable_url(),
        "match": row.title + " " + row.status + " " + fast_tags_for_task(row),
        "copy": row.title,
        "largetype": row.title
    } for row in notion_api.get_active_tasks()]

    empty_item = [{
        "uid": "nothing",
        "title": "Nothing... Maybe start something",
    }]

    if not tasks:
        print(json.dumps({"items": tasks + empty_item}))
    else:
        print(json.dumps({"items": tasks}))
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
