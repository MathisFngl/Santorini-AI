from .Player import Joueur, AIPlayer
from .Window import *
import Game.MinMax as MinMax
import copy

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

                player_pos_params = self.generatePlayerPos()
                render_grid(self.tableau_de_jeu, player_pos_params)

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
                    testMovementHandler, pion = player.movementHandler()
                    if testMovementHandler:
                        win = True
                        break
                    print()
                    print("Board State :")
                    self.printBoard()
                    print()
                    player.buildingHandler(pion)



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

    def isOccupied(self, x, y):
        for player in self.players:
            if (player.pion1.x == x and player.pion1.y == y) or (player.pion2.x == x and player.pion2.y == y):
                return True
        return False

    def generatePlayerPos(self):
        pos = []
        player1 = self.players[0]
        pos.append((player1.pion1.x, player1.pion1.y, (255, 0, 0)))
        pos.append((player1.pion2.x, player1.pion2.y, (255, 0, 0)))
        player2 = self.players[1]
        pos.append((player2.pion1.x, player2.pion1.y, (0, 0, 255)))
        pos.append((player2.pion2.x, player2.pion2.y, (0, 0, 255)))
        return pos

    def gameCopy(self):
        return copy.deepcopy(self)

    def ai_turn(self):
        state = MinMax.GameState(self, current_player=1)

        best_eval, best_moves = MinMax.minimax(state, 3, float('-inf'), float('inf'), True)

        moveToApply = best_moves[0]
        move_pion_id, dx, dy, build_pion_id, bx, by = moveToApply
        move_pion = self.players[1].pion1 if move_pion_id == 1 else self.players[1].pion2
        build_pion = self.players[1].pion1 if build_pion_id == 1 else self.players[1].pion2

        # Move if valid
        if self.players[1].isValidMovement(move_pion, dx, dy):
            self.players[1].move(move_pion, dx, dy)
        else:
            print("Invalid move")
            return False

        # Build if valid
        if build_pion.isValidBuilding(bx, by):
            build_pion.build(bx, by)
        else:
            print("Invalid building")
            return False

        for pion in [self.players[1].pion1, self.players[1].pion2]:
            if self.tableau_de_jeu[pion.x][pion.y] == 3:
                print("AI won!")
                return True

        return False
