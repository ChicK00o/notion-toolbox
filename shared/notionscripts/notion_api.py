#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

from cachetools import cached
from datetime import datetime
from datetime import timedelta
import calendar

from notion.client import NotionClient
from notion.block import DividerBlock, TextBlock, CollectionViewBlock
from notion.collection import NotionDate

from notionscripts.config import Config


class NotionApi():
    def __init__(self, config=Config()):
        self.config = config

    @cached(cache={})
    def client(self):
        return NotionClient(token_v2=self.config.notion_token(), monitor=False)

    @cached(cache={})
    def tags_database(self):
        return self.client().get_collection_view(self.config.tags_database_url())

    @cached(cache={})
    def tasks_database(self):
        return self.client().get_collection_view(self.config.tasks_database_url())

    @cached(cache={})
    def wins_database(self):
        return self.client().get_collection_view(self.config.wins_database_url())
    
    @cached(cache={})
    def lose_database(self):
        return self.client().get_collection_view(self.config.lose_database_url())

    @cached(cache={})
    def notes_database(self):
        return self.client().get_collection_view(self.config.notes_database_url())

    @cached(cache={})
    def year_database(self):
        return self.client().get_collection_view(self.config.year_database_url())

    @cached(cache={})
    def quarter_database(self):
        return self.client().get_collection_view(self.config.quarter_database_url())

    @cached(cache={})
    def month_database(self):
        return self.client().get_collection_view(self.config.month_database_url())

    @cached(cache={})
    def week_database(self):
        return self.client().get_collection_view(self.config.week_database_url())

    @cached(cache={})
    def day_database(self):
        return self.client().get_collection_view(self.config.day_database_url())

    def get_block(self, id):
        return self.client().get_block(id)

    def append_text_to_block(self, block, text):
        return block.children.add_new(TextBlock, title=text)

    @cached(cache={})
    def inbox_section(self):
        return self.client().get_block(self.config.inbox_section_url())

    @cached(cache={})
    def current_year(self):
        found_year = None
        current_year = str(datetime.now().year)

        # List all the records with "Bob" in them
        for row in self.year_database().collection.get_rows(search=current_year):
            if row.name == current_year:
                found_year = row
                break
        
        if found_year is None:
            found_year = self.create_new_year(current_year)

        return found_year

    @cached(cache={})
    def create_new_year(self, year="Default"):
        row = self.year_database().collection.add_row()
        row.name = year
        row.theme = "Catching Up"
        row.date = NotionDate(datetime(int(year), 1, 1).date(), datetime(int(year), 12, 31).date())
        return row

    @cached(cache={})
    def current_quarter(self):
        found_quarter = None
        date = datetime.now().date()
        current_quarter = "Q" + str((date.month - 1) // 3 + 1) + " - " + str(date.year)

        # List all the records with "Bob" in them
        for row in self.quarter_database().collection.get_rows(search=current_quarter):
            if row.name == current_quarter:
                found_quarter = row
                break
        
        if found_quarter is None:
            found_quarter = self.create_new_quarter(date, current_quarter)

        return found_quarter

    @cached(cache={})
    def create_new_quarter(self, date: datetime, quarter="Default"):
        quarter_int = (date.month - 1) // 3 + 1
        last_day = 31
        start_month = 1
        end_month = 3
        if quarter_int == 2:
            last_day = 30
            start_month = 4
            end_month = 6
        elif quarter_int == 3:
            last_day = 30
            start_month = 7
            end_month = 9
        elif quarter_int == 4:
            start_month = 10
            end_month = 12
        row = self.quarter_database().collection.add_row()
        row.name = quarter
        row.annual_reviews = self.current_year()
        row.date = NotionDate(datetime(int(date.year), start_month, 1).date(), datetime(int(date.year), end_month, last_day).date())
        return row

    @cached(cache={})
    def current_month(self):
        found_month = None
        current_month = datetime.now().strftime("%B")

        # List all the records with "Bob" in them
        for row in self.month_database().collection.get_rows(search=current_month):
            if row.name == current_month:
                found_month = row
                break
        
        if found_month is None:
            found_month = self.create_new_month(current_month)

        return found_month

    @cached(cache={})
    def create_new_month(self, month="Default"):
        row = self.month_database().collection.add_row()
        today = datetime.now().date()
        row.name = month
        row.theme = "Catching Up"
        row.quarter = self.current_quarter()
        row.year = self.current_year()
        row.date = NotionDate(datetime(today.year, today.month, 1).date(), datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).date())
        return row

    @cached(cache={})
    def current_week(self):
        found_week = None
        current_date = datetime.now()

        week_number = current_date.isocalendar()[1]
        week_number = week_number + (current_date.isoweekday() == 7) + 1

        current_week = "Week " + str(week_number) 

        # List all the records with "Bob" in them
        for row in self.week_database().collection.get_rows(search=current_week):
            if row.name == current_week:
                found_week = row
                break
        
        if found_week is None:
            found_week = self.create_new_week(current_week)

        return found_week

    @cached(cache={})
    def create_new_week(self, week="Default"):
        row = self.week_database().collection.add_row()
        today = datetime.now().date()
        row.name = week
        row.month = self.current_month()
        row.quarter = self.current_quarter()
        row.year = self.current_year()
        start, end = self.get_start_end_dates(today.year, today.isocalendar()[1])
        row.date = NotionDate(start.date(), end.date())
        return row

    @cached(cache={})
    def get_start_end_dates(self, year, week):
        d = datetime(year,1,1)
        if(d.weekday()<= 3):
            d = d - timedelta(d.weekday())             
        else:
            d = d + timedelta(7-d.weekday())
        dlt = timedelta(days = (week-1)*7)
        return d + dlt - timedelta(days=1),  d + dlt + timedelta(days=6) - timedelta(days=1)

    @cached(cache={})
    def current_day(self):
        found_day = None
        current_date = datetime.now()

        current_day = current_date.strftime(self.config.custom_day_format())

        for row in self.day_database().collection.get_rows(search=current_day):
            if row.name == current_day:
                found_day = row
                break
        
        if found_day is None:
            found_day = self.create_new_day(current_day)

        return found_day  
    
    @cached(cache={})
    def create_new_day(self, day="Default"):
        row = self.day_database().collection.add_row()
        row.name = day
        row.date = NotionDate(datetime.now().date())
        row.week = self.current_week()
        row.month = self.current_month()
        row.quarter = self.current_quarter()
        row.year = self.current_year()
        return row 

    def current_week_lights(self):
        found_lights = None

        for block in self.current_week().children:
            if type(block) == CollectionViewBlock and block.title.endswith("Lights"):
                found_lights = block
                break
            else:
                continue

        return found_lights

    def current_day_lights(self):
        view = self.current_week_lights()

        if view is None:
            return

        current_day = datetime.now().strftime("%A")

        lights = []
        for row in view.collection.get_rows():
            if not row.objective or row.objective.startswith("["):
                continue

            lights.append({
                "id": row.id,
                "title": "{} ({})".format(row.objective, getattr(row, current_day) or " "),
                "url": row.get_browseable_url()
            })

        return lights

    def append_to_current_day_notes(self, content):
        # Get the divider block that signifies the end of the notes for the current day
        divider_block = [x for x in self.current_day().children if type(x) == DividerBlock][0]

        # Add note to end of the page, then move it to before the divider
        note_block = self.current_day().children.add_new(TextBlock, title=content)
        note_block.move_to(divider_block, "before")

        return note_block

    def append_to_inbox(self, content):
        # Add note to end of the section
        note_block = self.inbox_section().children.add_new(TextBlock, title=content)
        return note_block

    def get_current_tasks(self):
        filter_params = {
            "filters": [
                {
                    "filter": {
                        "value": {
                            "type": "exact",
                            "value": False
                        },
                        "operator": "checkbox_is"
                    },
                    "property": "done"
                },
                {
                    "filter": {
                        "value": {
                            "type": "relative",
                            "value": "today"
                        },
                        "operator": "date_is_on_or_before"
                    },
                    "property": "do_date"
                },
                {
                    "filter": {
                        "value": {
                            "type": "exact",
                            "value": "Completed"
                        },
                        "operator": "enum_is_not"
                    },
                    "property": "status"
                }
            ],
            "operator": "and"
        }
        current_tasks_query = self.tasks_database().build_query(filter=filter_params)
        return current_tasks_query.execute()
