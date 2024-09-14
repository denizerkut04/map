import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
from turkiye import data_turkiye

# Extract the points from data_turkiye
points = np.array([[d['lon'], d['lat']] for d in data_turkiye])

# Add points to data_turkiye
for i, d in enumerate(data_turkiye):
    d['coordinates'] = points[i].tolist()

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

# Add adjacency to data_turkiye
for i, d in enumerate(data_turkiye):
    d['adjacency'] = adj[i]

# Voronoi tessellation
vor = Voronoi(points)

# Plot the Delaunay triangulation, Voronoi diagram, and Delaunay edges as lines
plt.figure(figsize=(10, 10))

# Plot the points
plt.plot(points[:, 0], points[:, 1], 'o', color='red', label="Points")

# Plot the Delaunay triangles
plt.triplot(points[:, 0], points[:, 1], tri.simplices, color='blue', alpha=0.5, label="Delaunay Triangulation")

# Plot the Voronoi diagram
voronoi_plot_2d(vor, show_vertices=False, line_colors='green', line_width=1.5, line_alpha=0.6, point_size=2)

# Plot Delaunay edges as individual lines
for simplex in tri.simplices:
    for i in range(3):
        p1 = points[simplex[i]]
        p2 = points[simplex[(i + 1) % 3]]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-', lw=1)  # Draw line between points p1 and p2

# Set axis limits
plt.xlim(25, 45)
plt.ylim(35, 45)
plt.legend()
plt.show()
