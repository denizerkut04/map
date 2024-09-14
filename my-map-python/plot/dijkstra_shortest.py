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

# Dijkstra's algorithm to find shortest path
def dijkstra(start, end):
    queue = [(0, start, [])]
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

# Find shortest path from index 0 to index 33
start, end = 21, 29
_, shortest_path = dijkstra(start, end)

# Plotting Delaunay triangulation
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'o')

# Plotting the shortest path in red
for i in range(len(shortest_path) - 1):
    p1 = shortest_path[i]
    p2 = shortest_path[i + 1]
    plt.plot([points[p1, 0], points[p2, 0]], [points[p1, 1], points[p2, 1]], 'r')

# Eksenlerin limitleri
plt.xlim(25, 45)
plt.ylim(35, 45)
plt.show()
