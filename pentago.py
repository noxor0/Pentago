import sys
import re
import os
from copy import deepcopy
intro = """Hello! Welcome to Pentago.
Move command: board/space board rotation.
Like this 3/1 3r\n"""

board = [[], [], [], []]
#just used for printing - DONT FORGET THIS AGAIN
boardTotal = []
for z in range(4):
    board[z] = ['.' for x in range(9)]

class node():
    def __init__(self, boardState, theMove, level):
        self.boardState = list(boardState)
        # self.value = self.heuristic()
        self.value = 1
        self.move = theMove
        self.level = level
        self.turn = False
        self.parent = None
        self.nextTurns = []
        self.nextNodes = []
        if (level < 1):
            self.getNext()

    def determineMove(self):
        newMove = self.move
        valueToBeat = -1000
        for nodeN in self.nextNodes:
            if(nodeN.value > valueToBeat):
                valueToBeat = nodeN.value
                newMove = nodeN.move
        return newMove

    def heuristic(self):
        score = 0
        possibleDir = [3, 1, -2, 4]
        for boardSec in self.boardState:
            for cellNum in range(9):
                if(boardSec[cellNum] != '.'):
                    for direction in possibleDir:
                        turnSymbol = boardSec[cellNum]
                        count = 0
                        pos3InRow = cellNum
                        prevCol = pos3InRow % 3
                        while(boardTotal[pos3InRow] == turnSymbol):
                            if (prevCol > pos3InRow % 3):
                                break
                            count += 1
                            if (turnSymbol == 'b'):
                                score += 2
                            else:
                                score += -2
                            prevCol = pos3InRow % 3
                            pos3InRow += direction
                            if (pos3InRow > 8 or pos3InRow < 0):
                                break
                            if (count == 3):
                                if (turnSymbol == 'b'):
                                    score += 10
                                else:
                                    score += -10
        return score

    def getNext(self):
        rotations = ["1l", "1r", "2l", "2r", "3l", "3r", "4l", "4r",]
        openMoves = []
        for boardNum in range(4):
            for spot in range(9):
                if (self.boardState[boardNum][spot] == '.'):
                    boardNumStr = str(boardNum + 1)
                    spotStr = str(spot + 1)
                    openMoves.append(''.join([boardNumStr, '/' ,spotStr]))

        for rotPair in rotations:
            for possMoves in openMoves:
                self.tempMove(possMoves, rotPair)

    def tempMove(self, move, rot):
        theMove = ''.join([move, ' ', rot])
        self.move = theMove
        boardCpy = deepcopy(self.boardState)
        #make move
        boardCpy[int(move[0]) - 1][int(move[2]) - 1] = 'b'
        #start rotating
        start = boardCpy[int(rot[0]) - 1]
        end = []
        #Right, CW
        if (rot[1] == 'r'):
            for col in range(3):
                end.append(start[col + 6])
                end.append(start[col + 3])
                end.append(start[col + 0])
        #Left, CCW
        if (rot[1] == 'l'):
            for col in range(2, -1, -1):
                end.append(start[col + 0])
                end.append(start[col + 3])
                end.append(start[col + 6])

        for count in range(len(end)):
            boardCpy[int(rot[0]) - 1][count] = end[count]

        if(boardCpy not in self.nextTurns):
            self.nextNodes.append(node(boardCpy, theMove, self.level+1))
            self.nextTurns.append(boardCpy)

def printBoard():
    global board, boardTotal
    boardTotal = []
    boardPrint = []
    boardPrint.append('Pantego - - -\n')
    for row in range(0, 3):
        for col in range(0, 3):
            boardPrint.append(board[0][row * 3 + col])
            boardTotal.append(board[0][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('| ')
        for col in range(0, 3):
            boardPrint.append(board[1][row * 3 + col])
            boardTotal.append(board[1][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('\n')
    boardPrint.append('- - - + - - -\n')
    for row in range(0, 3):
        for col in range(0, 3):
            boardPrint.append(board[2][row * 3 + col])
            boardTotal.append(board[2][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('| ')
        for col in range(0, 3):
            boardPrint.append(board[3][row * 3 + col])
            boardTotal.append(board[3][row * 3 + col])
            boardPrint.append(' ')
        boardPrint.append('\n')
    boardPrint.append('- - - + - - -')
    print ''.join(boardPrint)

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
    global boardTotal
    #Possible directions to win
    #vert +6 | hori +1 - rdia +5 / ldia -7 \
    possibleDir = [6, 1, -5, 7]
    for cellNum in range(36):
        if(boardTotal[cellNum] != '.'):
            for direction in possibleDir:
                turnSymbol = boardTotal[cellNum]
                count = 0
                pos5InRow = cellNum
                prevCol = pos5InRow % 6
                while(boardTotal[pos5InRow] == turnSymbol):
                    if (prevCol > pos5InRow % 6):
                        break
                    count += 1
                    prevCol = pos5InRow % 6
                    pos5InRow += direction
                    if (pos5InRow > 35 or pos5InRow < 0):
                        break
                    if (count == 5):
                        print "you win!"
                        return True
    return False

def main():
    global board, intro
    print intro
    game_end = False
    turn = True
    while(game_end == False):
        printBoard()
        if (turn == False):
            node0 = node(board, "0/0 1n", 0)
            makeMove(node0.determineMove(), turn)
            print "Maximillion moved", node0.determineMove()
            turn = not turn
        else:
            nextMove = raw_input("What would you like to do? ")
            if (nextMove.lower() == "exit" or nextMove.lower() == "end"):
                sys.exit("Bye Bye")
            if(nextMove.lower() == "test"):
                node0 = node(board, "2/4 3n", 0)
            if (nextMove.lower() == "debug"):
                makeMove("1/6 4n", False)
                makeMove("1/5 4n", False)
                makeMove("2/5 4n", False)
                makeMove("3/5 4n", True)
                makeMove("4/5 4n", True)
                makeMove("4/8 4n", True)
                printBoard()
            if (re.match("[1-4]/[1-9] [1-4][rln]", nextMove.lower())):
                print nextMove
                moveValid = makeMove(nextMove, turn)
                if (moveValid == True):
                    turn = not turn
                    os.system('clear')
                else:
                    nextMove = raw_input("Error, try again: ")
        game_end = checkForEnd()

main()
