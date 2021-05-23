#!/usr/local/bin/python3

import sys
import pygsheets
import pandas
import json

from notion_api import notion_api
from notion_api import config
# from utils import tags_json, office_category_json, office_quarter_json
# from utils import office_quarter_json

try:
    # cv = notion_api.test_database().collection
    cv = notion_api.office_project_database().collection

    gc = pygsheets.authorize(credentials_directory='/Users/rohit.bhosle/projects/personal/notion-toolbox/')
    sht1 = gc.open_by_key(config.sheet_id())
    wks = sht1[0]
    df = wks.get_as_df()

    rows = cv.get_rows()
    table_data = [{
        "ID": row.id,
        "Hide In Search": row.hide_in_search,
        "Quarter": row.quarter[0].title if len(row.quarter) > 0 else "",
        "Project": row.project,
        "BE Estimate": row.be_estimate,
        "FE Estimate": row.fe_estimate,
        "Tags": row.tags[0].title if len(row.tags) > 0 else "",
        "Planning RAG": row.planning_rag,
        "Current RAG": row.current_rag,
        "Done ETA": "" if not row.done_eta else row.done_eta.start.strftime("%B %d, %Y")
    } for row in rows]
    ndf = pandas.DataFrame(table_data)


    ndf = ndf.set_index('ID')
    df = df.set_index('ID')
    df.update(ndf)
    df.reset_index(inplace=True)

    df.pop('Priority')
    df.insert(2, 'Priority', "")
    df.at[0,'Priority'] = '=ArrayFormula(if(G2:G<>"",row(C2:C)-1,""))'
    wks.set_dataframe(df,(1,1))

    # Print out alfred-formatted JSON (modifies variables while passing query through)
    output = {
        "alfredworkflow": {
            "arg": "Sync notion to sheet done",
        }
    }
    print(json.dumps(output))

except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
