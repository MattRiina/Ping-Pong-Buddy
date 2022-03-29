import cv2
from imutils.video import VideoStream
import numpy as np
import imutils
import sys
import time


# TODO: try doing color detection off the difference of the frames: ball comes up as orage-ish, and background as black

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

    while True:
        # get the difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        blur_current = cv2.GaussianBlur(frame2, (5, 5), 0)
        hsv = cv2.cvtColor(blur_current, cv2.COLOR_BGR2HSV)

        # find the orange ball
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        for mot_c in contours:
            # only proceed if the contour is large enough
            if cv2.contourArea(mot_c) < 1000:
                continue

            # compute the center of the contour
            M = cv2.moments(mot_c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # draw the contour and center of the shape on the image
            cv2.drawContours(frame1, [mot_c], -1, (0, 255, 0), 2)
            cv2.circle(frame1, center, 7, (255, 255, 255), -1)

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            for c in cnts:
            #c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame1, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame1, center, 5, (0, 0, 255), -1)

        # show the frame to our screen
        cv2.imshow("Frame", frame1)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
        elif key == ord("p"):
            cv2.waitKey(-1) # pause until key is pressed
        elif key == ord("d"):
            # start a custom debugging mode: print important variables and show useful images
            cv2.waitKey(-1) # pause until key is pressed

            # print the location of each orange contour with radius
            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                print("x(col): {}, y(row): {}, radius: {}".format(x, y, radius))

            # show color matches for ball
            cv2.imshow("Color Matches Mask", mask)
            cv2.waitKey(0)

            # show the motion difference between the frames
            cv2.imshow("Motion", diff)
            cv2.waitKey(0)

            # convert the mask from grayscale to RGB
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

            # show the intersection of the mask and the motion difference
            cv2.imshow("Mask and Motion", cv2.bitwise_and(mask, diff))
            cv2.waitKey(0)

       

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
