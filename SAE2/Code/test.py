from graphe import *

import pandas as pd
import numpy as np
import scipy.spatial as sp
import matplotlib.pyplot as plt
import folium as f

def ouvrir(chemin):
        df_JSON = pd.read_json(chemin)
        arr = np.array(df_JSON)
        return arr

lien = "C:/Users/but-info/OneDrive - UPEC/Documents/Cours BUT1/semestre2/SAE2/station_information.json"
fichier = ouvrir(lien)
# nb de stations -> 1471

class coor:

    def __init__ (self, i):
         self.lat = fichier[0][2][i]["lat"]
         self.lon = fichier[0][2][i]["lon"]

    def get_coord(self):
          return [self.lat, self.lon]
        

liste = []
for i in range(len(fichier[0][2])):
      objet = coor(i)
      liste.append(objet.get_coord())

points = np.array(liste)

G = graphe()

tri = sp.Delaunay(points)
#print(tri.simplices[0][0], tri.simplices[0][1])

for i in range(0, 3):
     G.ajouter_sommet(int(tri.simplices[0][i]))

for i in G._graphe:
     for j in G._graphe:
          if j != i:
            G.ajouter_arete(i, j, 1)

for i in G._graphe:
    unique_edges = set(G._graphe[i])
    G._graphe[i] = list(unique_edges)

G.afficher()

plt.triplot(points[:,0], points[:,1], tri.simplices)
plt.plot(points[:,0], points[:,1], 'o')
#plt.show()

#for i in range(len(fichier[0][2])):
#      print(fichier[0][2][i]['name'])

m = f.Map(location=[np.mean(points[:,0]), np.mean(points[:,1])], zoom_start=12, popup="", legend_name="Velib_station")

for coord in points:
    f.Marker(location=[coord[0], coord[1]]).add_to(m)

for simplex in tri.simplices:
    pts = [points[i] for i in simplex] + [points[simplex[0]]]
    f.PolyLine(pts, color="red", weight=1.5, opacity=0.8).add_to(m)

m.save("map.html")

#print("Carte générée : ouvrez 'map.html' dans un navigateur.")