class GameState:
    def __init__(self, game, current_player):
        self.game = game  # The current game instance
        self.current_player = current_player  # The index of the current player (0 or 1)

    def get_possible_moves(self):
        moves = []
        current_player = self.game.players[self.current_player]
        for pion in [current_player.pion1, current_player.pion2]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if current_player.isValidMovement(pion, dx, dy):
                        for bx in [-1, 0, 1]:
                            for by in [-1, 0, 1]:
                                if pion.isValidBuilding(bx, by):
                                    moves.append((pion.pionID, dx, dy, bx, by))
        return moves

    def apply_move(self, pion, dx, dy, bx, by):
        pionChoosen =  self.game.players[self.current_player].pion1 if pion == 1 else self.game.players[self.current_player].pion2
        new_game = GameState(self.game.gameCopy(), self.current_player) # Create a deep copy of the game
        print("Applying move: ", pion, dx, dy, bx, by)
        current_player = new_game.game.players[new_game.current_player]
        print("Current player apply: ", current_player.name)
        # Move the pion, ensuring the move is valid
        if current_player.isValidMovement(pionChoosen, dx, dy):
            current_player.move(pionChoosen, dx, dy)
        # Build if valid
        if pionChoosen.isValidBuilding(bx, by):
            pionChoosen.build(bx, by)
        new_game.game.printBoard()
        return GameState(new_game, (self.current_player + 1) % 2)

    def is_terminal(self):
        for player in self.game.players:
            for pion in [player.pion1, player.pion2]:
                if self.game.tableau_de_jeu[pion.x][pion.y] == 3:
                    print("Player ", player.name, " has won!")
                    return True  # A player has won by reaching the third level
        return False

    def evaluate(self):
        score = 0
        for player in self.game.players:
            for pion in [player.pion1, player.pion2]:
                score += self.game.tableau_de_jeu[pion.x][pion.y]  # Sum the heights of the buildings
        return score if self.current_player == 0 else -score  # Positive score for player 0, negative for player 1

def minimax(state, depth, alpha, beta, maximizing_player):
    print("Depth: ", depth)
    print("Current player:", state.current_player)
    if depth == 0 or state.is_terminal():
        return state.evaluate(), []

    moves = state.get_possible_moves()
    if maximizing_player:
        max_eval = float('-inf')
        best_move_sequence = []
        for move in moves:
            new_state = state.apply_move(*move)
            eval, move_sequence = minimax(new_state, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move_sequence = [move] + move_sequence
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        print("Best move sequence: ", best_move_sequence)
        return max_eval, best_move_sequence
    else:
        min_eval = float('inf')
        best_move_sequence = []
        for move in moves:
            new_state = state.apply_move(*move)
            eval, move_sequence = minimax(new_state, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move_sequence = [move] + move_sequence
            beta = min(beta, eval)
            if beta <= alpha:
                break
        print("Best move sequence: ", best_move_sequence)
        return min_eval, best_move_sequence