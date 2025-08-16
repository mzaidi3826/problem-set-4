'''
PART 1: ETL the dataset and save in `data/`

Here is the imbd_movie data:
https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true

It is in JSON format, so you'll need to handle accordingly and also figure out what's the best format for the two analysis parts. 
'''

import os
import pandas as pd
import json
import requests
from datetime import datetime 

# Load datasets and save to '/data'
url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"

# Extract 
print("Downloading dataset...")
response = requests.get(url, stream=True)
response.raise_for_status()

movies_json = []
for line in response.iter_lines():
    if line:  # skip empty lines
        movies_json.append(json.loads(line.decode("utf-8")))

print(f"Loaded {len(movies_json)} movies")

# Transform
df = pd.DataFrame(movies_json)

# Make sure to always save to root/data
base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from src/
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

# Load (save to ./data with timestamp)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_out = os.path.join(data_dir, f"imdb_movies_{timestamp}.csv")
json_out = os.path.join(data_dir, f"imdb_movies_{timestamp}.json")

df.to_csv(csv_out, index=False)

with open(json_out, "w", encoding="utf-8") as out_file:
    for movie in movies_json:
        out_file.write(json.dumps(movie) + "\n")

print(f"Saved dataset to:\n  {csv_out}\n  {json_out}")
print(df.head())