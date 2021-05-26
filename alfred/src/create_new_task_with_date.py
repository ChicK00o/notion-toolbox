#!/usr/local/bin/python3

import sys
import argparse
import json
from datetime import datetime
from notion.collection import NotionDate
from utils import log, _copy_properties

from notion_api import notion_api


try:
    parser = argparse.ArgumentParser(
        description='Change status of selected task')
    parser.add_argument('--task', nargs='*', help='task id (notion url)')
    parser.add_argument('--taskname', nargs='*', help='taskname')
    parser.add_argument('--status', nargs='*', help='status')
    parser.add_argument('--newdate', nargs='*', help='new date')
    
    args = parser.parse_args(sys.argv[1].split())

    status = ' '.join(args.status)
    taskname = ' '.join(args.taskname)
    newdate = ' '.join(args.newdate)
    taskId = ' '.join(args.task)

    record = notion_api.get_block(taskId)
    collection = notion_api.tasks_database().collection
    row = collection.add_row()
    _copy_properties(record, row)
    # row.action_item = "\\" + record.action_item
    # log("record action : %r || row action : %r", record.action_item, row.action_item)
    # row.tags = record.tags
    row.do_date = NotionDate(datetime.strptime(newdate, "%d/%m/%Y").date())
    row.status = "Ready"

    # Print out alfred-formatted JSON (modifies variables while passing query through)
    output = {
        "alfredworkflow": {
            "arg": "done",
            "variables": {
                "status": status,
                "task": taskId,
                "taskname":taskname,
                "date":newdate,
            }
        }
    }
    print(json.dumps(output))

    # print(status)
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
