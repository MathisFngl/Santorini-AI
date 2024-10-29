class GameState:
    def __init__(self, board, players, current_player):
        self.board = board
        self.players = players
        self.current_player = current_player

    def get_possible_moves(self):
        # generate all possible moves for the current player
        moves = []
        current_player = self.players[self.current_player]
        for pion in [current_player.pion1, current_player.pion2]:
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x == 0 and y == 0:
                        continue  # ingore the case where the pion doesn't move
                    if current_player.isValidMovement(pion, x, y):
                        moves.append((pion, x, y))  # add the move to the list of possible moves
        return moves

    def apply_move(self, pion, x, y):
        # apply the move to the game state
        new_board = [row[:] for row in self.board] # copy the board
        new_players = [player.copy() for player in self.players] # copy the players
        new_pion = new_players[self.current_player].pion1 if pion == self.players[self.current_player].pion1 else new_players[self.current_player].pion2
        new_pion.x += x
        new_pion.y += y

        return GameState(new_board, new_players, 1 - self.current_player)
