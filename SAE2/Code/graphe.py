class Pile:
  def __init__(self, liste):
    self.liste = liste

  def est_vide(self):
    return len(self.liste) == 0

  def Empile(self, element):
    self.liste.append(element)

  def Depile(self):
    if self.est_vide():
      raise IndexError("La pile est vide")
    return self.liste.pop()
  

class graphe:

  def __init__(self):
    self._graphe = {}

  def ajouter_sommet(self, sommet):
    self._graphe[sommet] = []

  def ajouter_arete(self, s1, s2, poids):
    if s2 not in self._graphe[s1]:
      self._graphe[s1].append((s2,poids))
    if s1 not in self._graphe[s2]:
      self._graphe[s2].append((s1,poids))

  def parcours_profondeur(self, sommet_depart):
    pile = Pile([])
    pile.Empile(sommet_depart)
    marques = set()
    ordre_marq = []
    while not pile.est_vide():
      sommet = pile.Depile()
      if sommet not in marques:
        marques.add(sommet)
        ordre_marq.append(sommet)
        for voisin in reversed(self.DonneSommetsAdjacents(sommet)):
          if voisin not in marques:
            pile.Empile(voisin)
    return ordre_marq

  def Ordre(self):
    x = 0
    for _ in self._graphe.keys():
      x += 1
    return x

  def DonneSommetsAdjacents(self, s):
    retour = []
    if s in self._graphe:
      retour = [i[0] for i in self._graphe[s]]
    return retour


  def Matrice_Adjacente(self):
    M = [[0 for _ in range(self.Ordre())] for _ in range(self.Ordre())]
    # grande liste contenant des petites listes (=> les lignes)
    # toutes les lignes sont initialisées à 0
    ListeSommets = list(self._graphe.keys())

    for s in ListeSommets:
      indexSommet = ListeSommets.index(s)
      SommetsAdjacents = self.DonneSommetsAdjacents(s)

      for a in SommetsAdjacents:
        indexAdjacent = ListeSommets.index(a)
        M[indexSommet][indexAdjacent] = 1
    return M

  def Jarnik_Prim(self, sommet_debut):
    sommet = sommet_debut
    liste_arete_admiss = []
    graphe = [sommet]
    arbre_couvrant = []  # Liste des arêtes de l'ACM
    poids = 0

    for _ in range(self.Ordre()-1): # on boucle n-1 fois

        for voisin, poids_arete in self._graphe[sommet]: # liste des aretes admissibles
            if voisin not in graphe:
                liste_arete_admiss.append((sommet, voisin, poids_arete))
        
        for i in range(1, len(liste_arete_admiss)): # tri des aretes
            for j in range(1, len(liste_arete_admiss)):
              tmp = ""
              if liste_arete_admiss[i][0] < liste_arete_admiss[j][0]:
                tmp = liste_arete_admiss[j]
                liste_arete_admiss[j] = liste_arete_admiss[i]
                liste_arete_admiss[i] = tmp

        min = liste_arete_admiss[0] # arete de poids minimal
        for i in liste_arete_admiss:
          if min[2] > i[2]:
            min = i

        graphe.append(min[1])
        arbre_couvrant.append((min[0], min[1], min[2]))
        poids += min[2]

        sommet = min[1]
        liste_arete_admiss = [a for a in liste_arete_admiss if a[1] not in graphe]

    return graphe, arbre_couvrant, poids

 # --------- AFFICHAGE (pas utile donc) ----------#

  def afficher(self):
    print(self._graphe)

  def donne_sommets_adjacents(self, S):
    if S in self._graphe:
      print("les sommets adjacents de", S, "sont :")
      for i in self._graphe[S]:
        print(i[0])

  def DonneDegre(self, S):
    if S in self._graphe:
      x = 0
      for _ in self._graphe[S]:
        x += 1
    return x


# G = graphe()
# G.ajouter_sommet("A")
# G.ajouter_sommet("B")
# G.ajouter_sommet("C")
# G.ajouter_sommet("D")
# G.ajouter_sommet("E")
# G.ajouter_sommet("F")
# G.ajouter_sommet("G")
# G.ajouter_sommet("H")

# G.ajouter_arete("A", "B", 2)
# G.ajouter_arete("A", "D", 8)
# G.ajouter_arete("A", "G", 9)
# G.ajouter_arete("B", "F", 1)
# G.ajouter_arete("C", "D", 1)
# G.ajouter_arete("C", "F", 5)
# G.ajouter_arete("C", "H", 2)
# G.ajouter_arete("D", "C", 1)
# G.ajouter_arete("D", "G", 2)
# G.ajouter_arete("E", "B", 5)
# G.ajouter_arete("E", "G", 3)
# G.ajouter_arete("F", "C", 1)
# G.ajouter_arete("F", "D", 4)
# G.ajouter_arete("G", "A", 2)

# G.afficher()
# print("L'ordre du graphe est :",G.Ordre())
# G.donne_sommets_adjacents("B")
# print("Le degré du sommet A est",G.DonneDegre("A"))
# for i in G.Matrice_Adjacente():
#   print(i)
# for i in G.Jarnik_Prim("F"):
#   print(i)
# print(G.parcours_profondeur("A"))
