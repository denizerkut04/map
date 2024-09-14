import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import heapq
from turkiye import data_turkiye

# Points from the 'data_turkiye' dataset
points = np.array([[d['lon'], d['lat']] for d in data_turkiye])

# Delaunay triangulation
tri = Delaunay(points)

# Adjacency matrix for each node
adj = {}
for i, d in enumerate(data_turkiye):
    adj[i] = []
    for j, s in enumerate(tri.simplices):
        if i in s:
            for k in s:
                if k != i:
                    adj[i].append(k)
    adj[i] = list(set(adj[i]))
    adj[i].sort()

# Add adjacency data to 'data_turkiye'
for i, d in enumerate(data_turkiye):
    d['adjacency'] = adj[i]

# Function to calculate distance between two points
def distance(p1, p2):
    return np.linalg.norm(points[p1] - points[p2])

# Function to get shortest path using Dijkstra
def dijkstra(start, end):
    queue = [(0, start, [])]  # (cost, node, path)
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return cost, path
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + distance(node, neighbor), neighbor, path))
    return float("inf"), []

# Function to find alternative path by avoiding one edge from the shortest path
def find_alternative_path(shortest_path, start, end):
    for i in range(len(shortest_path) - 1):
        avoid_edge = (shortest_path[i], shortest_path[i+1])

        # Remove the edge by temporarily modifying the adjacency matrix
        original_neighbors = adj[avoid_edge[0]][:]
        if avoid_edge[1] in adj[avoid_edge[0]]:
            adj[avoid_edge[0]].remove(avoid_edge[1])
        if avoid_edge[0] in adj[avoid_edge[1]]:
            adj[avoid_edge[1]].remove(avoid_edge[0])

        # Run Dijkstra again
        cost, alternative_path = dijkstra(start, end)

        # Restore the edge
        adj[avoid_edge[0]] = original_neighbors

        if alternative_path and alternative_path != shortest_path:
            return cost, alternative_path
    return None, None

# Find shortest path from index 0 to index 33
start, end = 21, 29
shortest_cost, shortest_path = dijkstra(start, end)

# Find an alternative path by avoiding one of the edges in the shortest path
alternative_cost, alternative_path = find_alternative_path(shortest_path, start, end)

# Plotting Delaunay triangulation
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'o')

# Plotting the shortest path in red
for i in range(len(shortest_path) - 1):
    p1 = shortest_path[i]
    p2 = shortest_path[i + 1]
    plt.plot([points[p1, 0], points[p2, 0]], [points[p1, 1], points[p2, 1]], 'r', label='Shortest Path' if i == 0 else "")

# Plotting the alternative path in blue (if available)
if alternative_path:
    for i in range(len(alternative_path) - 1):
        p1 = alternative_path[i]
        p2 = alternative_path[i + 1]
        plt.plot([points[p1, 0], points[p2, 0]], [points[p1, 1], points[p2, 1]], 'b--', label='Alternative Path' if i == 0 else "")

# Add legends and limits
plt.legend()
plt.xlim(25, 45)
plt.ylim(35, 45)
plt.show()

# Print the paths with node count and total distance
print("Shortest Path:", shortest_path)
print("Node count in shortest path:", len(shortest_path))
print("Total distance in shortest path:", shortest_cost)

if alternative_path:
    print("Alternative Path:", alternative_path)
    print("Node count in alternative path:", len(alternative_path))
    print("Total distance in alternative path:", alternative_cost)
else:
    print("No alternative path found.")
