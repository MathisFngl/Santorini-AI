from Game.Pion import Pion
import random


class Joueur:
    def __init__(self, game, skip_initialization = False):
        self.game = game
        if not skip_initialization:
            self.name = self.nameDefinition()
            self.pion1 = Pion(self, -1, -1, 1)
            self.pion2 = Pion(self, -1, -1, 2)
            self.defineBothPions()


    def nameDefinition(self):
        return input("Player's name :")

    def defineBothPions(self):
        self.pion1 = self.pionDefinition(1)
        self.pion2 = self.pionDefinition(2)

    def pionDefinition(self, pionId):
        x = -1
        y = -1
        valid_position = False
        while not valid_position:
            x = int(input("Enter x pos of Pion :"))
            y = int(input("Enter y pos of Pion :"))
            if 0 <= x < 5 and 0 <= y < 5:
                if (not self.game.is_occupied(x, y)) and not (self.pion1.x == x and self.pion1.y == y):
                    valid_position = True
                else:
                    print("This Square is already occupied")
            else:
                print("Location out of bounds")
        return Pion(self, x, y, pionId)

    def isValidMovement(self, pion, x, y):
        new_x = pion.x + x
        new_y = pion.y + y
        if new_x < 0 or new_x >= 5 or new_y < 0 or new_y >= 5:
            if self.name != "AI":
                print("Cannot Move Here: Out of Bounds")
            return False
        if self.game.tableau_de_jeu[new_x][new_y] == 4:
            if self.name != "AI":
                print("Cannot Move Here: Cannot be on a Dome")
            return False
        for player in self.game.players:
            if (player.pion1.x == new_x and player.pion1.y == new_y) or (
                    player.pion2.x == new_x and player.pion2.y == new_y):
                if self.name != "AI":
                    print("Cannot Move Here: A builder is on this square.")
                return False
        return True

    def move(self, pion, x, y):
        if self.isValidMovement(pion, x, y):
            pion.x += x
            pion.y += y

    def chooseBuilder(self, ask_str):
        while True:
            choice = input(f"Which builder to {ask_str} ? (1 or 2)")
            if choice == '1':
                return self.pion1
            elif choice == '2':
                return self.pion2
            else:
                print("Invalid input. Please enter 1 or 2.")

    def selectDirection(self, desc_str):
        directions = {
            '1': (-1, -1),  # Up-Left
            '2': (-1, 0),  # Up
            '3': (-1, 1),  # Up-Right
            '4': (0, -1),  # Left
            '5': (0, 1),  # Right
            '6': (1, -1),  # Down-Left
            '7': (1, 0),  # Down
            '8': (1, 1)  # Down-Right
        }

        while True:
            print("Choose a direction to" + desc_str + " :")
            print("1: Up-Left    2: Up    3: Up-Right")
            print("4: Left               5: Right")
            print("6: Down-Left  7: Down  8: Down-Right")
            print()
            choice = input("Enter a number between 1 and 8: ")

            if choice in directions:
                return directions[choice]
            else:
                print("Invalid choice. Please choose a number between 1 and 8.")

    def didWin(self, pion):
        if self.game.tableau_de_jeu[pion.x][pion.y] == 3:
            return True

    def movementHandler(self):
        pion = self.chooseBuilder("move")
        print(f"Current Pion Position: ({pion.x},{pion.y})")
        movement = self.selectDirection("move")
        self.move(pion, movement[0], movement[1])
        print(f"New Pion Position: ({pion.x},{pion.y})")
        if self.didWin(pion):
            print("You won!")
            return True
        return False

    def buildingHandler(self):
        did_build = False
        while not did_build:
            pion = self.chooseBuilder("build")
            print(f"Current Pion Position: ({pion.x},{pion.y}")
            building = self.selectDirection("build")
            if pion.isValidBuilding(building[0], building[1]):
                pion.build(building[0], building[1])
                did_build = True

    def playerCopy(self):
        new_player = Joueur(self.game, skip_initialization=True)
        new_player.name = self.name
        new_player.pion1 = self.pion1.pionCopy()
        new_player.pion2 = self.pion2.pionCopy()
        return new_player

class AIPlayer(Joueur):
    def nameDefinition(self):
        return "AI"

    def defineBothPions(self):
        self.pion1 = self.randomPionDefinition(1)
        self.pion2 = self.randomPionDefinition(2)

    def randomPionDefinition(self, pionId):
        valid_position = False
        while not valid_position:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if not self.game.is_occupied(x, y):
                if pionId == 1 or (self.pion1.x != x or self.pion1.y != y):
                    valid_position = True
        return Pion(self, x, y, pionId)