'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json
import os
from datetime import datetime

# Build the graph
g = nx.Graph()

# Paths
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')

# Find latest JSON file in /data
json_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
if not json_files:
    raise FileNotFoundError("No JSON dataset found in /data. Run Part 1 ETL first.")

latest_json = max(
    [os.path.join(data_dir, f) for f in json_files],
    key=os.path.getctime
)

print(f"Using dataset: {latest_json}")

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'
actor_pairs = []

with open(latest_json, "r", encoding="utf-8") as in_file:
    # Don't forget to comment your code
    for line in in_file:
        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Skip if no actors listed
        if 'actors' not in this_movie or not this_movie['actors']:
            continue
        
        # Create a node for every actor
        for actor_id,actor_name in this_movie['actors']:
        # add the actor to the graph   
            g.add_node(actor_name)
             
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
        i = 0 #counter
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:

                # Get the current weight, if it exists
                if g.has_edge(left_actor_name, right_actor_name):
                    g[left_actor_name][right_actor_name]['weight'] += 1
                # Add an edge for these actors
                else:
                    g.add_edge(left_actor_name, right_actor_name, weight=1)
                
                # Store this pair for CSV output
                actor_pairs.append({
                    'left_actor_name': left_actor_name,
                    '<->': '<->',
                    'right_actor_name': right_actor_name
                })
            i += 1
                
# Print the info below
print("Nodes:", len(g.nodes))
degree_centrality = nx.degree_centrality(g)

#Print the 10 the most central nodes
print("\nTop 10 Most Central Actors:")
top_10 = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
for actor, centrality in top_10:
    print(f"{actor}: {centrality:.4f}")

# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
df_pairs = pd.DataFrame(actor_pairs)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(data_dir, f'network_centrality_{timestamp}.csv')
df_pairs.to_csv(output_path, index=False)

print(f"\nNetwork centrality data saved to: {output_path}")
