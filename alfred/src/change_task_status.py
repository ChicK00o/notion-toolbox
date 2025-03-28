#!/usr/local/bin/python3

import sys
import argparse
import json

from notion_api import notion_api


try:
    parser = argparse.ArgumentParser(
        description='Change status of selected task')
    parser.add_argument('--status', nargs='*', help='status')
    parser.add_argument('--task', nargs='*', help='task id (notion url)')
    args = parser.parse_args(sys.argv[1].split())

    status = ' '.join(args.status)
    taskId = ' '.join(args.task)

    record = notion_api.get_block(taskId)
    record.status = status

    date = "Not Set" if not record.do_date else record.do_date.start.strftime("%d/%m/%Y")

    # Print out alfred-formatted JSON (modifies variables while passing query through)
    output = {
        "alfredworkflow": {
            "arg": ("recurring" if record.action_item[0] == '*' else "normal") + ("done" if status == "Done" else "notdone"),
            "variables": {
                "status": status,
                "task": taskId,
                "taskname":record.action_item,
                "date":date,
            }
        }
    }
    print(json.dumps(output))

    # print(status)
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
