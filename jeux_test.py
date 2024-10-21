from Maze import *
from util_aux import maze_anim
"""Ce script comporte des jeux de test a appelé pour tester toutes les fonctionnalité du projet"""


def test_affichage():
    maze = Maze(10,10)
    maze.show(True)


def test_generation_exhaustive():
    maze = Maze(50,50)
    maze.generation_exhaustive()
    maze.show(True)


def test_solve_rh():
    maze = Maze(15,15)
    maze.generation_exhaustive()
    path,path_dir = maze.solve_rh()
    print("Chemin :",len(path))
    print(path)
    maze_anim(maze,[path_dir],["#ff0088"],7)


def test_solve_dist():
    maze = Maze(30,30)
    maze.generation_exhaustive()
    path,path_dir = maze.solve_dist()
    print("Chemin :",len(path))
    print(path)
    maze_anim(maze,[path_dir],["#DB5461"],0)

def test_solve_random():
    maze = Maze(10,10)
    maze.generation_exhaustive()
    path,path_dir = maze.solve_random2()
    print("Chemin :", len(path))
    print(path)
    maze_anim(maze, [path_dir], ["#00ff00"], 0)

def test_multi():
    maze = Maze(30,30)
    maze.generation_exhaustive()
    path,path_dir = maze.solve_rh()
    path2,path_dir2 = maze.solve_dist()
    print("Chemin RH : ", len(path))
    print("Chemin DIST : ", len(path2))
    maze_anim(maze, [path_dir,path_dir2], ["#00ff00","#0055ff"], 0)



