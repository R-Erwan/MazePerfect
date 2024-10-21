import random
from Cellule import *  # Class cellule
from collections import deque  # Module pour utiliser des piles / files
from matplotlib import pyplot as plt  # Module pyplot pour les affichages de graphiques
from util_aux import rotate_left
from util_aux import rotate_right

class Maze:
    """Class Labyrinthe, représente le labyrinthe, correspond à une matrice de cellules, possèdes des méthodes pour
    modéliser le labyrinthe, généré des labyrinthes et autres"""

    def __init__(self, lig, col):
        """Constructeur de la class, prend en paramètre le nombre de lignes et de colones, initialise la matrice de
        cellules"""
        self.lig = lig
        self.col = col
        self.cells = [[Cellule(i, j) for j in range(col)] for i in range(lig)]
        self.graph = [[[]for j in range(col)]for i in range(lig)]

    def show(self, show=False):
        """Méthode pour afficher une fenêtre pyplot modélisant le labyrinthe, pour tracer les murs en utilisant 2
        double boucles pour parcourir 2 fois toutes les cellules"""
        plt.figure()
        plt.title("Labyrinthe " + str(self.lig) + " par " + str(self.col))  # Affecte un titre
        plt.axis(False)  # Enlever les axes gradués de base sur les fenêtres pyplot
        plt.plot([0, 0, self.col, self.col, 0], [0, self.lig, self.lig, 0, 0], color="#000000")
        # Créer les 4 bordures externes du labyrinthe

        # Affichage des traits horizontaux, on regarde les bords N
        for i in range(self.lig):
            for j in range(self.col):
                if self.cells[i][j].walls['N']:
                    plt.plot([j, j + 1], [i + 1, i + 1], color="#000000")
                    # Trace un trait représentant le mur N de la cellule

        # Affichage des traits verticaux, on regarde les bords E
        for j in range(self.col):
            for i in range(self.lig):
                if self.cells[i][j].walls['E']:
                    plt.plot([j + 1, j + 1], [i, i + 1], color="#000000")
                    # Trace un trait représentant le mur N de la cellule

        plt.plot([self.col, self.col], [1, 0], color="#ffffff")  # Supprime le mur de l'entrée
        plt.plot([0, 1], [self.lig, self.lig], color="#ffffff")  # Supprime le mur de la sortie
        plt.savefig('maze_bg')

        if show: plt.show()

    def neighbor(self, cel: Cellule) -> list[Cellule]:
        """Méthode qui retourne toutes les cellules voisines de la cellule en param"""
        liste_v = []  # Liste des cellules voisines
        lig = cel.lig  # coordonné ligne de la cel
        col = cel.col  # coordonné ligne de la cel

        if lig - 1 >= 0:  # Regarde si la cellule en bas est possible
            liste_v.append(self.cells[lig - 1][col])
        if lig + 1 < self.lig:  # Regarde si la cellule en haut est possible
            liste_v.append(self.cells[lig + 1][col])
        if col - 1 >= 0:  # Regarde si la cellule à gauche est possible
            liste_v.append(self.cells[lig][col - 1])
        if col + 1 < self.col:  # Regarde si la cellule à droite est possible
            liste_v.append(self.cells[lig][col + 1])
        return liste_v

    def possible_adjoining(self, cell: Cellule) -> list[Cellule]:
        """Retourne un tableau des cellules adjointes où l'on peut se déplacer à partir de la cellule en param"""
        list_adj = self.neighbor(cell)  # On récupère la liste des cellules voisines
        list_possible_adj = []  # Liste retourner
        for c in list_adj:  # On parcourt cette liste de cel voisines
            share_wall = self.share_wall(cell, c)  # On récupère le(s) murs partager entre ces deux cellules
            if not cell.walls[share_wall[0]]:  # Si le mur est a False (il y a un passage)
                list_possible_adj.append(c)  # On ajoute cette cellule dans la liste
        return list_possible_adj

    def uncheck_neighbor(self, cel: Cellule) -> list[Cellule]:
        """Méthode qui retourne une liste de cellules voisines non visitée à partir d'une cellule"""
        liste_v = self.neighbor(cel)  # Liste des cellules voisines
        l_uncheck = []  # liste des cellules non visitée
        for e in liste_v:  # boucle sur chaque cellule de la liste
            if not e.visit:  # si la cellule n'a pas été visité
                l_uncheck.append(e)  # on l'ajoute dans la liste
        return l_uncheck

    def share_wall(self, c1: Cellule, c2: Cellule) -> (str, str):
        """Méthode qui retourne les murs en communs entre deux cellules"""
        if c1.lig == c2.lig:  # Si les cellules sont sur la même ligne
            if c1.col == c2.col + 1:  # Est-ce que c2 est positionné à GAUCHE de c1 ?
                return 'W', 'E'
            else:  # Alors c2 est positionné à DROITE de c1
                return 'E', 'W'
        elif c1.lig == c2.lig + 1:  # Les cellules sont donc sur la même colonne, est-ce que c2 est EN BAS de c1 ?
            return 'S', 'N'
        else:  # Alors c2 est EN HAUT de c1
            return 'N', 'S'

    def sup_share_wall(self, c1: Cellule, c2: Cellule):
        """Méthode pour supprimer le mur partagé/en commun entre deux cellules passé en paramètre"""
        m1, m2 = self.share_wall(c1, c2)
        c1.walls[m1] = False
        c2.walls[m2] = False
    def generation_exhaustive(self):  # time 0.16
        """Algorithme de génération de labyrinthe par la méthode d'exploration exhaustive, version itérative Principe
        : On part de la cellule de départ et on explore aléatoirement une voisine non visitée, s'il n'y en a pas, on
        revient en arrière jusqu'à avoir tout exploré au moin une fois"""
        pile = deque()  # Initialisation d'une pile pour stocker les cell rencontrées dont on va regarder les voisins
        pile.append(self.cells[self.lig - 1][0])
        self.cells[self.lig-1][0].visit=True# On initialise la pile avec la cellule de départ
        while len(pile) > 0:  # Boucle tant qu'il reste des cellules à explorer
            c = pile[-1]  # c: c'est la cellule courante, c'est la première de la pile
            l_voisins_uncheck = self.uncheck_neighbor(c)  # On récupère toutes les cellules voisines non visitées à c.
            if len(l_voisins_uncheck):  # S'il y a des cellules voisines à visiter
                voisin = random.choice(l_voisins_uncheck)  # On choisit un voisin aléatoire
                self.sup_share_wall(c, voisin)  # On supprime le mur en commun entre le voisin et la cellule courante
                #  AJOUTE LE VOISIN AU GRAPH DE C
                self.graph[c.lig][c.col].append(voisin)
                #  IMPORTANT A EXPLIQUER RAPPORT
                voisin.visit = True  # On affecte l'attribut visite de la cellule visite à True
                pile.append(voisin)  # On ajoute la cellule dans la pile
            else:  # Si il n'y as pas de cellule voisines non visite
                pile.pop()  # On dépile la 1ʳᵉ cellule de la pile

    def solve_rh(self) -> (list[(Cellule, Cellule)], list[str]):
        """Algorithme pour parcours le labyrinthe en utilisant la stratégie de la main droite"""
        directions = deque(['S', 'W', 'N', 'E'])  # Liste des directions possibles
        current_c = self.cells[self.lig - 1][0]  # Cellule courante, initialisé avec la cellule d'entrée
        path = [(current_c.lig,
                 current_c.col)]  # Liste pour enregistrer le chemin parcourut, tuples avec les coordonnées des cell
        path_dir = []  # Liste avec des lettres représentant le chemin parcourut utilisé pour animer le chemin
        while current_c != self.cells[0][self.col - 1]:  # Boucle tant que l'on n'est pas arrivé à la cellule de sortie
            next_d = directions[0]  # Prochaine direction à regarder
            next_c = None
            if next_d == 'E' and not current_c.walls[
'E'] and current_c.col + 1 < self.col:  # Regarde si on peut aller à droite :
                # On peut si : la prochaine direction est E ET s'il n'y a pas de murs à droite ET si on ne sort pas des limite du labyrinthe
                next_c = self.cells[current_c.lig][current_c.col + 1]  # la prochaine cell est donc la cell à droite
            elif next_d == 'S' and not current_c.walls[
                'S'] and current_c.lig - 1 >= 0:  # ...ect pour toutes les directions
                next_c = self.cells[current_c.lig - 1][current_c.col]
            elif next_d == 'W' and not current_c.walls['W'] and current_c.col - 1 >= 0:
                next_c = self.cells[current_c.lig][current_c.col - 1]
            elif next_d == 'N' and not current_c.walls['N'] and current_c.lig + 1 < self.lig:
                next_c = self.cells[current_c.lig + 1][current_c.col]

            if next_c:  # Est-ce que l'on a trouvé une cell où aller ?
                current_c = next_c  # Update de la cel courante
                rotate_right(directions)  # On tourne la liste de direction à droite cf. util_aux.js
                path.append((current_c.lig, current_c.col))  # Ajoute la cellule parcourut dans la list path
                path_dir.append(next_d)  # Ajoute la direction du trajet
            else:
                rotate_left(directions)  # On tourne la liste de direction à gauche cf. util_aux.js
        path.append((current_c.lig, current_c.col))  # On ajoute la cellule de sortie
        path_dir.append('E')  # On ajoute la dernière direction
        return path, path_dir

    def calc_dist_graph(self) -> list[[int]]:
        """Retourne une matrice des distances entre la cellule de départ et de sortie,
        fait référence à l'algo de parcours en largeur dist_bfs vus dans le cours sur les graph"""
        # [ [int, int, int], [int, int, int] ...]
        # INITIALISATION
        cel = self.cells[self.lig - 1][0]  # Cellule de départ
        # graph = self.create_graph()  # Graph représentant le labyrinthe
        graph = self.graph
        dist = [[-1 for j in range(self.col)] for i in range(self.lig)]  # Matrice des distances avec -1 partout
        dist[cel.lig][cel.col] = 0  # La distance de la cell de départ = 0
        visit = deque()  # File pour stocker les cell à parcourir
        visit.append(cel)  # On enfile la cellule de départ

        while len(visit) > 0:  # Boucle tant qu'il y a des cellules dans la file à visiter
            cel = visit.popleft()  # Defile la file
            for v in graph[cel.lig][cel.col]:  # Boucle sur tous les voisins de la cellule
                if dist[v.lig][v.col] == -1:  # Si sa distance n'a pas été calculée, 1ʳᵉ fois qu'on la rencontre
                    dist[v.lig][v.col] = dist[cel.lig][
                                             cel.col] + 1  # On calcule sa distance par rapport à la cell de départ
                    if v == self.cells[0][self.col - 1]:  # S'il s'agit de la cellule de sortie
                        return dist  # On est stop et on sort de la fonction en retournant la matrice de distance
                    visit.append(v)  # Ajoute le voisin à la file
        return dist  # Si on arrive ici, c'est que l'on a jamais atteint la cellule de sortie (N.B. possible ?)

    def solve_dist(self) -> (list[(Cellule, Cellule)], list[str]):
        """Calcul et retourne un chemin pour sortir du labyrinthe à partir d'une matrice de distance,
        on part de la cellule de sortie qui est connu, et on remonte la matrice de distance dans l'ordre décroissant,
        on remonte le labyrinthe depuis la sortie"""
        # INITIALISATION
        dist = self.calc_dist_graph()  # Matrice de distances
        path = []  # List représentant le chemin parcourut avec des tuples pour chaque cellule parcourut
        path_dir = []  # List représentant les directions empreinté
        cel = self.cells[0][self.col - 1]  # Cellule de sortie
        dist_courante = dist[cel.lig][cel.col]  # Distance courante
        while dist_courante != 0:  # Boucle tant que la distance ne vaut pas 0, i.e, on est à la cellule de départ
            voisins = self.possible_adjoining(cel)  # List des voisins possibles de la cel courante
            for v in voisins:  # Boucle sur tous les voisins
                if dist[v.lig][v.col] == dist_courante - 1:  # Si la dist du voisin = la dist de la c_courante -1
                    path.append((cel.lig, cel.col))  # Ajoute la cel_courante à path
                    path_dir.append(self.share_wall(cel, v)[1])  # Ajoute la direction empreinté
                    cel = v  # La cellule courante devient ce voisin
                    dist_courante -= 1  # La distance courante diminue de 1

        path.append((cel.lig, cel.col))  # Ajoute la dernière cellule i.e la cellule d'entrée
        path.reverse()  # Inverse path
        path_dir.reverse()  # Inverse path_dir
        path_dir.append('E')  # Ajoute à path_dir la dernière direction
        return path, path_dir

    def solve_random2(self):
        current_cell = self.cells[self.lig - 1][0]  # Cellule courante = cellule de départ
        path = [(current_cell.lig, current_cell.col)] #
        path_dir = []

        while current_cell != self.cells[0][self.col - 1]: # Tant que l'on n'est pas à la sortie
            possible_cell = self.possible_adjoining(current_cell)  # liste des cellules possibles
            if possible_cell:
                next_cell = random.choice(possible_cell)
                path.append((next_cell.lig, next_cell.col))
                path_dir.append(self.share_wall(current_cell, next_cell)[0])
                current_cell = next_cell
            else:
                path.pop()
                path_dir.pop()
                current_cell = self.cells[path[-1][0]][path[-1][1]]
        path_dir.append("E")
        return path,path_dir

    # def solve_random3(self):
    #     c_c = self.cells[self.lig - 1][0]
    #     path = [c_c.lig][c_c.col]
    #     path_dir = []
    #     dir = {'S','E','W','N'}
    #     last_dir = []
    #     c_dir = ['S']
    #
    #     while c_c != self.cells[0][self.col -1]:






    # def get_dead_end(self):
    #     dead_end = []
    #     for l in range(self.lig):
    #         for c in range(self.col):
    #             if len(self.graph[l][c]) < 1:
    #                 dead_end.append(self.cells[l][c])
    #     return dead_end
    # def solve_dead_end(self):
    #     dead_end = self.get_dead_end()
    #     while len(dead_end) > 0:
    #         for d in dead_end:
    #             d.walls = {'N': True, 'E': True, 'S': True,'W': True}
    #             dead_end = self.get_dead_end()
    #     return dead_end


