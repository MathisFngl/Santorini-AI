from .Player import Joueur, QLearningAgentPlayer, MinMaxPlayer
from .Window import *
import Game.MinMax as MinMax
import copy
from .Heuristique import evaluateGameState, isPawnBlocked
from .QLearningAgent import QLearningUCB
from .Heuristique import evaluateGameState

class Game:
    def __init__(self, skip_initialization=False):
        if not skip_initialization:
            self.players = []
            self.tableau_de_jeu = [[0 for i in range(5)] for j in range(5)]
            self.play()

    def play(self):
        win = False
        mode = self.chooseMode()
        if mode == 1 or mode == 2:
            self.choosePlayer()
        elif mode == 3:
            q_learning_agent = QLearningUCB(self)
            self.players = [QLearningAgentPlayer(self), QLearningAgentPlayer(self)]
            # Load the model if it exists
            try:
                q_learning_agent.load_model('q_learning_model.pkl')
            except FileNotFoundError:
                print("No existing model found. Starting fresh.")
            q_learning_agent.train(1000)  # Train the Q-learning agent
            q_learning_agent.plot_training_progress()
            q_learning_agent.save_model('q_learning_model.pkl')
        elif mode == 4:
            q_learning_agent = QLearningUCB(self)
            self.players = [QLearningAgentPlayer(self), MinMaxPlayer(self)]
            self.simulate_games(q_learning_agent, 100)  # Simulate 10 games
            q_learning_agent.plot_training_progress()

        while not win and mode != 3 and mode != 4:
            for player in self.players:
                player_pos_params = self.generatePlayerPos()
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
                    print(player.name + "'s turn :")
                    testMovementHandler, pion = player.movementHandler()
                    if testMovementHandler:
                        win = True
                        player_pos_params = self.generatePlayerPos()
                        render_grid(self.tableau_de_jeu, player_pos_params)
                        break
                    print()
                    print("Board State :")
                    self.printBoard()
                    print()
                    player.buildingHandler(pion)

    def chooseMode(self):
        print("Choose the mode you want to play :")
        print("1. Player vs Player")
        print("2. Player vs AI")
        print("3. Q-Learning Training")
        print("4. Q-Learning vs Minimax")
        mode = int(input())
        return mode


    def choosePlayer(self):
        player_1 = Joueur(self)
        self.players.append(player_1)
        print("Enter the name of the second player (or type 'AI' for the AI): ")
        player_2_name = input()
        if player_2_name == "AI":
            player_2 = MinMaxPlayer(self)
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
        else:
            print("Invalid building")
            return False

        print("/// SCORE FINAL ///\n")
        score = state.evaluate()

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

        # Move if valid
        if self.players[0].isValidMovement(move_pion, dx, dy):
            self.players[0].move(move_pion, dx, dy)
        else:
            return self.get_state(), -1, False  # Invalid move, negative reward

        # Check for win condition
        for pion in [self.players[0].pion1, self.players[0].pion2]:
            if self.tableau_de_jeu[pion.x][pion.y] == 3:
                return self.get_state(), 10, True  # Win, positive reward

        # Build if valid
        if build_pion.isValidBuilding(bx, by):
            build_pion.build(bx, by)
        else:
            return self.get_state(), -1, False  # Invalid build, negative reward

        # Additional rewards and penalties
        reward = -0.1  # Small penalty for each move to encourage faster wins

        # Reward for moving to a higher level
        if self.tableau_de_jeu[move_pion.x][move_pion.y] > self.tableau_de_jeu[move_pion.x - dx][move_pion.y - dy]:
            reward += 1

        # Penalty for moving to a lower level
        if self.tableau_de_jeu[move_pion.x][move_pion.y] < self.tableau_de_jeu[move_pion.x - dx][move_pion.y - dy]:
            reward -= 1

        # Reward for blocking opponent's move
        opponent = self.players[1]
        for pion in [opponent.pion1, opponent.pion2]:
            if isPawnBlocked(pion,self.tableau_de_jeu, [self.players[0].pion1, self.players[0].pion2]):
                reward += 0.5

        return self.get_state(), reward, False  # Continue game
    def get_possible_actions(self, state):
        actions = []
        for move_pion_id in [1, 2]:
            move_pion = self.players[0].pion1 if move_pion_id == 1 else self.players[0].pion2
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx, dy) != (0, 0):
                        if self.players[0].isValidMovement(move_pion, dx, dy):
                            for bx in [-1, 0, 1]:
                                for by in [-1, 0, 1]:
                                    if (bx, by) != (0, 0):
                                        if move_pion.isValidBuilding(bx + dx, by + dy):
                                            actions.append((move_pion.pionID, dx, dy, move_pion.pionID, bx, by))
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