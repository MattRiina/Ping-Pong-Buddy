import cv2
from imutils.video import VideoStream
import numpy as np
import imutils
import sys
import time

if __name__ == "__main__":
    file = None
    feed = None
    
    # parse argument for video file name (if specified)
    if len(sys.argv) > 1:
        file = sys.argv[1]
        feed = cv2.VideoCapture(file)
    else:
        feed = cv2.VideoCapture(0)

    # allow the camera or video file to warm up
    time.sleep(2.0)

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

        # draw out each contour on frame
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 900:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Movement Detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        # show the frame
        cv2.imshow("feed", frame1)

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
