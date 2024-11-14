from .Player import Joueur, AIPlayer
import Game.MinMax as MinMax

class Game:
    def __init__(self, skip_initialization=False):
        if not skip_initialization:
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
                if player.name == "AI":
                    print("AI's turn :")
                    if self.ai_turn():
                        win = True
                        break
                    print("AI turn ended")
                else:
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
        print("Enter the name of the second player (or type 'AI' for the AI): ")
        player_2_name = input()
        if player_2_name == "AI":
            player_2 = AIPlayer(self)
        else:
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

    def gameCopy(self):
        new_game = Game(skip_initialization=True)
        new_game.players = [player.playerCopy() for player in self.players]
        new_game.tableau_de_jeu = [row[:] for row in self.tableau_de_jeu]
        return new_game

    def ai_turn(self):
        state = MinMax.GameState(self, current_player=1)

        best_eval, best_moves = MinMax.minimax(state, 3, float('-inf'), float('inf'), True)

        #if self.players[1].didWin(pion):
            #print("AI won!")
            #return True

        return False
