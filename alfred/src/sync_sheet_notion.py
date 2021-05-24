#!/usr/local/bin/python3

from datetime import datetime
import sys
from notion.collection import NotionDate
import pygsheets
import pandas
import json

from notion_api import notion_api
from notion_api import config
from utils import tags_json, office_category_json, office_quarter_json, log
# from utils import office_quarter_json

try:
    # categoryFile = office_category_json()
    quarterFile = office_quarter_json()
    tagsFile = tags_json()

    # cv = notion_api.test_database().collection
    cv = notion_api.office_project_database().collection
    rows = cv.get_rows()
    table_data = [row.get_all_properties() | {'id-gen':row.id} for row in rows]
    ndf = pandas.DataFrame(table_data)

    gc = pygsheets.authorize(credentials_directory='/Users/rohit.bhosle/projects/personal/notion-toolbox/')
    sht1 = gc.open_by_key(config.sheet_id())
    wks = sht1[0]
    df = wks.get_as_df()

    for index, dataRow in df.iterrows():
        if not dataRow['ID']:
            new_row = cv.add_row()
            # categoryData = list(filter(lambda x: x["title"] == dataRow['Category'], categoryFile['items']))
            # if len(categoryData) > 0:
                # new_row.category = categoryData[0]['arg']
            tagData = list(filter(lambda x: x["title"] == dataRow['Tags'], tagsFile['items']))
            if len(tagData) > 0:
                new_row.tags = tagData[0]['arg']
            new_row.project = dataRow['Project']
            new_row.fe_estimate = dataRow['FE Estimate']
            new_row.be_estimate = dataRow['BE Estimate']
            new_row.planning_rag = dataRow['Planning RAG']
            new_row.current_rag = dataRow['Current RAG']
            new_row.status = dataRow['Status']
            if dataRow['Done ETA']:
                # log("done eta value : %r", dataRow['Done ETA'])
                new_row.done_eta = NotionDate(datetime.strptime(dataRow['Done ETA'], "%B %d, %Y").date())
            quarterData = list(filter(lambda x: x["title"] == dataRow['Quarter'], quarterFile['items']))
            if len(quarterData) > 0:
                new_row.quarter = quarterData[0]['arg']
            new_row.priority = dataRow['Priority']
            new_row.hide_in_search = dataRow['Hide In Search'] == "TRUE"
            df.at[index,'ID'] = new_row.id
        else:
            project_row = notion_api.get_row(dataRow['ID'])
            project_row.priority = dataRow['Priority']

    df.pop('Priority')
    df.insert(2, 'Priority', "")
    df.at[0,'Priority'] = '=ArrayFormula(if(G2:G<>"",row(C2:C)-1,""))'
    wks.set_dataframe(df,(1,1))

    # Print out alfred-formatted JSON (modifies variables while passing query through)
    output = {
        "alfredworkflow": {
            "arg": "Sync sheet to notion done",
        }
    }
    print(json.dumps(output))

except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
