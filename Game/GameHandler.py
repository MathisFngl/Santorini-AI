from .Player import Joueur


class Game:
    def __init__(self):
        self.players = []
        self.tableau_de_jeu = [[0 for i in range(5)] for j in range(5)]
        self.play()

    def play(self):
        win = False
        self.choosePlayer()
        while not win:
            for player in self.players:
                print()
                print("Board State :")
                self.printBoard()
                print()
                print(player.name + "'s turn :")
                if player.movementHandler():
                    win = True
                    break
                print()
                print("Board State :")
                self.printBoard()
                print()
                player.buildingHandler()

    def choosePlayer(self):
        player_1 = Joueur(self)
        self.players.append(player_1)
        player_2 = Joueur(self)
        self.players.append(player_2)

    def printBoard(self):
        for row in self.tableau_de_jeu:
            print(row)
        for player in self.players:
            print(f"{player.name}'s pawn 1 : ({player.pion1.x}:{player.pion1.y})")
            print(f"{player.name}'s pawn 2 : ({player.pion2.x}:{player.pion2.y})")

    def is_occupied(self, x, y):
        for player in self.players:
            if (player.pion1.x == x and player.pion1.y == y) or (player.pion2.x == x and player.pion2.y == y):
                return True
        return False
