import pandas as pd
import json
from pathlib import Path

# df = pd.read_csv('answers.csv') # local csv file
sheet_id = '1VDNvlQS8v6WFh040YT99ij9-JNgUob8olW9IbYu5xNM'
file = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx'
sheets = pd.read_excel(file, sheet_name=None)

def convert_to_json():
    result = {"categories": {}}

    for round_name, df in sheets.items():
        # type: audio , video , image , text
        # daily double: true , false
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
                type = "text"
                daily_double = False
                # if category == "Jet-Setters":
                #     type = "image"
                # if category == "Spotify Wrap-Up":
                #     type = "audio"
                # if category == "The 'not-so fairweather' Office fans":
                #     type = "video"
                if df.columns[-1] == category:
                    color = "orange"
                result["categories"][round_name][category] = {
                    "color": color,
                    "type": type,
                    "daily_double": daily_double,
                    "content": {}
                }
                for _, row in df.iterrows():
                    content = row[category]
                    if content.find(/n) != -1 and result["categories"][round_name][category]["type"] == "text":
                        index_pos = content.index('\n')
                        label = content[:index_pos]
                        if label == "daily double":
                            daily_double = True
                        elif label == "image":
                            type = "image"
                        elif label == "audio":
                            type = "audio"
                        elif label == "video":
                            type = "video"
                        else:
                            type = "text"
                        content = content[index_pos+1:]
                    elif type == "image":
                        index_pos = content.index('\n')
                        src = content[:index_pos]
                        content = content[index_pos+1:]
                        result["categories"][round_name][category]["image_src"] = src
                        result["categories"][round_name][category]["content"][row["Value"]] = content                        
                    elif category == "Jet-Setters":
                        result["categories"][round_name][category]["type"] = "image"
                        directory = Path("images/trip_pics")
                        images = []
                        for i, file in enumerate(directory.iterdir()):
                            if content in file.name:
                                images.append(file.name)
                    elif category == "Spotify Wrap-Up":
                        result["categories"][round_name][category]["type"] = "audio"
                        result["categories"][round_name][category]["audio_file_name"] = f"audio/{content}.mp3"
                    elif category == "The 'not-so fairweather' Office fans":
                        index_pos = content.index('\n')
                        content= content[:index_pos]
                        src = content[index_pos+1:]
                        result["categories"][round_name][category]["type"] = "video"   
                        result["categories"][round_name][category]["video_src"] = src
                        result["categories"][round_name][category]["content"][row["Value"]] = content                        
                    else:
                        result["categories"][round_name][category]["content"][row["Value"]] = content                        

    # print(json.dumps(result, indent=2))

    with open("answers.json", "w") as f:
        json.dump(result, f)