import json
import os
import pandas as pd

for file in os.listdir("/Users/aayushkumbhare/Desktop/SSMSOC/athlete-activity-data"):
    if file.endswith(".json"):
        filename = file
    file_path = f"/Users/aayushkumbhare/Desktop/SSMSOC/athlete-activity-data/{filename}"

    if not os.path.exists(file_path):
        print("Error: File does not exist at the specified path.")
    elif os.stat(file_path).st_size == 0:
        print("Error: File is empty.")
    else:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                print("JSON File Loaded Successfully!")
                
                for entry in data[0]["data"]:
                    entry['ts'] = pd.to_datetime(entry["ts"], unit="s").strftime("%Y-%m-%d %H:%M:%S")

                with open(file_path, 'w') as json_out:
                    json.dump(data, json_out, indent=4)
                print("Timestamps Extracted Successfully!")
                
            except json.JSONDecodeError as e:
                print("Error: Invalid JSON format.")
                print("Details:", e)
