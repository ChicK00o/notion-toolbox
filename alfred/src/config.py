import sys
import os
import json
from pathlib import Path
from cachetools import cached


class Config():
    @cached(cache={})
    def tags_file_path(self):
        return str(Path(__file__).parent.parent.absolute()) + "/data/tags.json"

    @cached(cache={})
    def office_category_file_path(self):
        return str(Path(__file__).parent.parent.absolute()) + "/data/office_category.json"

    @cached(cache={})
    def office_project_file_path(self):
        return str(Path(__file__).parent.parent.absolute()) + "/data/office_project.json"

    @cached(cache={})
    def office_quarter_file_path(self):
        return str(Path(__file__).parent.parent.absolute()) + "/data/office_quarter.json"

    @cached(cache={})
    def config_file_path(self):
        return str(Path(__file__).parent.parent.absolute()) + "/data/config.json"

    @cached(cache={})
    def config_json(self):
        try:
            if os.path.isfile(self.config_file_path()):
                with open(self.config_file_path()) as json_file:
                    return json.load(json_file)
        except Exception as e:
            # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
            sys.stderr.write(e)

    @cached(cache={})
    def notion_token(self):
        return self.config_json()['NOTION_TOKEN']

    @cached(cache={})
    def tags_database_url(self):
        return self.config_json()['TAGS_DATABASE_URL']

    @cached(cache={})
    def office_category_database_url(self):
        return self.config_json()['OFFICE_CATEGORY_DATABASE_URL']

    @cached(cache={})
    def office_project_database_url(self):
        return self.config_json()['OFFICE_PROJECT_DATABASE_URL']

    @cached(cache={})
    def office_quarter_database_url(self):
        return self.config_json()['OFFICE_QUARTER_DATABASE_URL']

    @cached(cache={})
    def change_rag_database_url(self):
        return self.config_json()['CHANGE_RAG_DATABASE_URL']

    @cached(cache={})
    def change_date_database_url(self):
        return self.config_json()['CHANGE_DATE_DATABASE_URL']

    @cached(cache={})
    def tasks_database_url(self):
        return self.config_json()['TASKS_V2_DATABASE_URL']

    @cached(cache={})
    def wins_database_url(self):
        return self.config_json()['WINS_DATABASE_URL']
    
    @cached(cache={})
    def lose_database_url(self):
        return self.config_json()['LOSE_DATABASE_URL']

    @cached(cache={})
    def notes_database_url(self):
        return self.config_json()['NOTES_DATABASE_URL']

    @cached(cache={})
    def office_notes_database_url(self):
        return self.config_json()['OFFICE_NOTES_DATABASE_URL']

    @cached(cache={})
    def year_database_url(self):
        return self.config_json()['YEAR_DATABASE_URL']

    @cached(cache={})
    def quarter_database_url(self):
        return self.config_json()['QUARTER_DATABASE_URL']

    @cached(cache={})
    def month_database_url(self):
        return self.config_json()['MONTH_DATABASE_URL']

    @cached(cache={})
    def week_database_url(self):
        return self.config_json()['WEEK_DATABASE_URL']

    @cached(cache={})
    def day_database_url(self):
        return self.config_json()['DAY_DATABASE_URL']

    @cached(cache={})
    def inbox_section_url(self):
        return self.config_json()['INBOX_SECTION_URL']

    @cached(cache={})
    def test_database_url(self):
        return self.config_json()['TEST']

    @cached(cache={})
    def sheet_id(self):
        return self.config_json()['SHEET_ID']

    @cached(cache={})
    def custom_day_format(self):
        return self.config_json().get('CUSTOM_DAY_FORMAT', "%B %-d")
