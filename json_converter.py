import pandas as pd
import json

# df = pd.read_csv('answers.csv') # local csv file
sheet_id = '1VDNvlQS8v6WFh040YT99ij9-JNgUob8olW9IbYu5xNM'
file = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx'
sheets = pd.read_excel(file, sheet_name=None)

def convert_to_json():
    result = {"categories": {}}

    for round_name, df in sheets.items():
        # print(round_name)
        color = ""
        if round_name == "Vic Jeopardy":
            color = "orange"
        else: color ="blue"
        result["categories"][round_name] = {}
        if round_name == "Final Jeopardy":
            result["categories"][round_name] = {
                "Category": df.columns[0],
                "Content": df.iloc[0, 0]
            }
        else:
            for category in df.columns[1:]:
                if df.columns[-1] == category:
                    color = "orange"
                result["categories"][round_name][category] = {
                    "color": color,
                    "content": {}
                }
                for _, row in df.iterrows():
                    result["categories"][round_name][category]["content"][row["Value"]] = row[category]

    # print(json.dumps(result, indent=2))

    with open("answers.json", "w") as f:
        json.dump(result, f)