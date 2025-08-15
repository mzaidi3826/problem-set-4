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

# Create '/data' directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_dir, exist_ok=True)

# Load datasets and save to '/data'
url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"

# Extract: load JSON data from the URL
response = requests.get(url)
response.raise_for_status()
movies_json = response.json()

# Transform: convert JSON to DataFrame
movies_df = pd.DataFrame(movies_json)

# Load: save DataFrame to CSV in '/data'
output_path = os.path.join(data_dir, "imdb_movies_2000to2022.csv")
movies_df.to_csv(output_path, index=False)

print(f"Data saved to: {output_path}")
print(movies_df.head())