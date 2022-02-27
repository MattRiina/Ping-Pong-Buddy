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

    # look for orange ball based on HSV color space
    # orange is in range of [0, 20, 100] to [0, 130, 230] to [10, 255, 255] (in RGB space, not BGR or HSV)
    lower_orange = np.array([0, 20, 100])
    upper_orange = np.array([0, 130, 230])

    # convert to HSV color space
    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create mask
    mask = cv2.inRange(image, lower_orange, upper_orange)

    # find contours in the mask
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    # if no contours were found, exit
    if len(contours) == 0:
        print("No contours found in the image")
        sys.exit()
    
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    for c in contours:
        #c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        # draw the circle and centroid on the image,
        # then show the image
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)

    # show  the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)




#    # apply a gaussian blur to the image 
#     image = cv2.GaussianBlur(image, (11, 11), 0)

#     # show the image after applying the blur
#     cv2.imshow("Blurred", image)
#     cv2.waitKey(0)

#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # show the image after applying the gray scale
#     cv2.imshow("Gray", gray)
#     cv2.waitKey(0)

#     thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
#     # show the image after applying the threshold
#     cv2.imshow("Thresh", thresh)
#     cv2.waitKey(0)

#     kernel = np.ones((5,5),np.uint8)

#     after_open = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)
#     im_open_first = cv2.morphologyEx(after_open,cv2.MORPH_CLOSE,kernel)

#     # show the image after applying the open and close
#     cv2.imshow("Open and Close", im_open_first)
#     cv2.waitKey(0)

#     # perform a series of erosions and dilations to remove any small blobs of noise from the thresholded image
#     thresh = cv2.erode(thresh, None, iterations=2)
#     thresh = cv2.dilate(thresh, None, iterations=4)

#     # show the image after applying the erosions and dilations
#     cv2.imshow("Eroded", thresh)
#     cv2.waitKey(0)  

#     # show the output images
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     # cv2.imwrite("output.jpg", image)

#     # # get the difference between the frames
#     # diff = cv2.absdiff(frame1, frame2)
#     # gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     # blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     # _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#     # dilated = cv2.dilate(thresh, None, iterations=3)
#     # contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # # draw out each contour on frame
#     # for contour in contours:
#     #     (x, y, w, h) = cv2.boundingRect(contour)

#     #     if cv2.contourArea(contour) < 900:
#     #         continue

#     #     cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     #     cv2.putText(frame1, "Movement Detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)


    

    
