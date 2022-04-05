import cv2
from imutils.video import VideoStream
import numpy as np
import imutils
import sys
import time



# TODO: use new videos collected to come up with different thresholds for everything

# Rertroreflective tape (paint)


if __name__ == "__main__":
    file = None
    feed = None
    file_name = None
    
    # parse argument for video file name (if specified)
    if len(sys.argv) > 1:
        file = sys.argv[1]
        feed = cv2.VideoCapture(file)
        file_name = file.lower().split(".mov")[0]
        file_name = file_name.split("/")[-1]
        file_name = file_name.split("\\")[-1]
    else:
        feed = cv2.VideoCapture(0)

    # allow the camera or video file to warm up
    time.sleep(2.0)

    # look for orange ball based on HSV color space
    lower_orange = np.array([15, 25, 35]) #HSV
    upper_orange = np.array([40, 100, 100]) #HSV

    # convert to HSV color space from real-world color space
    lower_orange[0] = lower_orange[0] / 2.0
    upper_orange[0] = upper_orange[0] / 2.0
    lower_orange[1] = lower_orange[1] * 255.0 / 100.0
    upper_orange[1] = upper_orange[1] * 255.0 / 100.0
    lower_orange[2] = lower_orange[2] * 255.0 / 100.0
    upper_orange[2] = upper_orange[2] * 255.0 / 100.0

    ret, frame1 = feed.read()
    ret, frame2 = feed.read()

    image_list = []
    ball_locations = []
    consecutive_frames_without_ball = 0

    while True:
        # get the difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        # contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        blur_current = cv2.GaussianBlur(frame2, (5, 5), 0)
        hsv = cv2.cvtColor(blur_current, cv2.COLOR_BGR2HSV)

        # find the orange ball
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        colored_mask = frame2.copy()
        colored_mask[np.where(mask == 0)] = [0,0,0]

        tmp = dilated[np.where(colored_mask != [0,0,0])[0:2]]

        contours, _ = cv2.findContours(tmp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        orange_locations = {}

        # loop through each orange contour found
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # TEMPORARILY REMOVE THIS FOR DEBUGGING
            if radius > 10 and radius < 55:
                orange_locations[(int(x), int(y))] = [radius, center]

        for mot_c in contours:
            # only proceed if the contour is large enough
            if cv2.contourArea(mot_c) < 1000:
                continue

            # compute the center of the contour
            M = cv2.moments(mot_c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            locations_initial = len(orange_locations)

            # check to see if this center is near any of the orange locations
            for (x, y), (radius, o_center) in orange_locations.items():
                # calculate the distance between the center of the contour and the orange location
                dist = np.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)

                # if the distance is less than the radius of the orange
                if dist <= radius + 10:
                    # draw a circle around the orange
                    cv2.circle(frame2, o_center, int(radius), (0, 255, 255), 2)

                    print("Orange found at: " + str(o_center) + " with radius: " + str(radius))
                    if radius > 10 and radius < 35:
                        consecutive_frames_without_ball = 0

                        # add the contour and location to the list
                        ball_locations.append([mot_c, o_center])

                        # draw path from previous location to current location
                        if len(ball_locations) > 1:
                            # draw path of the ball
                            for i in range(len(ball_locations) - 1):
                                cv2.line(frame2, ball_locations[i][1], ball_locations[i+1][1], (0, 255, 255), 2)
                            #cv2.line(frame2, ball_locations[-2][1], o_center, (0, 255, 255), 2)
            
            # if there were no matches, ball is most likely off screen
            if len(orange_locations) == locations_initial:
                consecutive_frames_without_ball += 1
            
            if consecutive_frames_without_ball > 30:
                # clear the list of locations to draw new ball path later
                ball_locations = []
                consecutive_frames_without_ball = 0

        print()

        # update the points queue
        image_list.append(frame1)

        # show the frame to our screen
        cv2.imshow("Frame", frame1)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

        # get the next frame
        frame1 = frame2
        ret, frame2 = feed.read()

        # break when frames are exhausted
        if frame2 is None:
            break

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    feed.release()

    # Close all windows
    cv2.destroyAllWindows()
