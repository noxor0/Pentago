import sys
import re
import os
from random import randint, getrandbits
from copy import deepcopy

intro = """Hello! Welcome to Pentago.
Move command: board/space board rotation.
Like this 3/1 3r\n"""

useAB = True
board = [[], [], [], []]
boardTotal = []
for z in range(4):
    board[z] = ['.' for x in range(9)]

#This is the ugliest piece of code I've ever written. If you ignore this,
#the rest of the code is pretty swell.
class node():
    def __init__(self, theBoardState, theMove, theLevel, theTurn, theParent, theA, theB):
        global useAB
        self.boardState = list(theBoardState)
        self.parent = theParent
        self.depth = None
        self.value = None
        if (self.parent == None):
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
        self.move = theMove
        self.turn = theTurn
        self.level = theLevel
        self.nextTurns = []
        self.nextNodes = []
        self.alpha = theA
        self.beta = theB
        #lol
        if (useAB == True):
            if (self.turn == True):
                self.value = -1000
            else:
                self.value = 1000
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
            if (nodeN.value == self.value):
                return nodeN.move

    #a perfect heuristic
    def randomH(self):
        return randint(-100,100)

    #A very bad heuristic that is geared to getting 3 pieces in a row
    #Check my github again in a couple of days - this will be much better :)
    #You never said this had to be good...
    #github.com/noxor0
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

        check = True
        for rotPair in rotations:
            for possMoves in openMoves:
                check = self.moveAlphaBeta(possMoves, rotPair, self.turn)
                if (check == False):
                    break
            if (check == False):
                break

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
            newNode = node(boardCpy, theMove, self.level+1, not self.turn, self, self.alpha, self.beta)
            if (self.depth < 2):
                if (self.turn == True):
                    self.alpha = max(self.alpha, newNode.value)
                    self.value = self.alpha
                    if (self.alpha < newNode.beta):
                        self.alpha = newNode.beta
                else:
                    self.beta = min(self.beta, newNode.value)
                    self.value = self.beta
                    if(self.beta > newNode.alpha):
                        self.beta = newNode.alpha

            if(self.alpha >= self.beta):
                return False
            self.nextNodes.append(newNode)
            self.nextTurns.append(boardCpy)
            return True

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
            newNode = node(boardCpy, theMove, self.level+1, not self.turn, self, 0, 0)
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
    wPlayer = 0
    bPlayer = 0
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
                        if (turnSymbol == 'w'):
                            wPlayer += 1
                            break
                        else:
                            bPlayer += 1
                            break
                    if (pos5InRow > 35 or pos5InRow < 0):
                        break
    if (wPlayer == bPlayer and wPlayer != 0):
        print "Tie game!"
        return True
    if (wPlayer > bPlayer):
        print "White Player wins!"
        return True
    if (bPlayer > wPlayer):
        print "Black Player wins!"
        return True
    else:
        return False

def main():
    writeFile = open('log.txt', 'w')
    global board, intro
    print intro
    game_end = False
    playerName = raw_input('Whats your name? ')
    #True means player first
    turn = bool(getrandbits(1))
    playerInfo = "New Game-------- \nPlayer 1: " + playerName
    if (turn == True):
        playerInfo += " goes first (W)\n"
    else:
        playerInfo += " goes second (B)\n"
    playerInfo += "Player 2: Maximillion"
    if (turn == False):
        playerInfo += " goes first (W)\n"
    else:
        playerInfo += " goes second (B)\n"
    writeFile.write(playerInfo)
    turnLog = []
    while(game_end == False):
        os.system('clear')
        print playerInfo
        printBoard()
        print "".join(turnLog)
        if (turn == False):
            node0 = node(board, "0/0 1n", 0, turn, None, -1000, 1000)
            moveToMake = node0.determineMove()
            makeMove(moveToMake, turn)
            turnLog.append("Maximillion moved" + moveToMake + '\n')
            print "Maximillion moved", moveToMake
            turn = not turn
        else:
            nextMove = raw_input("What would you like to do? ")
            if (nextMove.lower() == "exit" or nextMove.lower() == "end"):
                writeFile.write("".join(turnLog))
                break
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
                moveToWrite = playerName + " moved: " + nextMove + '\n'
                print moveToWrite
                turnLog.append(moveToWrite)
                if (moveValid == True):
                    turn = not turn

        if (checkForEnd() == True):
            writeFile.write("".join(turnLog))
            writeFile.close()
            break

main()
