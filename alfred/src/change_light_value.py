#!/usr/local/bin/python3

import sys
import argparse
from datetime import datetime

from notion_api import notion_api


try:
    parser = argparse.ArgumentParser(
        description='Change value of selected light')
    parser.add_argument('--value', nargs='*', help='value (Yes/No)')
    parser.add_argument('--light', nargs='*', help='light id (notion url)')
    args = parser.parse_args(sys.argv[1].split())

    value = ' '.join(args.value)
    lightId = ''.join(args.light)

    current_day = notion_api.current_day()

    # block = notion_api.get_block(lightId)
    setattr(current_day, lightId, True if value == "Yes" else False)

    print(value)
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
