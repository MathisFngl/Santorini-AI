tableau_de_jeu = [[0 for i in range(5)] for j in range(5)]
for li in tableau_de_jeu:
    print(li)


class Pion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def build(X,Y):
        if tableau_de_jeu[X][Y] < 4:
            tableau_de_jeu[X][Y] += 1


class Joueur:
    def __init__(self, name, dieu):
        self.name = name
        self.pion1 = Pion.__init__(self, 0, 0)
        self.pion2 = Pion.__init__(self, 0, 1)

        self.pouvoir_de_dieu = dieu


