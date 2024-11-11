import copy

# Class representing the state of the game
class GameState:
    def __init__(self, game, current_player):
        self.game = game  # The current game instance
        self.current_player = current_player  # The index of the current player (0 or 1)

    # Method to get all possible moves (including construction) for the current player
    def get_possible_moves(self):
        moves = []
        current_player = self.game.players[self.current_player]
        for pion in [current_player.pion1, current_player.pion2]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Skip the current position
                    if current_player.isValidMovement(pion, dx, dy):
                        for bx in [-1, 0, 1]:
                            for by in [-1, 0, 1]:
                                if bx == 0 and by == 0:
                                    continue  # Skip the current position
                                if pion.isValidBuilding(bx, by):
                                    moves.append((pion, dx, dy, bx, by))  # Add valid move and build actions to the list
        return moves

    def apply_move(self, pion, dx, dy, bx, by):
        if not pion.player.isValidMovement(pion, dx, dy) or not pion.isValidBuilding(bx, by):
            return self  # Return the current state if the move is invalid
        new_game = copy.deepcopy(self.game)  # Create a deep copy of the game
        current_player = new_game.players[self.current_player]
        current_player.move(pion, dx, dy)  # Move the pion
        pion.build(bx, by)  # Build after moving

        return GameState(new_game, (self.current_player + 1) % 2)


    # Method to check if the game is in a terminal state (win or loss)
    def is_terminal(self):
        for player in self.game.players:
            for pion in [player.pion1, player.pion2]:
                if self.game.tableau_de_jeu[pion.x][pion.y] == 3:
                    print(f"{player.name} has won the game!")
                    return True  # A player has won by reaching the third level
        for _ in self.game.players:
            if not any(self.get_possible_moves()):
                print("A player has lost the game!")
                return True  # A player has lost by having no valid moves
        print("Game continues...")
        return False

    # Method to evaluate the game state and return a score
    def evaluate(self):
        score = 0
        for player in self.game.players:
            for pion in [player.pion1, player.pion2]:
                score += self.game.tableau_de_jeu[pion.x][pion.y]  # Sum the heights of the buildings
        return score if self.current_player == 0 else -score  # Positive score for player 0, negative for player 1


def get_best_moves(state, depth):
    best_moves = []
    best_value = float('-inf')

    for move in state.get_possible_moves():
        new_state = state.apply_move(*move)
        move_value = minimax(new_state, depth - 1, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)

        if move_value > best_value:
            best_value = move_value
            best_moves = [move]
        elif move_value == best_value:
            best_moves.append(move)

    return best_moves

def minimax(state, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return state.evaluate()  # Return the evaluation of the state if depth is 0 or state is terminal

    moves = state.get_possible_moves()
    # Order moves based on build higher levels first
    moves.sort(key=lambda move: state.apply_move(*move).evaluate(), reverse=maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_state = state.apply_move(*move)
            eval = minimax(new_state, depth - 1, alpha, beta, False)  # Recursively call minimax for the minimizing player
            max_eval = max(max_eval, eval)  # Update the maximum evaluation
            alpha = max(alpha, eval)  # Update alpha
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_state = state.apply_move(*move)
            eval = minimax(new_state, depth - 1, alpha, beta, True)  # Recursively call minimax for the maximizing player
            min_eval = min(min_eval, eval)  # Update the minimum evaluation
            beta = min(beta, eval)  # Update beta
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval