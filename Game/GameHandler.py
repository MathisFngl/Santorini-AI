import msvcrt
from time import sleep

from .Player import Joueur, QLearningAgentPlayer, MinMaxPlayer
from .Window import *
import Game.MinMax as MinMax
import copy
import threading
from .Heuristique import evaluateGameState, isPawnBlocked
from .QLearningAgent import QLearningUCB
from .Heuristique import evaluateGameState
from .GameServer import GameServer

class Game:
    def __init__(self, skip_initialization=False, isServerActive=False, server=None):
        self.mode = None
        self.players = []
        self.tableau_de_jeu = [[0 for i in range(5)] for j in range(5)]
        self.mode_set_event = threading.Event()
        self.mode_set_by_server = False
        self.last_move_x = -1  # Store the last move x coordinate
        self.last_move_y = -1  # Store the last move y coordinate
        self.moveReceived = False  # Flag to indicate if a move has been received
        self.buildReceived = False  # Flag to indicate if a build has been received
        self.moveDirection = (None, 0, 0)  # Store the direction of the last move
        self.buildDirection = (0, 0)  # Store the direction of the last build
        if isServerActive:
            self.game_server = server
        self.isServerActive = isServerActive
        if not skip_initialization:
            self.play()

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpicklable entries
        del state['mode_set_event']
        if 'game_server' in state:
            del state['game_server']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Restore the unpicklable entries
        self.mode_set_event = threading.Event()
        if self.isServerActive:
            self.game_server = None

    def play(self):
        win = False
        self.chooseMode()
        if self.mode == 1 :
            player_1 = Joueur(self)
            self.players.append(player_1)
            player_2 = Joueur(self)
            self.players.append(player_2)
            #self.game_server.sendMessageToServer("START")
        elif self.mode == 2:
            player_1 = Joueur(self)
            self.players.append(player_1)
            player_2 = MinMaxPlayer(self)
            self.players.append(player_2)
            if self.isServerActive :
                self.game_server.sendMessageToServer(f"INIT Player1 Perso1 {player_1.pion1.x} {player_1.pion1.y} Perso2 {player_1.pion2.x} "
                                                 f"{player_1.pion2.y} Player2 Perso1 {player_2.pion1.x} {player_2.pion1.y} Perso2 {player_2.pion2.x} {player_2.pion2.y}")
        elif self.mode == 3:
            q_learning_agent = QLearningUCB(self)
            self.players = [QLearningAgentPlayer(self), QLearningAgentPlayer(self)]
            # Load the model if it exists
            try:
                q_learning_agent.load_model('q_learning_model.pkl')
            except FileNotFoundError:
                print("No existing model found. Starting fresh.")
            q_learning_agent.train(episodes=10000)  # Train the Q-learning agent
            q_learning_agent.plot_training_progress()
            q_learning_agent.save_model('q_learning_model.pkl')
        elif self.mode == 4:
            q_learning_agent = QLearningUCB(self)
            self.players = [QLearningAgentPlayer(self), MinMaxPlayer(self)]
            self.simulate_games(q_learning_agent, 100)  # Simulate 10 games
            q_learning_agent.plot_training_progress()

        while not win and self.mode != 3 and self.mode != 4:
            for player in self.players:
                player_pos_params = self.generatePlayerPos()
                if not self.isServerActive:
                    render_grid(self.tableau_de_jeu, player_pos_params)


                print()
                print("Board State :")
                self.printBoard()
                print()

                print("/// GAME STATE ///")
                ai_pawns = [self.players[1].pion1, self.players[1].pion2]
                player_pawns = [self.players[0].pion1, self.players[0].pion2]
                score = evaluateGameState(self.tableau_de_jeu, ai_pawns, player_pawns, 1)
                print("Score : " + str(score))
                print()
                if player.name == "AI":
                    print("AI's turn :")
                    if self.ai_turn(1):
                        win = True
                        break
                    print("AI turn ended")
                elif player.name == "Q-Learning":
                    print("Q-Learning's turn :")
                    if self.q_learning_turn(player):
                        win = True
                        break
                    print("Q-Learning turn ended")
                else:
                    if self.isServerActive :
                        while not self.moveReceived:
                            sleep(0.1)
                    print(player.name + "'s turn :")
                    testMovementHandler, pion = player.movementHandler()
                    if testMovementHandler:
                        win = True
                        player_pos_params = self.generatePlayerPos()
                        if not self.isServerActive:
                            render_grid(self.tableau_de_jeu, player_pos_params)
                        break
                    print()
                    print("Board State :")
                    self.printBoard()
                    print()
                    player.buildingHandler(pion)

    def wait_for_mode_set(self):
        """
        Bloque jusqu'à ce que le serveur définisse un mode.
        """
        self.mode_set_event.wait()  # Attend que le mode soit défini
        self.mode_set_by_server = True  # Set the flag when mode is set by server
        print("\nMode défini par le serveur. Interruption de l'entrée utilisateur...")

    def chooseMode(self):
        """
        Permet de choisir un mode, interrompu si le serveur définit le mode avant la saisie.
        """
        print("Choose the mode you want to play or wait for the server:")
        print("1. Player vs Player")
        print("2. Player vs AI")
        print("3. Q-Learning Training")
        print("4. Q-Learning vs Minimax")

        if self.isServerActive:
            # Démarre un thread pour surveiller si le mode est défini par le serveur
            watcher_thread = threading.Thread(target=self.wait_for_mode_set, daemon=True)
            watcher_thread.start()

        while not self.mode_set_event.is_set():
            try:
                if not self.mode_set_by_server:  # Check the flag before reading input
                    user_input = self.non_blocking_input() if self.isServerActive else input()
                    if user_input.isdigit():
                        self.mode = int(user_input)
                        self.mode_set_event.set()
                        break
            except KeyboardInterrupt:
                print("\nInput interrompu.")
                break

        if self.mode_set_event.is_set():
            print(f"Mode sélectionné automatiquement par le serveur : {self.mode}")
        else:
            print(f"Mode sélectionné par l'utilisateur : {self.mode}")

    def non_blocking_input(self):
        """
        Non-blocking method to read user input.
        """
        if msvcrt.kbhit():
            return input()
        return ""

    def setMode(self, mode):
        """
        Définit le mode de jeu. Peut être appelé par le serveur.
        """
        self.mode = mode
        self.mode_set_event.set()  # Signale que le mode est défini
        print(f"Mode défini par le serveur : {self.mode}")

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

    def ai_turn(self, mode):
        state = MinMax.GameState(self, current_player=1)

        best_eval, best_moves = MinMax.minimax(state, 3, float('-inf'), float('inf'), True)

        if not best_moves:  # Vérifie si best_moves est vide
            print("AI has no valid moves.")
            return False
        else:
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
            if self.isServerActive:
                self.game_server.sendMessageToServer(f"AI MOVE {move_pion_id} {move_pion.x} {move_pion.y} BUILD {move_pion.x + bx} {move_pion.y + by}")
        else:
            print("Invalid building")
            return False

        for pion in [self.players[1].pion1, self.players[1].pion2]:
            if self.tableau_de_jeu[pion.y][pion.x] == 3:
                print("AI won!")
                player_pos_params = self.generatePlayerPos()
                if mode == 1 or mode == 2:
                    render_grid(self.tableau_de_jeu, player_pos_params)
                return True

        return False

    def reset(self):
        self.tableau_de_jeu = [[0 for _ in range(5)] for _ in range(5)]
        self.players = [QLearningAgentPlayer(self),
                        QLearningAgentPlayer(self)]
        return self.get_state()

    def step(self, action):
        move_pion_id, dx, dy, build_pion_id, bx, by = action
        move_pion = self.players[0].pion1 if move_pion_id == 1 else self.players[0].pion2
        build_pion = self.players[0].pion1 if build_pion_id == 1 else self.players[0].pion2
        print("Applying move: ", move_pion_id, dx, dy, build_pion_id, bx, by)
        # Move if valid
        if self.players[0].isValidMovement(move_pion, dx, dy):
            self.players[0].move(move_pion, dx, dy)
        else:
            return self.get_state(), -10, False  # Invalid move, negative reward

        # Check for win condition
        for pion in [self.players[0].pion1, self.players[0].pion2]:
            if self.tableau_de_jeu[pion.y][pion.x] == 3:
                return self.get_state(), 1000, True  # Win, positive reward

        # Build if valid
        if build_pion.isValidBuilding(bx, by):
            build_pion.build(bx, by)
        else:
            return self.get_state(), -10, False  # Invalid build, negative reward

        # Additional rewards and penalties
        reward = -0.2  # Small penalty for each move to encourage faster wins

        # Reward for moving to a higher level
        if self.tableau_de_jeu[move_pion.y][move_pion.x] > self.tableau_de_jeu[move_pion.y - dy][move_pion.x - dx]:
            reward += 1

        # Penalty for moving to a lower level
        if self.tableau_de_jeu[move_pion.y][move_pion.x] < self.tableau_de_jeu[move_pion.y - dy][move_pion.x - dx]:
            reward -= 1

        # Reward for blocking opponent's move
        opponent = self.players[1]
        for pion in [opponent.pion1, opponent.pion2]:
            if isPawnBlocked(pion,self.tableau_de_jeu, [self.players[0].pion1, self.players[0].pion2]):
                reward += 1

        if not self.get_possible_actions(self.get_state()):
            reward -= 10  # Significant penalty for having no valid moves

        return self.get_state(), reward, False  # Continue game
    def get_possible_actions(self, state):
        actions = []
        for move_pion_id in [1, 2]:
            move_pion = self.players[0].pion1 if move_pion_id == 1 else self.players[0].pion2
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx, dy) != (0, 0):
                        if self.players[0].isValidMovement(move_pion, dx, dy):
                            build_pion_test = move_pion.pionCopy()
                            build_pion_test.x = build_pion_test.x + dx
                            build_pion_test.y = build_pion_test.y + dy
                            for bx in [-1, 0, 1]:
                                for by in [-1, 0, 1]:
                                    if (bx, by) != (0, 0):
                                        if build_pion_test.isValidBuilding(bx, by):
                                            actions.append((move_pion_id, dx, dy, move_pion_id, bx, by))
        return actions

    def get_state(self):
        return (tuple(tuple(row) for row in self.tableau_de_jeu),
                tuple((pion.x, pion.y) for player in self.players for pion in [player.pion1, player.pion2]))

    def q_learning_turn(self, q_learning_agent):
        state = MinMax.GameState(self, current_player=0)
        action = q_learning_agent.select_action(state)
        if action is None:
            return False
        next_state, reward, done = self.step(action)
        q_learning_agent.update_q_value(state, action, reward, MinMax.GameState(self, 0))
        q_learning_agent.update_visit_counts(state, action)
        return done

    def simulate_games(self, q_learning_agent, num_games):
        for _ in range(num_games):
            self.reset()
            print("Game number: ", _)
            done = False
            while not done:
                if self.players[0].name == "Q-Learning":
                    done = self.q_learning_turn(q_learning_agent)
                else:
                    done = self.ai_turn(4)