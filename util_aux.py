import turtle
from collections import deque
from turtle import Turtle
import Maze

LARGEUR_LAB = 335
LONGUEUR_LAB = 450
IMAGE_BG = "maze_bg.png"


def rotate_right(d: deque):
    """Méthode pour 'tourner' une deque vers la droite"""
    t = d.popleft()
    d.append(t)


def rotate_left(d: deque):
    """Méthode pour 'tourner' une deque vers la gauche"""
    t = d.pop()
    d.appendleft(t)


def maze_anim(maze: Maze, path: list[list], color=list[str], speed=7, ):
    """Fonction pour afficher le labyrinthe et animer 1 ou plusieurs turtle qui suivent un chemin path_dir"""
    maze.show()  # Génère l'affichage pyplot du labyrinthe
    nl = maze.lig  # Nombre de lignes
    nc = maze.col  # Nombre de col
    turtle.Screen().bgpic(IMAGE_BG)  # Affecte comme image de fond à la fenêtre turtle l'image du labyrinthe
    lar_cell = LARGEUR_LAB / nl  # Largeur d'une cellule
    long_cell = LONGUEUR_LAB / nc  # Longueur d'une cellule
    cpt = -1  # Compteur des tortues
    for pa in path:  # Pour chaques trajet différent
        cpt += 1
        t = Turtle()  # Créer une tortue
        t.penup()  # Lève le stylo
        t.goto((-440 / 2) + long_cell / 2,
               (330 / 2) - lar_cell / 2)  # Initialise la position de la tortue a la 1ère cellule
        t.pendown()  # Baisse le stylo
        t.color(color[cpt])  # Affect ela couleur
        t.shapesize(1)  # Taille du stylo
        t.speed(speed)  # Vitesse de déplacement de la tortue
        for p in pa:  # Pour chaques direction dans la liste path_dir
            if p == 'S':  # Si la direction est S
                if t.heading() != 270:  # Si la tortue ne regarde pas en bas
                    t.setheading(270)  # On l'oriente vers le bas
                t.forward(lar_cell)  # On avance de la largeur d'une cellule
            if p == 'N':  # ... ... ...
                if t.heading() != 90:
                    t.setheading(90)
                t.forward(lar_cell)
            if p == 'W':
                if t.heading() != 180:
                    t.setheading(180)
                t.forward(long_cell)
            if p == 'E':
                if t.heading() != 0:
                    t.setheading(0)
                t.forward(long_cell)
    turtle.Screen().mainloop()

# -220 165
