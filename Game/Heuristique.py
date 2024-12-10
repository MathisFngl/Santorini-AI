import math


def averageHeightAroundCoordinates(x, y, tableau):
    """
    Calculates the average height around a place on the board
    :param x: x evaluated coordinate, int
    :param y: y evaluated coordinate, int
    :param tableau: Board information, matrix
    :return: average height around the x, y coordinates, float
    """
    total_height = 0
    valid_entries = 0

    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            nx, ny = x + x1, y + y1
            if 0 <= nx < 5 and 0 <= ny < 5:  # Ensure we're within the 5x5 grid
                total_height += tableau[nx][ny]
                valid_entries += 1

    return total_height / valid_entries if valid_entries > 0 else 0


def maxAvailableMoves(x, y, tableau, pawns):
    """
    Calculates the number of possible moves.
    :param x: x evaluated coordinate, int
    :param y: y evaluated coordinate , int
    :param tableau: Board information, matrix
    :param pawns: List of every other pawns : coordinates list
    :return: number of possible moves, int
    """
    moves = 0

    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            if x1 == 0 and y1 == 0:
                continue
            nx, ny = x + x1, y + y1
            if 0 <= nx < 5 and 0 <= ny < 5:
                if tableau[nx][ny] != 4 and not any(pawn.x == nx and pawn.y == ny for pawn in pawns):
                    moves += 1
    return moves


def isCentralPosition(x, y):
    """
    Determine if the given x, y position is among the 9 center square
    :param x: x evaluated coordinate, int
    :param y: y evaluated coordinate , int
    :return: if the coordinates are among the 9 center : boolean
    """
    return 1 <= x <= 3 and 1 <= y <= 3


def distanceToCentralPosition(pawn):
    """
    Calculate the straight-line distance between the center of the board and a pawn.
    :param pawn: The pawn with getCoordinates() method.
    :return: The straight-line distance (hypotenuse) between the two points.
    """
    x1, y1 = pawn.getCoordinates()
    x2, y2 = 2, 2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def euclidean_distance(pawn1, pawn2):
    """
    Calculate the straight-line distance between two pawns.
    :param pawn1: The starting pawn with getCoordinates() method.
    :param pawn2: The target pawn with getCoordinates() method.
    :return: The straight-line distance (hypotenuse) between the two points.
    """
    x1, y1 = pawn1.getCoordinates()
    x2, y2 = pawn2.getCoordinates()
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def sumCompletedTowersAroundPawn(x, y, tableau, pawns):
    """
    Count the number of unoccupied towers with values 2 or 3
    :param pawns: list of pawns on the board
    :param x: x evaluated coordinate, int
    :param y: y evaluated coordinate , int
    :param tableau: The 5x5 game board.
    :return: Number of cells around the pawn with values 2 or 3.
    """
    total_count = 0

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < 5 and 0 <= ny < 5:
                if tableau[nx][ny] in (2, 3):
                    is_occupied = any(pawn.x == nx and pawn.y == ny for pawn in pawns)
                    if not is_occupied:
                        total_count += 1
    return total_count


def isPawnBlocked(p, tableau, pawns):
    """
    Determines if a player is blocked by towers of 4 or other players all around them.
    :param p: The current pawn (object with coordinates x, y).
    :param tableau: The 5x5 game board containing tower values.
    :param pawns: List of pawns (objects with x, y) representing other pawns.
    :return: True if the pawn is blocked; otherwise, False.
    """

    x, y = p.getCoordinates()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < 5 and 0 <= ny < 5:
                if tableau[nx][ny] == 4 or any(pawn.x == nx and pawn.y == ny for pawn in pawns):
                    continue  # The cell is blocked, cycle the loop
                return False  # If at least one of the 8 surrounding cells is free, the pawn is NOT blocked
    return True

def countCompletedTowers(tableau):
    """
    Count the total number of completed towers (level 4) on the board.
    :param tableau: The 5x5 game board containing tower values.
    :return: Number of completed towers on the board
    """
    total_count = 0
    for row in tableau:
        for cell in row:
            if cell == 4:
                total_count += 1
    return total_count

def winningPawn(p, tableau, pawns):
    """
    Check if a pawn can make a winning move by moving to a level 3 tower.
    :param p: The current pawn (object with coordinates x, y).
    :param tableau: The 5x5 game board containing tower values.
    :param pawns: List of pawns (objects with x, y) representing other pawns.
    :return: True if the pawn can win by moving, False otherwise.
    """
    x, y = p.getCoordinates()
    if tableau[x][y] != 2:
        return False

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < 5 and 0 <= ny < 5:
                if any(pawn.x == nx and pawn.y == ny for pawn in pawns):
                    continue
                if tableau[nx][ny] == 3:
                    return True
    return False

def countTotalConstructions(tableau):
    """
    Calculate the total number of constructions on the board.
    :param tableau: The 5x5 game board containing tower values.
    :return: The total number of constructions
    """
    total_constructions = 0

    for row in tableau:
        for cell in row:
            total_constructions += cell
    return total_constructions


def evaluatePawn(pawn, tableau, allPawns, coeff):
    """
    Evaluate a single pawn and return its contribution to the score.

    :param pawn: The pawn to evaluate.
    :param tableau: The 5x5 game board containing tower values.
    :param allPawns: List of the other pawns (AI and player).
    :param weight: A multiplier (1 for AI, -1 for player).
    :return: The score contribution of the pawn.
    """
    x, y = pawn.getCoordinates()
    pawn_level = tableau[x][y]
    score = 0

    # Define weights for each attribute
    weights = {
        "winning_move_weight": 100,
        "blocked_weight": 30,
        "towers_weight": 10,
        "height_weight": 2,
        "center_weight": 10,
        "distance_weight": 5,
        "moves_weight": 1
    }

    # Can the pawn make a winning move
    if winningPawn(pawn, tableau, allPawns):
        score += coeff * weights["winning_move_weight"]

    # Is the pawn blocked
    if isPawnBlocked(pawn, tableau, allPawns):
        score -= coeff * weights["blocked_weight"]

    # Is the pawn next to towers
    accessible_towers = sumCompletedTowersAroundPawn(x, y, tableau, allPawns)
    if pawn_level > 0:
        score += coeff * accessible_towers * weights["towers_weight"]
    else:
        score -= coeff * accessible_towers * weights["towers_weight"]

    # Average height around the pawn
    score += coeff * averageHeightAroundCoordinates(x, y, tableau) * weights["height_weight"]

    # Is the pawn at the center of the board
    if isCentralPosition(x, y):
        score += coeff * weights["center_weight"]
    else:
        score -= coeff * distanceToCentralPosition(pawn) * weights["distance_weight"]

    # Can the pawn move around
    score += coeff * maxAvailableMoves(x, y, tableau, allPawns) * weights["moves_weight"]

    return score



def evaluateGameState(tableau, AIpawns, playerPawns):
    """
    Evaluate the value of the game state for the AI.
    :param tableau: The 5x5 game board containing tower values.
    :param AIpawns: List of AI's pawns.
    :param playerPawns: List of player's pawns.
    :return: A float representing the value of the game state.
    """
    score = 0

    # Evaluate AI pawns
    for pawn in AIpawns:
        score += evaluatePawn(pawn, tableau, AIpawns + playerPawns, 1)

    # Evaluate player pawns
    for pawn in playerPawns:
        score += evaluatePawn(pawn, tableau, AIpawns + playerPawns, -1)


    return score
