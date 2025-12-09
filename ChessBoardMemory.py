


import numpy as np
from numpy.array_api import uint8
import cv2


'''
-----------------------------------------------------------------------------------------------------------------------
Set up
'''

chessBoard = np.zeros([8,8], dtype = uint8)
chessBoard[0:1, :] = (2, 3, 4, 5, 6, 4, 3, 2)
chessBoard[1:2, :] = (1, 1, 1, 1, 1, 1, 1, 1)
chessBoard[7:8, :] = (12, 13, 14, 15, 16, 14, 13, 12)
chessBoard[6:7, :] = (11, 11, 11, 11, 11, 11, 11, 11)

'''
-----------------------------------------------------------------------------------------------------------------------

'''


'''
------------------------------------------------------------------------------------------------------------------------
Functions
'''
def CallBoard():
    CharacterBoard()
    isMovement()



def CharacterBoard():
    chess = []
    k = 0
    piece = "-"
    print("-" * 48)
    for r in range(8):
        rows = []
        for c in range(8):
            letter = chessBoard[r, c]
            if letter == 0:
                piece = "--"
            if letter == 1:
                piece = "bP"
            if letter == 2:
                piece = "bR"
            if letter == 3:
                piece = "bN"
            if letter == 4:
                piece = "bB"
            if letter == 5:
                piece = "bK"
            if letter == 6:
                piece = "bQ"
            if letter == 11:
                piece = "wP"
            if letter == 12:
                piece = "wR"
            if letter == 13:
                piece = "wN"
            if letter == 14:
                piece = "wB"
            if letter == 15:
                piece = "wK"
            if letter == 16:
                piece = "wQ"
            rows.append(piece)
        chess.append(rows)

    for row in chess:
        print(row)
    print("-" * 48)


def isMovement():
    check = 0
    for x in range(8):
        for y in range(8):
            previousBoardvalue = previousBoard[y, x]
            currentBoardvalue = chessBoard[y, x]
            if previousBoardvalue - currentBoardvalue != 0:
                if check == 0:
                    y1 = y
                    x1 = x
                    check = previousBoardvalue - currentBoardvalue
                else:
                    y2 = y
                    x2 = x

    if check == 0:
        print("False")

    else:
        print("True", "x1:", x1+1, "y1:", y1+1)
        print("True", "x2:", x2+1, "y2:", y2+1)
        if previousBoard[y1, x1] == 0:
            print("Change occurred at: ", x1+1, y1+1)
        else:
            print("Change occurred at: ", x2+1, y2+1)
    cv2.waitKey(3000)


'''
-----------------------------------------------------------------------------------------------------------------------
'''
# Initial Board, So previousBoard has something to compare to

CharacterBoard()
previousBoard = chessBoard.copy()
cv2.waitKey(3000)

# Move 1
chessBoard[6:7, 3:4] = 0
chessBoard[4:5, 3:4] = 11
CallBoard()
previousBoard = chessBoard.copy()

# Fake Move Call
CallBoard()
previousBoard = chessBoard.copy()

# Move 2
chessBoard[1:2, 3:4] = 0
chessBoard[3:4, 3:4] = 1
CallBoard()
previousBoard = chessBoard.copy()

# Move 3
chessBoard[7:8, 6:7] = 0
chessBoard[5:6, 5:6] = 12
CallBoard()
previousBoard = chessBoard.copy()