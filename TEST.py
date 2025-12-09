
import cv2

ChessImages = []


for i in range(2):
    filename = f"Chess Game/Move{i}.jpg"
    img = cv2.imread(filename)
    ChessImages.append(img)

imagewidth = 200
imageheight = 200
startx1 = 1450
endx = startx1 + imagewidth
starty1 = 3300
endy = starty1 + imageheight

currentBoard = ChessImages[0]
move1Board = ChessImages[1]
for r in range(8):
    if r <= 1:
        startx1 = 1450
        endx = startx1 + imagewidth
        starty1 = 3300 - 360 * r
        endy = starty1 + imageheight
        shifty = 0
        shiftx = 0 + 10 * r
        change = 380
    if r == 2 or r == 3:
        startx1 = 1450
        endx = startx1 + imagewidth
        starty1 = 3300 - 360 * r
        endy = starty1 + imageheight
        shifty = 0
        shiftx = 0 + 10 * r
        change = 370
    if r == 4 or r == 5:
        startx1 = 1490
        endx = startx1 + imagewidth
        starty1 = 3300 - 360 * r
        endy = starty1 + imageheight
        shifty = 20
        shiftx = 0 - 5 * r
        change = 365
    if r > 5:
        startx1 = 1530
        endx = startx1 + imagewidth
        starty1 = 3290 - 355 * r
        endy = starty1 + imageheight
        shifty = 20
        shiftx = 0 - 5 * r
        change = 350
    for i in range(8):
        cv2.rectangle(move1Board, (startx1 + shiftx, starty1 + shifty), (endx+ shiftx, endy + shifty), (300, 100, 100), 3)
        roi0 = move1Board[starty1 + shifty:endy + shifty, startx1 + shiftx : endx + shiftx, :]
        startx1 = startx1 + change
        endx = startx1 + imagewidth
        shifty -= 10
        print(startx1, starty1)
        cv2.imshow("ROI - noMove", roi0)

"""startx2 = 1500
endx = startx2 + imagewidth
starty2 = 900 + 330
endy = starty2 + imageheight
for i in range(8):
    cv2.rectangle(currentBoard, (startx2 + shiftx, starty2 + shifty), (endx + shiftx, endy + shifty), (300, 100, 100), 3)
    startx2 = startx2 + 350
    endx = startx2 + imagewidth
    shifty -= 10
    print(startx2, starty2)
"""
cv2.imshow("Chess", move1Board)
cv2.waitKey(0)