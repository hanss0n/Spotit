import numpy as np

def distance(track1, track2):
    return np.linalg.norm(np.array(list(track1.values())) - np.array(list(track2.values())))

def build_graph(features):
    edges = {}
    # Go through each track and find its closest neighbour
    for base_track in features.items():
        min_dist = float('inf')
        for reference_track in features.items():
            # We don't want to compare it to itself
            if base_track[0] != reference_track[0]:
                dist = distance(base_track[1], reference_track[1])
                # Keep the closest distance
                if min_dist > dist:
                    min_dist = dist
                    min_id = reference_track[0]
        
        edges[base_track[0]] = min_id
    return edges