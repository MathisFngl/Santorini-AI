class Pion:
    def __init__(self, player, x, y, id):
        self.x = x
        self.y = y
        self.player = player
        self.pionID = id

    def isValidBuilding(self, x, y):
        new_x = self.x + x
        new_y = self.y + y
        if new_x < 0 or new_x >= 5 or new_y < 0 or new_y >= 5:
            if self.player.name != "AI":
                print("Cannot Build Here: Out of Bounds")
            return False
        for player in self.player.game.players:
            if (player.pion1.x == new_x and player.pion1.y == new_y) or (
                    player.pion2.x == new_x and player.pion2.y == new_y):
                if self.player.name != "AI":
                    print("Cannot Build Here: A builder is on this square.")
                return False
        if self.player.game.tableau_de_jeu[new_x][new_y] >= 4:
            if self.player.name != "AI":
                print("Cannot Build Here: Cannot build on a dome.")
            return False
        return True

    def build(self, x_build, y_build):
        new_x = self.x + x_build
        new_y = self.y + y_build
        if 0 <= new_x < 5 and 0 <= new_y < 5:
            self.player.game.tableau_de_jeu[new_x][new_y] += 1
        else:
            print("Cannot Build Here: Out of Bounds")

    def pionCopy(self):
        return Pion(self.player, self.x, self.y, self.pionID)
