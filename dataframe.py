import json
import os
import pandas as pd
from io import StringIO

def convert_to_dataframe():
    for file in os.listdir("/Users/aayushkumbhare/Desktop/SSMSOC/athlete-activity-data"):
        if file.endswith(".json"):
            filename = file
        file_path = f"/Users/aayushkumbhare/Desktop/SSMSOC/athlete-activity-data/{filename}"

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                #print("JSON File Loaded Successfully!")
                df = pd.DataFrame(data)
                #print(f"{file_path} added to dataframe successfully.")
                
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON format for file {file_path}.")
                print("Details:", e)

    df_exploded = df.explode('data')
    expanded_df = pd.DataFrame(df_exploded["data"].tolist())
    df.to_csv('expanded_df.csv', index=False)

    try:
        expanded_df['ts'] = pd.to_datetime(expanded_df['ts'])
        final_df = expanded_df.set_index('ts').resample('1s').mean().reset_index()

        final_df.to_csv('new_df.csv', index=False)
    except Exception as e:
        print(f"Error: {e}")
    
    return final_df
