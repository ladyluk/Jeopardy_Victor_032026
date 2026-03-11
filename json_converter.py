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
        # print("round_name: ", round_name)
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
                daily_double = False
                if df.columns[-1] == category:
                    color = "orange"
                result["categories"][round_name][category] = {
                    "color": color,
                    "content": {}
                }
                for _, row in df.iterrows():
                    clue = row[category]
                    label = ""
                    media_type = "text"
                    daily_double = False
                    if clue.find('\n') != -1:
                        index_pos = clue.index('\n')
                        label = clue[:index_pos]
                        clue = clue[index_pos+1:]
                        if label == "daily double":
                            daily_double = True
                        elif label == "image":
                            media_type = "image"
                        elif label == "audio":
                            media_type = "audio"
                        elif label == "video":
                            media_type = "video"
                        else:
                            media_type = "text"
                    content = {"Clue": clue, "Media_type": media_type, "Daily_double": daily_double}
                    result["categories"][round_name][category]["content"][row["Value"]] = content
                    if media_type == "image":
                        index_pos = clue.index('\n')
                        src = clue[:index_pos]
                        clue = clue[index_pos+1:]
                        result["categories"][round_name][category]["content"][row["Value"]]["image_src"] = src
                        result["categories"][round_name][category]["content"][row["Value"]]["Clue"] = clue                        
                    # elif category == "Jet-Setters":
                    #     result["categories"][round_name][category]["type"] = "image"
                    #     directory = Path("images/trip_pics")
                    #     images = []
                    #     for i, file in enumerate(directory.iterdir()):
                    #         if content in file.name:
                    #             images.append(file.name)
                    #     result["categories"][round_name][category]["content"][row["Value"]] = content  
                    # elif category == "Spotify Wrap-Up":
                    #     result["categories"][round_name][category]["type"] = "audio"
                    #     result["categories"][round_name][category]["audio_file_name"] = f"audio/{content}.mp3"
                    #     result["categories"][round_name][category]["content"][row["Value"]] = content  
                    # elif category == "The 'not-so fairweather' Office fans":
                    #     index_pos = content.index('\n')
                    #     content= content[:index_pos]
                    #     src = content[index_pos+1:]
                    #     result["categories"][round_name][category]["type"] = "video"   
                    #     result["categories"][round_name][category]["video_src"] = src
                    #     result["categories"][round_name][category]["content"][row["Value"]] = content                        
                    # else:
                    #     result["categories"][round_name][category]["content"][row["Value"]] = content                        
                    if category == "Nippon ga ichiban":
                        print("value: ", row["Value"])
                        print("media_type: ", result["categories"][round_name][category]["content"][row["Value"]]["Media_type"])
                        print("clue: ", result["categories"][round_name][category]["content"][row["Value"]]["Clue"])
                        print("daily_double: ", result["categories"][round_name][category]["content"][row["Value"]]["Daily_double"], '\n')

    # print(json.dumps(result, indent=2))

    with open("answers.json", "w") as f:
        json.dump(result, f)

convert_to_json()