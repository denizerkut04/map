import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
from turkiye import data_turkiye

points = np.array([[d['lon'], d['lat']] for d in data_turkiye])
#add points to data_turkiye
for i, d in enumerate(data_turkiye):
    d['coordinates'] = points[i].tolist()

# Delaunay üçgenlemesi uygulanıyor
tri = Delaunay(points)

#Adjacency matrix for each node
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
#add adj to data_turkiye
for i, d in enumerate(data_turkiye):
    d['adjacency'] = adj[i]

#add voronoi to data_turkiye

#############################
# Üçgenleri çizdirme
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'o')
# Eksenlerin limitleri
plt.xlim(25, 45)
plt.ylim(35, 45)
plt.show()
