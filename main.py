tableau_de_jeu = [[0 for i in range(5)] for j in range(5)]
PlayerList = []
for li in tableau_de_jeu:
    print(li)


class Pion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isValidBuilding(self, x, y, player_list):
        if not (0 <= x < 5 and 0 <= y < 5):
            print("Cannot Build Here : Out of Bounds")
            return False
        if not abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
            print("Cannot Build Here: Cannot build further than 1 square away.")
            return False
        for player in player_list:
            if (player.pion1.x == x and player.pion1.y == y) or (player.pion2.x == x and player.pion2.y == y):
                print("Cannot Build Here: A builder is on this square.")
                return False
        if tableau_de_jeu[x][y] >= 4:
            print("Cannot Build Here: Cannot build on a dome.")
            return False
        return True

    def build(self, x_build, y_build):
        if self.isValidBuilding(x_build, y_build, PlayerList):
            tableau_de_jeu[x_build][y_build] += 1


class Joueur:
    def __init__(self, name, dieu):
        self.name = name
        self.pion1 = Pion(0, 0)
        self.pion2 = Pion(1, 1)
        self.pouvoir_de_dieu = dieu


Joueur_1 = Joueur("Antoine", "Rebelle")
Joueur_2 = Joueur("Alexis", "Raiponse")
PlayerList.append(Joueur_1)
PlayerList.append(Joueur_2)

Joueur_1.pion1.build(0, 1)

print()
for li in tableau_de_jeu:
    print(li)
