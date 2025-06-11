import pandas as pd 
import json 
import os 

folder_path = 'events'  
fight_rows = []

# Loop through all JSON files
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        with open(os.path.join(folder_path, filename), 'r') as f:
            data = json.load(f)

        date = data.get("date")
        event = data.get("event")

        for key, fight in data.items():
            if isinstance(fight, dict) and 'fighter1' in fight and 'fighter2' in fight:
                f1_data = fight.get('fighter1_fight_data') or {}
                f2_data = fight.get('fighter2_fight_data') or {}

                row = {
                    'event': event,
                    'date': date,
                    'fight_name': fight.get('name'),
                    'f1': fight.get('fighter1'),
                    'f2': fight.get('fighter2'),
                    'winner': fight.get('winner'),
                    'method': fight.get('method'),
                    'fight_length': fight.get('fight_length'),
                    'score': fight.get('score'),
                }

                # Add all fighter1 stats with prefix f1_
                for stat, value in f1_data.items():
                    row[f'f1_{stat}'] = value

                # Add all fighter2 stats with prefix f2_
                for stat, value in f2_data.items():
                    row[f'f2_{stat}'] = value

                fight_rows.append(row)

# Create DataFrame
df = pd.DataFrame(fight_rows)


