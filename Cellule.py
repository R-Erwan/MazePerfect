class Cellule:
    """Class cellule, représentant les case de labyrinthe,
    avec 4 cotés ouvert ou fermé"""

    def __init__(self, lig=0, col=0):
        """Constructeur de la classe, prend en paramètre les coordonnée de la cellule dans le labyrinthe"""

        self.lig = lig  # coordonnée représentant la ligne, axe des ordonnées
        self.col = col  # coordonnée représentant la colonne de la cellule, axe des abscisses
        self.walls = {'N': True, 'E': True, 'S': True,
                      'W': True}  # Dictionnaire orientation → booléen, représente si une cellule a un mur
        self.visit = False  # booléen pour savoir si la cellule a été visité lors de la génération

    def __str__(self):
        """Overwrite de la méthode pour print la cellule en console"""

        s = '{' + str(self.lig) + ',' + str(self.col)
        if self.walls['N']:
            s += ',N'
        if self.walls['E']:
            s += ',E'
        if self.walls['S']:
            s += ',S'
        if self.walls['W']:
            s += ',W'
        s += '}'
        return s
