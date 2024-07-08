import numpy as np


def main():
    # Input and output file paths
    input_file = "input.txt"
    output_file = "output.txt"

    # Call the ReadBoard function
    ReadBoard(input_file)

def ReadBoard(input_file):
    with open(input_file, 'r') as inp:
        color = int(inp.readline().strip())
        print(f"Color 1 - white, 2 - black: {color}")
        
        prev = []
        board = []
        
        for _ in range(5):
            line = inp.readline().strip()
            row = [int(char) for char in line]
            prev.append(row)

        # Read the next 5 lines into board
        for _ in range(5):
            line = inp.readline().strip()
            row = [int(char) for char in line]
            board.append(row)

        testprogram(prev, board, color)

def testprogram(prev, board, color):

    # Print the resulting 5x5 matrix
    print("Previous Board")
    for row in prev:
        print(row)
    print("Board")
    for row in board:
        print(row)
        

    hello = DetectNeighbors(board, 0, 2)
    #print(f"Neighbors of (0, 2): {hello}")

    x = FindPreviousMove(prev, board, color)
    #valid = CheckValidMove(board, 1, 2)
    #print(valid)
    print("Trying to place piece at (1, 2)")
    valid = IsValidMove(board, 1, 2, color, prev)
    print(f"Valid move?: {valid}")

    print("Trying to place piece at (0, 1)")
    valid = IsValidMove(board, 0, 1, color, prev)
    print(f"Valid move?: {valid}")

    ValidMoveMatrix(board, color, prev)

    score = CalculateScore(board, color)
    print(f"Score for {color}: {score}")
    print(f"Score for orther: {CalculateScore(board, 1)}")




# Returns location of the previous move made
def FindPreviousMove(prev, board, color):
    if color == 1:
        opp = 2
    else:
        opp = 1
    for i in range(5):
        for j in range(5):
            if prev[i][j] != board[i][j]:
                if board[i][j] == opp:
                    prev_move = (i, j)
    return prev_move

# Returns the 4 locations adjacent to a position
def DetectNeighbors(board, x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < len(board) - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < len(board) - 1:
        neighbors.append((x, y + 1))
    return neighbors

# Returns location of ally neighbors
def DetectAllyNeighbors(board, x, y):
    neighbors = DetectNeighbors(board, x, y)
    allies = []
    #print(f"NEIGHBORS: {neighbors}")
    for space in neighbors:
        #print(f"SPACE: {space}")
        if board[space[0]][space[1]] == board[x][y]:
            allies.append(space)
    return allies

# Returns location of connecting allies, non diagonal
def FindConnectingAllies(board, x, y):
    pos = (x, y)
    a = [pos]
    allies = []
    #print(f"a: {a[0]}")
    while a:
        space = a.pop()
        allies.append(space)
        neighbors = DetectAllyNeighbors(board, space[0], space[1])
        for ally in neighbors:
            if ally not in a and ally not in allies:
                a.append(ally)
    return allies

# Returns the number of empty board spaces around a group of allies
def FindLiberty(board, x, y):
    allies = FindConnectingAllies(board, x, y)
    #print(f"Allies Connected: {allies}")
    num = 0
    for ally in allies:
        neighbors = DetectNeighbors(board, ally[0], ally[1])
        #print(f"Ally: {ally} and board number: {board[ally[1]][ally[1]]}")
        #print(neighbors)
        for neighbor in neighbors:
            if board[neighbor[0]][neighbor[1]] != board[ally[0]][ally[1]] and board[neighbor[0]][neighbor[1]] == 0:
                num = num + 1
                #print(f"Adding liberty at {neighbor}")

    return num

# Return coords of spaces captured of instance player color
def FindCapturedSpaces(board, color):
    captured = []
    for x in range (5):
        for y in range(5):
            if board[x][y] == color:
                lib = FindLiberty(board, x, y)
                if lib == 0:
                    captured.append((x, y))
    return captured

# Returns board with captured array locations set to 0
def RemoveCapturedTiles(board, captured):
    for space in captured:
        board[space[0]][space[1]] = 0
    return board

def CheckKO(prev, next):
    for row in range(5):
        for col in range(5):
            if next[row][col] != prev[row][col]:
                return False
    return True

def IsValidMove(board, x, y, color, prev):
    new = np.copy(board)
    #print(color)
    new[x][y] = color
    """
    print("Board:")
    for row in board:
        print(row)
    print("New:")
    for row in new:
        print(row)
    print("Prev:")
    for row in prev:
        print(row)
    """
    ko = CheckKO(prev, new)
    """
    print(f"Violate KO?: {ko}")
    """
    captured = FindCapturedSpaces(new, 1)
    new = RemoveCapturedTiles(new, captured)
    ko = CheckKO(prev, new)
    """
    print("New after removing")
    for row in new:
        print(row)
    print(f"Violate KO?: {ko}")
    """
    if board[x][y] == 0 and FindLiberty(new, x, y) >= 1 and CheckKO(prev, new) == False:
        return True

def ValidMoveMatrix(board, color, prev):
    validm = []
    for x in range(5):
        row = []
        for y in range(5):
            valid = IsValidMove(board, x, y, color, prev)
            row.append(valid)
        validm.append(row)
    print("Valid Matrix:")
    for row in validm:
        print(row)
        
def CalculateScore(board, color):
    score = 0
    for x in range(5):
        for y in range(5):
            if board[x][y] == color:
                score = score + 1
    
    if color == 1:
        score = score + 2.5

    return score



if __name__ == "__main__":
    main()