import sys
import re
intro = """Hello! Welcome to Pentago.
Move command: board/space board rotation.
Like this 3/1 3r\n"""
board = [[], [], [], []]
for z in range(4):
    board[z] = ['.' for x in range(9)]

#easier way to do this?
def printBoard():
    boardPrint = []
    boardPrint.append('Pantego - - -\n')
    for row in range(0, 3):
        for col in range(0, 3):
            boardPrint.append(board[0][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('| ')
        for col in range(0, 3):
            boardPrint.append(board[1][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('\n')
    boardPrint.append('- - - + - - -\n')
    for row in range(0, 3):
        for col in range(0, 3):
            boardPrint.append(board[2][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('| ')
        for col in range(0, 3):
            boardPrint.append(board[3][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('\n')
    boardPrint.append('- - - + - - -')
    print ''.join(boardPrint)

#3/2 2R
def makeMove(move, turn):
    add = move.split(' ')[0]
    rotate = move.split(' ')[1]
    if(turn == True):
        turn = 'w'
    else:
        turn = 'b'

    if (board[int(add[0]) - 1][int(add[2]) - 1] == '.'):
        board[int(add[0]) - 1][int(add[2]) - 1] = turn
        rotateBoard(int(rotate[0]) - 1, rotate[1])
        return True
    else:
        return False

def rotateBoard(number, direction):
    global board
    # 0 1 2   R   6 3 0
    # 3 4 5       7 4 1
    # 6 7 8       8 5 2
    #
    # 0 1 2 3 4 5 6 7 8
    # 6 3 0 7 4 1 8 5 3
    #
    # 0 1 2   L   2 5 8
    # 3 4 5       1 4 7
    # 6 7 8       0 3 6
    #
    # 0 1 2 3 4 5 6 7 8
    # 2 5 8 1 4 6 0 3 6
    start = board[number]
    end = []
    #Right, CW
    if (direction.lower() == 'r'):
        for col in range(3):
            end.append(start[col + 6])
            end.append(start[col + 3])
            end.append(start[col + 0])
    #Left, CCW
    if (direction.lower() == 'l'):
        for col in range(2, -1, -1):
            end.append(start[col + 0])
            end.append(start[col + 3])
            end.append(start[col + 6])

    for count in range(len(end)):
        board[number][count] = end[count]

def checkForEnd():
    global board
    matchFound = False

    return matchFound

def main():
    global board, intro
    print intro
    game_end = False
    turn = True
    printBoard()

    while(game_end == False):
        game_end = checkForEnd()

        nextMove = raw_input("What would you like to do? ")
        if (nextMove.lower() == "exit" or nextMove.lower() == "end"):
            game_end = True
        if (nextMove.lower() == "debug"):
            makeMove("1/1 4l", True)
            makeMove("1/2 4l", True)
            makeMove("1/3 4l", True)
            makeMove("2/1 4l", True)
            makeMove("2/2 4l", True)
            print board
            printBoard()
        if (re.match("[1-4]/[1-9] [1-4][rl]", nextMove.lower())):
            moveValid = makeMove(nextMove, turn)
            if (moveValid == True):
                printBoard()
            else:
                nextMove = raw_input("Error, try again: ")
        turn = not turn

main()
