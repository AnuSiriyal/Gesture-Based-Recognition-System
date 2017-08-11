import cv2 #import opencv -open source computer vision..OpenCV was designed for computational efficiency and with a strong focus on real-time applications
import numpy as np #NumPy is the fundamental package for scientific computing with Python
import math
import time
import webbrowser
new=2
url="http://facebook.com"
url1="http://twitter.com"
url2="http://google.com"

cap = cv2.VideoCapture(0)#To capture a video, you need to create a VideoCapture object. 
						#Its argument can be either the device index or the name of a video file. 
						#Device index is just the number to specify which camera. Normally one camera 
						#will be connected (as in my case). So I simply pass 0 (or -1). You can select 
						#the second camera by passing 1 and so on. After that, you can capture frame-by-frame.


while(cap.isOpened()):  #Sometimes, cap may not have 
						#initialized the capture. In that case, this code shows error. 
						#You can check whether it is initialized or not by the method cap.isOpened().
#    if measure(time.clock()) < 5
        ret, img = cap.read()  #cap.read() returns a bool (True/False). If frame is read correctly, it will be True. 
								#So you can check end of the video by checking this return value
        cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)#for rectangle formation or cutting image to a particular rectangular form
        crop_img = img[100:300, 100:300]#image stored as array is cropped to the region of interest
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)#convert RGB to gray scale image
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0) #blur the image using gaussian filter
        _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #threshold the image.. cv2.THRESH_OTSU is for optimal thresholding
        cv2.imshow('Thresholded', thresh1)#image is displayed in a window with window name as Thresholded and the image thresh1
        #time.sleep(5)
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                cv2.CHAIN_APPROX_NONE)#Contours can be explained simply as a curve joining all the continuous points (along the boundary), having same 
										#color or intensity. The contours are a useful tool for shape analysis and object detection and recognition.
										#For better accuracy, use binary images. So before finding contours, apply threshold or canny edge detection.
										#findContours function modifies the source image. So if you want source image even after finding contours, already 
										#store it to some other variables.
										#In OpenCV, finding contours is like finding white object from black background. So remember, object to be found 
										#should be white and background should be black.
        max_area = -1
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)#finds area between contours-2D
            if(area>max_area):
                max_area=area
                ci=i
        cnt=contours[ci]
        x,y,w,h = cv2.boundingRect(cnt) #It is a straight rectangle, it doesn't consider the rotation of the object. So area of the bounding rectangle won't be minimum. I
										#t is found by the function 
        cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
        hull = cv2.convexHull(cnt) #Convex Hull will look similar to contour approximation, but it is not (Both may provide same results in some cases). 
									#Here, cv2.convexHull() function checks a curve for convexity defects and corrects it. Generally speaking, convex 
									#curves are the curves which are always bulged out, or at-least flat. And if it is bulged inside, it is called convexity defects.
        drawing = np.zeros(crop_img.shape,np.uint8) #Return a new array of given shape and type, filled with zeros.
        cv2.drawContours(drawing,[cnt],0,(0,255,0),0) #To draw the contours, cv2.drawContours function is used. It can also be used to draw any shape provided you have 
														#its boundary points. Its first argument is source image, second argument is the contours which should be passed 
														#as a Python list, third argument is index of contours (useful when drawing individual contour. To draw all contours, 
														#pass -1) and remaining arguments are color, thickness etc.
        cv2.drawContours(drawing,[hull],0,(0,0,255),0)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)#It returns an array where each row contains these values - [ start point, end point, farthest point, approximate distance 
												#to farthest point ]. We can visualize it using an image. We draw a line joining start point and end point, then draw a 
												#circle at the farthest point. Remember first three values returned are indices of cnt. So we have to bring those values from cnt.
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img,far,1,[0,0,255],-1)
            cv2.line(crop_img,start,end,[0,255,0],2)
        if count_defects == 1:
#        str = "Thats 2"
 #       cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            webbrowser.open(url, new=new)
            break
        #time.sleep(5)
        elif count_defects == 2:
        #str = "thats 3"
        #cv2.putText(img, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            webbrowser.open(url1, new=new)
            break
    #         time.sleep(5)
        elif count_defects == 3:
            webbrowser.open(url2, new=new)
            break
        #time.sleep(5)
        #cv2.putText(img,"thats 4", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(img,"thats 5", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            cv2.putText(img,"Hello World!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
    #cv2.imshow('Contours', all_img)
        k = cv2.waitKey(10)
        if k == 27:
            break