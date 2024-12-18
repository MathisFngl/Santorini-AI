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
            if self.player.name != "AI" or self.player.name != "QLearningAgent":
                print("Cannot Build Here: Out of Bounds")
            return False
        for player in self.player.game.players:
            if (player.pion1.x == new_x and player.pion1.y == new_y) or (
                    player.pion2.x == new_x and player.pion2.y == new_y):
                if self.player.name != "AI" or self.player.name != "QLearningAgent":
                    print("Cannot Build Here: A builder is on this square.")
                return False
        if self.player.game.tableau_de_jeu[new_x][new_y] >= 4:
            if self.player.name != "AI" or self.player.name != "QLearningAgent":
                print("Cannot Build Here: Cannot build on a dome.")
            return False
        if self.player.game.tableau_de_jeu[new_x][new_y] + 1 > 4:
            print("\n\n\nNOOOOOOO \n\n\n.")
            if self.player.name != "AI" or self.player.name != "QLearningAgent":
                print("Cannot Build Here: Cannot build higher than 3.")
            return False
        return True

    def build(self, x_build, y_build):
        print("Building for ", self.player.name)
        print("building x : ", x_build)
        print("building y : ", y_build)
        new_x = self.x + x_build
        new_y = self.y + y_build
        print("new_x : ", new_x)
        print("new_y : ", new_y)
        print("stage : ", self.player.game.tableau_de_jeu[new_x][new_y] + 1)
        if self.player.game.tableau_de_jeu[new_x][new_y] + 1 > 4:
            print("\n\n\nJOSHUA \n\n\n.")
        if 0 <= new_x < 5 and 0 <= new_y < 5:
            self.player.game.tableau_de_jeu[new_y][new_x] += 1
            print("debug build")
            self.player.game.printBoard()
        else:
            if self.player.name != "AI" or self.player.name != "QLearningAgent":
                print("Cannot Build Here: Out of Bounds")

    def pionCopy(self):
        new_player = self.player
        new_x = self.x
        new_y = self.y
        new_pionID = self.pionID
        return Pion(new_player, new_x, new_y, new_pionID)

    def getCoordinates(self):
        return int(self.x), int(self.y)

    def getHeight(self):
        return self.player.game.tableau_de_jeu[self.x][self.y]