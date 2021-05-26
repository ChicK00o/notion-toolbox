from __future__ import print_function
import os
import json
import sys
from cachetools import cached
from notion_api import config
from copy import copy, deepcopy 

def _copy_properties(old, new):
    for prop in dir(old):
        try:
            if not prop.startswith('_'):
                attr = getattr(old, prop)
                # copying tags creates a whole new set of problems
                if prop != 'tags' and attr != '' and not callable(attr):
                    setattr(new, prop, copy(attr))

        # notion-py raises AttributeError when it can't assign an attribute
        except AttributeError:
            pass

    if bool(old.children):
        for old_child in old.children:
            new_child = new.children.add_new(old_child.__class__)
            _copy_properties(old_child, new_child)


def app_url(browser_url):
    return browser_url.replace("https://", "notion://")


def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)

@cached(cache={})
def tags_json():
    output = None
    tag_file_path = config.tags_file_path()
    if os.path.isfile(tag_file_path):
        with open(tag_file_path) as json_file:
            output = json.load(json_file)
    return output

@cached(cache={})
def office_category_json():
    output = None
    office_category_file_path = config.office_category_file_path()
    if os.path.isfile(office_category_file_path):
        with open(office_category_file_path) as json_file:
            output = json.load(json_file)
    return output

@cached(cache={})
def office_project_json():
    output = None
    office_project_file_path = config.office_project_file_path()
    if os.path.isfile(office_project_file_path):
        with open(office_project_file_path) as json_file:
            output = json.load(json_file)
    return output

@cached(cache={})
def office_quarter_json():
    output = None
    office_quarter_file_path = config.office_quarter_file_path()
    if os.path.isfile(office_quarter_file_path):
        with open(office_quarter_file_path) as json_file:
            output = json.load(json_file)
    return output

@cached(cache={})
def find_tag(id):
    try:
        for tag in tags_json()["items"]:
            if tag["uid"] == id:
                return tag["title"]
    except Exception:
        raise "Could not find tags in the tags.json file (check the file)"


@cached(cache={})
def tags_schema_id(row):
    for entry in row.schema:
        if entry["slug"] == "tags":
            return entry["id"]
    raise "Could not find tags slug in the row schema"


def fast_tags_for_task(row):
    tags = []

    data = row.get(["properties", tags_schema_id(row)])

    if data is not None:
        for property in data:
            if property[0] == "‣":
                tag = find_tag(property[1][0][1])
                if tag:
                    tags.append(tag)

    return ", ".join(tags)
