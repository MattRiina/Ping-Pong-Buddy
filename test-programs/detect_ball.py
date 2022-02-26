import cv2
from imutils.video import VideoStream
import numpy as np
import imutils
import sys
import time
import imageio

if __name__ == "__main__":
    file = None
    file_name = None
    
    # parse argument for image file name
    file = sys.argv[1]
    # file_name = file.lower().split(".mov")[0]
    # file_name = file.lower().split(".mp4")[0]
    # file_name = file_name.split("/")[-1]
    # file_name = file_name.split("\\")[-1]
    

    # read in the input image using OpenCV
    image = cv2.imread(file)

   # apply a gaussian blur to the image 
    image = cv2.GaussianBlur(image, (11, 11), 0)

    # show the image after applying the blur
    cv2.imshow("Blurred", image)
    cv2.waitKey(0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # show the image after applying the gray scale
    cv2.imshow("Gray", gray)
    cv2.waitKey(0)

    num_labels, labels, stats, centroids = \
        cv2.connectedComponentsWithStats(gray, 8, cv2.CV_32S)

    colors = np.random.randint(0, 255, (num_labels, 3), dtype="uint8")
    img_colored = colors[labels]

    cv2.imshow("Connected components", img_colored)

    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    # show the image after applying the threshold
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)

    # find contours in the thresholded image
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # loop over the contours
    for c in contours[0]:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the
        # object is
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, "Movement Detected", (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

    # show the output images
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imwrite("output.jpg", image)

    # # get the difference between the frames
    # diff = cv2.absdiff(frame1, frame2)
    # gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # dilated = cv2.dilate(thresh, None, iterations=3)
    # contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # # draw out each contour on frame
    # for contour in contours:
    #     (x, y, w, h) = cv2.boundingRect(contour)

    #     if cv2.contourArea(contour) < 900:
    #         continue

    #     cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     cv2.putText(frame1, "Movement Detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)


    

    
