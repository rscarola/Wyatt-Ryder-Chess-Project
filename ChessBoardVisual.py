import cv2
import numpy as np

'''
---------------------------------------------------------------------------------------------------
Functions
---------------------------------------------------------------------------------------------------

VideoProcess is the function which calls the videofeed which we take the frame of if space
is pressed. That part is in the general code. It also draws two lines over the frame so 
that you can line up the physical board and thus the capture is smooth. 
'''
def videoProcess(whichSource=0):
    vidCap = cv2.VideoCapture(whichSource)

    while True:
        ret, frame = vidCap.read()
        if not ret:
            break
        x = cv2.waitKey(10)
        if x > 0 and chr(x) == 'q':
            break

        # lines to line up physical board. (Just to make sure the capture isn't weird so the ROI works
        cv2.line(frame, (300, 1000), (1500, 1000), (100, 100, 230), 10)
        cv2.line(frame, (300, 100), (300, 1000), (100, 100, 230), 10)

        cv2.imshow("Video", frame)
        # next line tells the main code what button is pressed, we use this for frame capture.
        key = cv2.waitKey(1) & 0xFF

        # yield here so that the loop can continue while we tell whether space was pressed or not
        yield key, frame

    vidCap.release()
    cv2.destroyAllWindows()

'''
mouse_click captures the x and y coordinates when the user clicks a spot on the "Select 4 points"
window. This is then used to get the 4 coordinates for a warp prespective function later. 
It will only capture 4 points and use that for all analysis until the program terminates.
Points have to be click in certain order for rest of code to work - 
top left, top right, bottom right, bottom left
'''
def mouseclick(event, x, y, flags, param):
    # so we can access the points coordinates outside of this function
    global points

    # appends the 4 x and y coordinates to points and prints them in console.
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append([x, y])
        print(f"Point {len(points)}: ({x}, {y})")

'''
Warpimage starts by prompting for the user to select points for the warp prespective
it draws circles where the user clicks and exits once 4 spots have been clicked. 
It then maps the points to certain spots of the prespective warp, creates a matrix which
it uses with the points to form a warp prespective board. 
Finally we change the new board to grey instead of color for later color pixel thresholding
'''
def warpimage(image):

    cv2.namedWindow("Select 4 Points")
    cv2.setMouseCallback("Select 4 Points", mouseclick)

    while True:

        temp = currentBoard.copy()

        # Draw selected points
        for p in points:
            cv2.circle(temp, tuple(p), 20, (0, 0, 255), -1)

        cv2.imshow("Select 4 Points", temp)

        # Exit once 4 points are selected
        if len(points) == 4:
            break

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
    cv2.destroyAllWindows()

    '''
    helper function which is responsible for mapping points to corners
    '''
    def order_points(pts):
        pts = np.array(pts, dtype="float32")

        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)

        ordered = np.zeros((4, 2), dtype="float32")
        ordered[0] = pts[np.argmin(s)]  # top-left
        ordered[2] = pts[np.argmax(s)]  # bottom-right
        ordered[1] = pts[np.argmin(diff)]  # top-right
        ordered[3] = pts[np.argmax(diff)]  # bottom-left

        return ordered

    src_pts = order_points(points)

    width = 500
    height = 700

    dst_pts = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # last 3 lines create the warpPrespective board and make it grey then pass it back to main code
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(currentBoard, M, (width, height))
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    return warped

'''
Creates 64 different ROI's starting with the bottom left square where it looks at the 
center of that square and then adds the average of all its grey color values together 
and puts them in a list. This is what is used for seeing if a square changes from frame to frame
once it adds the value to the list is continues for all 63 other squares then stops. 
'''
def roiProcessing (image):
    current_value = []
    incrementx = 60
    incrementy = -88
    for l in range(8):

        starty = 622 + incrementy * l
        endy = 690 + incrementy * l
        for i in range(8):
            startx = 10 + incrementx * i
            endx = 50 + incrementx * i
            if i > 3:
                startx += 10
                endx += 10
            img = image[starty:endy, startx:endx]
            mean_val = np.mean(img)
            current_value.append(mean_val)
            cv2.imshow("Previous", image)
            cv2.imshow("Move0", img)
            cv2.waitKey(10)


    return(current_value)

'''
small function which changes the numbers it deduces to be the squares changed into chess 
notation for the final product. Note: not in any particular order, just the two spaces that were changed. 
'''
def chess_notation(idex):
    files = "abcdefgh"
    rank = 8 - (idex // 8) #this is the number part of the notation
    file = files[7 - (idex % 8)] # this is the letter part of the notation
    return f"{file}{rank}" # returns them to be printed by the main code.

'''
---------------------------------------------------------------------------------------------------
Main Code Script
----------------------------------------------------------------------------------------------------
'''
# setup
ChessImages = []
points = []
current_value = []
comparison_values = []
previous_value = None

'''
Main code which uses the functions above to get two frames and then compare them, resulting in two spaces in chess notation
will run until the code is manually stopped or by pressing q, but can continuously compare the last frame to the current one. 
'''
for key, frame in videoProcess(0):

    if key == ord('q'):
        break

    if key == ord(' '):  # When SPACE is pressed create a new warped image with functions
        currentBoard = frame.copy()
        warped = warpimage(currentBoard)
        current_value = roiProcessing(warped)

        # everything within this if statement is comparison
        if previous_value is not None:
            comparison_values = []
            THRESH = 5
            # looks for the difference of the absolute value of the average values between frames to be less than 5
            for i in range(64):
                diff = abs(previous_value[i] - current_value[i])
                comparison_values.append(diff)
            # assigns any squares with a change bigger than 5 to the changed_squares, then
            # calls the notation function which prints the chess notated squares.
            changed_squares = [i for i, d in enumerate(comparison_values) if d > THRESH]
            print("Changed squares:", [chess_notation(i) for i in changed_squares])


        else:
            print("Initial board captured")
        # replaces the previous mean values with the current ones and starts the camera again looking for a SPACE press.
        previous_value = current_value
