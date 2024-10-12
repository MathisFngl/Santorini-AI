class Pion:
    def __init__(self, player, x, y):
        self.x = x
        self.y = y
        self.player = player

    def isValidBuilding(self, x, y):
        if not (0 <= self.x + x < 5 and 0 <= self.y < 5):
            print("Cannot Build Here : Out of Bounds")
            return False
        for player in self.player.game.players:
            if ((player.pion1.x == self.x + x and player.pion1.y == self.y + y) or
                    (player.pion2.x == self.x + x and player.pion2.y == self.y + y)):
                print("Cannot Build Here: A builder is on this square.")
                return False
        if self.player.game.tableau_de_jeu[x][y] >= 4:
            print("Cannot Build Here: Cannot build on a dome.")
            return False
        return True

    def build(self, x_build, y_build):
        self.player.game.tableau_de_jeu[self.x + x_build][self.y + y_build] += 1
