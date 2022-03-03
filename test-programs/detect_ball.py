import cv2
import numpy as np
import sys

if __name__ == "__main__":
    file = None
    file_name = None
    
    # parse argument for image file name
    file = sys.argv[1]    

    # read in the input image using OpenCV
    image = cv2.imread(file)

    # look for orange ball based on HSV color space
    lower_orange = np.array([20, 60, 35]) #HSV
    upper_orange = np.array([40, 100, 100]) #HSV

    # convert to HSV color space from real-world color space
    lower_orange[0] = lower_orange[0] / 2.0
    upper_orange[0] = upper_orange[0] / 2.0
    lower_orange[1] = lower_orange[1] * 255.0 / 100.0
    upper_orange[1] = upper_orange[1] * 255.0 / 100.0
    lower_orange[2] = lower_orange[2] * 255.0 / 100.0
    upper_orange[2] = upper_orange[2] * 255.0 / 100.0

    # convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create mask
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    result = cv2.bitwise_and(hsv, hsv, mask=mask)

    # show the images
    cv2.imshow("images", np.hstack([hsv, result]))
    cv2.waitKey(0)


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

        # now filter based on area


    # show  the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
