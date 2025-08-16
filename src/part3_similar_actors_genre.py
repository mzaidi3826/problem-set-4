'''
PART 3: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

import os
import json
import pandas as pd
from datetime import datetime
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances

# Write your code below

# Paths 
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
input_path = os.path.join(data_dir, 'imdb_movies_2000to2022.prolific.json')

# Build actor-genre matrix
actor_genre_counts = {}  # {actor_id: {'name': actor_name, 'genre_counts': {genre: count}}}
all_genres = set()

with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        movie = json.loads(line)

        # Skip movies without required fields
        if 'actors' not in movie or 'genres' not in movie:
            continue

        genres = movie['genres']
        for genre in genres:
            all_genres.add(genre)

        for actor_id, actor_name in movie['actors']:
            if actor_id not in actor_genre_counts:
                actor_genre_counts[actor_id] = {
                    'name': actor_name,
                    'genre_counts': {}
                }
            for genre in genres:
                actor_genre_counts[actor_id]['genre_counts'][genre] = \
                    actor_genre_counts[actor_id]['genre_counts'].get(genre, 0) + 1
                    
# Create dataframe
genre_list = sorted(list(all_genres))
data = []
actor_ids = []

for actor_id, info in actor_genre_counts.items():
    row = [info['genre_counts'].get(genre, 0) for genre in genre_list]
    data.append(row)
    actor_ids.append((actor_id, info['name']))

df_genres = pd.DataFrame(data, columns=genre_list)
df_genres.index = pd.MultiIndex.from_tuples(actor_ids, names=['actor_id', 'actor_name'])

# Similarity calculations 
query_actor_id = "nm1165110"  # Chris Hemsworth
if query_actor_id not in actor_genre_counts:
    raise ValueError("Query actor not found in dataset.")

query_vector = df_genres.loc[query_actor_id].values.reshape(1, -1)

# Cosine distance
cosine_dist = cosine_distances(query_vector, df_genres.values).flatten()
df_genres['cosine_distance'] = cosine_dist

# Euclidean distance
euclidean_metric = DistanceMetric.get_metric('euclidean')
euclidean_dist = euclidean_metric.pairwise(query_vector, df_genres.values).flatten()
df_genres['euclidean_distance'] = euclidean_dist

# Top 10 similar actors 

# Cosine top 10
top_10_cosine = df_genres.sort_values(by='cosine_distance', ascending=True).iloc[1:11]
top_10_cosine_list = [(idx[0], idx[1]) for idx in top_10_cosine.index]

# Euclidean top 10
top_10_euclidean = df_genres.sort_values(by='euclidean_distance', ascending=True).iloc[1:11]
top_10_euclidean_list = [(idx[0], idx[1]) for idx in top_10_euclidean.index]

# Output csv
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(data_dir, f'similar_actors_genre_{timestamp}.csv')
pd.DataFrame(top_10_cosine_list, columns=['actor_id', 'actor_name']).to_csv(output_path, index=False)

print(f"\nTop 10 actors most similar to Chris Hemsworth (Cosine Distance):")
for actor_id, actor_name in top_10_cosine_list:
    print(f"{actor_id} {actor_name}")

print(f"\nTop 10 actors most similar to Chris Hemsworth (Euclidean Distance):")
for actor_id, actor_name in top_10_euclidean_list:
    print(f"{actor_id} {actor_name}")
    
# Compare difference 
diff = set(top_10_cosine_list) ^ set(top_10_euclidean_list)
if diff:
    print("\nDifferences between cosine and euclidean top 10 lists:")
    for actor in diff:
        print(actor)
else:
    print("\nBoth cosine and euclidean top 10 lists are identical.")

print(f"\nSimilar actors (cosine) saved to: {output_path}")
