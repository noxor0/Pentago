import sys
import re
import os
from random import randint
from copy import deepcopy

intro = """Hello! Welcome to Pentago.
Move command: board/space board rotation.
Like this 3/1 3r\n"""
useAB = False
board = [[], [], [], []]
#just used for printing - DONT FORGET THIS AGAIN
boardTotal = []
for z in range(4):
    board[z] = ['.' for x in range(9)]

class node():
    def __init__(self, theBoardState, theMove, theLevel, theTurn, theParent):
        global useAB
        self.boardState = list(theBoardState)
        self.parent = theParent
        self.depth = None
        if (self.parent == None):
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
        self.move = theMove
        self.turn = theTurn
        self.value = None
        self.level = theLevel
        self.nextTurns = []
        self.nextNodes = []
        self.alpha = -1000
        self.beta = 1000
        if (useAB == True):
            if (self.level < 2):
                self.getNextAB()
            else:
                self.value = self.randomH()
                if (self.turn == True):
                    self.alpha = self.value
                else:
                    self.beta = self.value
        else:
            if (self.level < 2):
                self.getNext()
            else:
                self.value = self.randomH()

    #Determines the best move based on the tree created
    def determineMove(self):
        for nodeN in self.nextNodes:
            print nodeN.alpha, nodeN.beta
            if (nodeN.value == self.value):
                return nodeN.move

    #a perfect heuristic
    def randomH(self):
        return randint(-100,100)

    #A very bad heuristic that is geared to getting 3 pieces in a row
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
                            if (count == 2):
                                if (turnSymbol == 'b'):
                                    score += 2
                                else:
                                    score += -2
                            if (count == 3):
                                if (turnSymbol == 'b'):
                                    score += 10
                                else:
                                    score += -10
        return score

    #runs all possible turns for all possible directions and invokes creates
    #all nodes based on what would happen IF the move was taken.
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
                self.moveMinMax(possMoves, rotPair, self.turn)

    def getNextAB(self):
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
                self.moveAlphaBeta(possMoves, rotPair, self.turn)

    #builds the the tree and assigns values to non-terminal leaf nodes based on
    #the alphabeta pruning algorithm. This simulates a turn on the board.
    def moveAlphaBeta(self, thePlace, theRot, theTurn):
        theMove = ''.join([thePlace, ' ', theRot])
        boardCpy = deepcopy(self.boardState)
        #make move
        if (theTurn == False):
            boardCpy[int(thePlace[0]) - 1][int(thePlace[2]) - 1] = 'b'
        else:
            boardCpy[int(thePlace[0]) - 1][int(thePlace[2]) - 1] = 'w'
        #start rotating
        start = boardCpy[int(theRot[0]) - 1]
        end = []
        #Right, CW
        if (theRot[1] == 'r'):
            for col in range(3):
                end.append(start[col + 6])
                end.append(start[col + 3])
                end.append(start[col + 0])
        #Left, CCW
        if (theRot[1] == 'l'):
            for col in range(2, -1, -1):
                end.append(start[col + 0])
                end.append(start[col + 3])
                end.append(start[col + 6])

        for count in range(len(end)):
            boardCpy[int(theRot[0]) - 1][count] = end[count]

        if(boardCpy not in self.nextTurns):
            newNode = node(boardCpy, theMove, self.level+1, not self.turn, self)
            if (self.depth < 2):
                if (self.turn == True):
                    if (self.alpha < newNode.beta):
                        self.alpha = newNode.beta
                else:
                    if(self.beta < newNode.alpha):
                        self.beta = newNode.alpha
            self.nextNodes.append(newNode)
            self.nextTurns.append(boardCpy)

    #builds the the tree and assigns values to non-terminal leaf nodes based on
    #the minimax algorithm. This simulates a turn on the board.
    def moveMinMax(self, thePlace, theRot, theTurn):
        theMove = ''.join([thePlace, ' ', theRot])
        boardCpy = deepcopy(self.boardState)
        #make move
        if (theTurn == False):
            boardCpy[int(thePlace[0]) - 1][int(thePlace[2]) - 1] = 'b'
        else:
            boardCpy[int(thePlace[0]) - 1][int(thePlace[2]) - 1] = 'w'
        #start rotating
        start = boardCpy[int(theRot[0]) - 1]
        end = []
        #Right, CW
        if (theRot[1] == 'r'):
            for col in range(3):
                end.append(start[col + 6])
                end.append(start[col + 3])
                end.append(start[col + 0])
        #Left, CCW
        if (theRot[1] == 'l'):
            for col in range(2, -1, -1):
                end.append(start[col + 0])
                end.append(start[col + 3])
                end.append(start[col + 6])

        for count in range(len(end)):
            boardCpy[int(theRot[0]) - 1][count] = end[count]

        if(boardCpy not in self.nextTurns):
            newNode = node(boardCpy, theMove, self.level+1, not self.turn, self)
            self.nextNodes.append(newNode)
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
                    if (count == 5):
                        print "player", turnSymbol, "wins!"
                        return True
                    if (pos5InRow > 35 or pos5InRow < 0):
                        break
    return False

def main():
    global board, intro
    print intro
    game_end = False
    turn = True
    while(game_end == False):
        printBoard()
        if (turn == False):
            node0 = node(board, "0/0 1n", 0, turn, None)
            moveToMake = node0.determineMove()
            makeMove(moveToMake, turn)
            print "Maximillion moved", moveToMake
            turn = not turn
        else:
            nextMove = raw_input("What would you like to do? ")
            if (nextMove.lower() == "exit" or nextMove.lower() == "end"):
                sys.exit("Bye Bye")
            if (nextMove.lower() == "debug"):
                makeMove("1/2 4n", True)
                makeMove("1/6 4n", True)
                makeMove("2/7 4n", True)
                makeMove("4/2 4n", True)
                makeMove("4/6 4n", True)
                printBoard()
            if (re.match("[1-4]/[1-9] [1-4][rln]", nextMove.lower())):
                print nextMove
                moveValid = makeMove(nextMove, turn)
                if (moveValid == True):
                    turn = not turn
                    # os.system('clear')
                else:
                    nextMove = raw_input("Error, try again: ")
        if (checkForEnd() == True):
            break

main()
