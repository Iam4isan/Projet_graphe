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

for simplex in tri.simplices:
      for sommet in simplex:
            G.ajouter_sommet(int(sommet))

      for i in range(3):
            for j in range(i + 1, 3): # eviter les doublons
                  s1 = int(simplex[i])
                  s2 = int(simplex[j])
                  G.ajouter_arete(s1, s2, 1)

def indice_repartition(station):
      if G.DonneDegre(station) == 6:
            return 0
      else:
            capa_max = 0 # on determine la capacite max
            for i in range(len(fichier[0][2])):
                  capa_max += fichier[0][2][i]['capacity']
            ind = 0 # on determine d'indice de la station
            for i, j in zip(G._graphe.keys(), range(len(G._graphe))):
                  if i == station:
                        ind = j
            capa = fichier[0][2][ind]['capacity']
            connec = G.DonneDegre(station)
            alpha = 1 # ça rend bien avec 1 \_0_/
            return alpha*((connec-6)/6) + (1-alpha)*((capa_max-capa)/capa_max)

for i in G._graphe:
      print(indice_repartition(i))

# liste_deg = []
# for i in G._graphe:
#       liste_deg.append(G.DonneDegre(i))
# print(np.mean(liste_deg)) # -> revoie environ 6

#print(G._graphe)

# for i in G._graphe:
#       print(i, G._graphe[i])

#print(G.DonneDegre(1143))

plt.triplot(points[:,0], points[:,1], tri.simplices)
plt.plot(points[:,0], points[:,1], 'o')
#plt.show()

m = f.Map(location=[np.mean(points[:,0]), np.mean(points[:,1])], zoom_start=12, popup="", legend_name="Velib_station")

for coord in points:
    f.Marker(location=[coord[0], coord[1]]).add_to(m)

for simplex in tri.simplices:
    pts = [points[i] for i in simplex] + [points[simplex[0]]]
    f.PolyLine(pts, color="red", weight=1.5, opacity=0.8).add_to(m)

m.save("map.html")

#print("Carte générée : ouvrez 'map.html' dans un navigateur.")