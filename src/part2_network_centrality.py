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

def nc():

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
    print(f"\nUsing dataset: {latest_json}")

    # Store actor pairs for CSV output
    actor_pairs = []

    # Read dataset line by line
    with open(latest_json, "r", encoding="utf-8") as in_file:
        for line in in_file:
            movie = json.loads(line)

            # Skip if no actors listed
            if 'actors' not in movie or not movie['actors']:
                continue

            # Extract actor names
            actor_names = [name for _, name in movie['actors']]

            # Add each actor as a node
            g.add_nodes_from(actor_names)

            # Generate all unique pairs of actors
            for i, left_actor in enumerate(actor_names):
                for right_actor in actor_names[i+1:]:
                    # Increment edge weight if it exists, else create edge
                    if g.has_edge(left_actor, right_actor):
                        g[left_actor][right_actor]['weight'] += 1
                    else:
                        g.add_edge(left_actor, right_actor, weight=1)

                    # Store pair for CSV
                    actor_pairs.append({
                        'left_actor_name': left_actor,
                        '<->': '<->',
                        'right_actor_name': right_actor
                    })

    # Print graph info
    print("Nodes:", len(g.nodes))
    degree_centrality = nx.degree_centrality(g)

    # Top 10 most central actors
    print("\nTop 10 Most Central Actors:")
    for actor, centrality in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{actor}: {centrality:.4f}")

    # Save actor pairs to CSV
    df_pairs = pd.DataFrame(actor_pairs)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(data_dir, f'network_centrality_{timestamp}.csv')
    df_pairs.to_csv(output_path, index=False)

    print(f"\nNetwork centrality data saved to: {output_path}")
