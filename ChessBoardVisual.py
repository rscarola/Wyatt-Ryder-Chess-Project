import cv2
import numpy as np


ChessImages = []

for i in range(2):
    filename = f"Chess Game/Move{i}.jpg"
    img = cv2.imread(filename)
    ChessImages.append(img)

print(len(ChessImages), ChessImages[len(ChessImages)-1])

originalBoard = ChessImages[0]
move1Board = ChessImages[1]

cv2.imshow("Chess", originalBoard)
#cv2.imshow("Move 1", move1Board)




print(originalBoard.shape)




startx = 1500
starty = 3250
endx = startx + 250
endy = starty + 250
incrementx = 400
incrementy = -350
currentBoard = originalBoard

for i in range(8):
    startx = 1500
    endx = startx + 450

    starty = 3250 + incrementy * i
    endy = 3500 + incrementy * i
    for l in range(8):
        startx = 1500 + incrementx * l
        endx = startx + 250
        roi0 = currentBoard[starty:endy, startx:endx, :]
        roi1 = move1Board[starty:endy, startx:endx, :]
        cv2.imshow("ROI - noMove", roi0)
        cv2.imshow("ROI - Move 1", roi1)
        cv2.moveWindow("ROI - Move 1", 200, -100)

        print(starty, startx, endy, endx)

        thres = 65

        min_vals0 = min(roi0.min(axis=(0, 1)))
        max_vals0 = max(roi0.max(axis=(0, 1)))
        min_vals1 = min(roi1.min(axis=(0, 1)))
        max_vals1 = max(roi1.max(axis=(0, 1)))

        #within_thres0 = np.all((max_vals0 - min_vals0) <= thres)
        #within_thres1 = np.all((max_vals1 - min_vals1) <= thres)
        move0 = max_vals0 - min_vals0
        move1 = max_vals1 - min_vals1
        higher = max(move0, move1)
        lower = min(move0, move1)
        val = higher - lower
        print(higher - lower)
        if val <=  thres:
            print("No significant change between frames")
        else:
            print("SOMETHING HAPPENED HERE")

        print("Move0:", move0,"Move1:", move1)


        c = cv2.waitKey(0)
        c = chr(c)
        if c == 'q':
            break
    if c == 'q':
        break