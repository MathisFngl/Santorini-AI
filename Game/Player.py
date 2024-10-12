from .Pion import Pion
from .Board import PlayerList, tableau_de_jeu

class Joueur:
    def __init__(self, name, dieu):
        self.name = name
        self.pion1 = Pion(0, 0)
        self.pion2 = Pion(1, 1)
        self.pouvoir_de_dieu = dieu

    def isValidMovement(self, pion, x, y):
        new_x = pion.x + x
        new_y = pion.y + y
        if new_x < 0 or new_x > 5 and new_y < 0 or new_y > 5:
            print("Cannot Move Here: Out of Bounds")
            return False
        if tableau_de_jeu[new_x][new_y] == 4:
            print("Cannot Move Here: Cannot be on a Dome")
            return False
        for player in PlayerList:
            if (player.pion1.x == new_x and player.pion1.y == new_y) or (player.pion2.x == new_x and player.pion2.y == new_y):
                print("Cannot Move Here: A builder is on this square.")
                return False
        return True

    def move(self, pion, x, y):
        if self.isValidMovement(pion, x, y):
            pion.x += x
            pion.y += y

    def chooseBuilderToMove(self):
        while True:
            choice = input("Which builder to move ? (1 or 2)")
            if choice == '1':
                return self.pion1
            elif choice == '2':
                return self.pion2
            else:
                print("Invalid input. Please enter 1 or 2.")

    def selectDirectionOfMovement(self):
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
            print("Choose a direction to move:")
            print("1: Up-Left    2: Up    3: Up-Right")
            print("4: Left               5: Right")
            print("6: Down-Left  7: Down  8: Down-Right")
            print()
            choice = input("Enter a number between 1 and 8: ")

            if choice in directions:
                return directions[choice]
            else:
                print("Invalid choice. Please choose a number between 1 and 8.")

    def movementHandler(self):
        pion = self.chooseBuilderToMove()
        print(f"Current Pion Position: ({pion.x},{pion.y})")
        movement = self.selectDirectionOfMovement()
        self.move(pion, movement[0], movement[1])
        print(f"New Pion Position: ({pion.x},{pion.y})")
