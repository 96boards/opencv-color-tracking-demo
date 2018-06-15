"""
Summary: 



Copyright 2018 Don Harbin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.


"""
import numpy as np
import cv2
import MM
import time
import imutils
import time


kernelOp = np.ones((3,3),np.uint8)
kernelOp1 = np.ones((7,7),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)

kernelCl = np.ones((11,11),np.uint8)
kernelCl1 = np.ones((20,20),np.uint8)
kernelCl2 = np.ones((25,25),np.uint8)

#Variables
font = cv2.FONT_HERSHEY_SIMPLEX
mm = []
max_p_age = 5
min_radius = 9        # Adjust to size of m & m. Impacted by distance from camera

#DEBUG import pdb; pdb.set_trace() # Begin debug

##########
# Create color objects  
# Note: Run the colorIsolationApp.py to define HSV min and max parms for each color.
##########

# RED
color_id = 0          # One for each color
redCircleColor = (0,0,255)
redTextLocation = (10,25)

red_hue_min = 158
red_saturation_min = 107 
red_value_min = 34 
red_hsv_min=np.array([red_hue_min,red_saturation_min,red_value_min])

red_hue_max = 193
red_saturation_max = 229 
red_value_max = 171
red_hsv_max=np.array([red_hue_max,red_saturation_max,red_value_max])

mm.append(MM.M_and_M(color_id, "Red",redCircleColor, red_hsv_min,red_hsv_max,redTextLocation))  # Create Red Tracking Object

# BLUE
color_id += 1
blueCircleColor = (255,0,0)
blueTextLocation = (10,50)

blue_hue_min = 84
blue_saturation_min = 77 
blue_value_min = 57 
blue_hsv_min=np.array([blue_hue_min,blue_saturation_min,blue_value_min])

blue_hue_max = 146
blue_saturation_max = 236 
blue_value_max = 160
blue_hsv_max=np.array([blue_hue_max,blue_saturation_max,blue_value_max])

mm.append(MM.M_and_M(color_id, "Blue",blueCircleColor, blue_hsv_min,blue_hsv_max,blueTextLocation))  # Create Red Tracking Object

# ORANGE
color_id += 1
orangeCircleColor = (0,125,255)
orangeTextLocation = (10,75)

orange_hue_min = 4
orange_saturation_min = 155 
orange_value_min = 104 
orange_hsv_min=np.array([orange_hue_min,orange_saturation_min,orange_value_min,])

orange_hue_max = 18
orange_saturation_max = 229 
orange_value_max = 174
orange_hsv_max=np.array([orange_hue_max,orange_saturation_max,orange_value_max])

mm.append(MM.M_and_M(color_id, "Orange",orangeCircleColor, orange_hsv_min,orange_hsv_max,orangeTextLocation))  # Create Red Tracking Object

# YELLOW
color_id += 1
yellowCircleColor = (0,255,255)
yellowTextLocation = (10,100)

yellow_hue_min = 18
yellow_saturation_min = 71 
yellow_value_min = 111 
yellow_hsv_min=np.array([yellow_hue_min,yellow_saturation_min,yellow_value_min])

yellow_hue_max =31
yellow_saturation_max = 215 
yellow_value_max = 190
yellow_hsv_max=np.array([yellow_hue_max,yellow_saturation_max,yellow_value_max])

mm.append(MM.M_and_M(color_id, "Yellow", yellowCircleColor, yellow_hsv_min,yellow_hsv_max,yellowTextLocation))  # Create Red Tracking Object

# BLACK
color_id += 1
blackCircleColor = (0,0,0)
blackTextLocation = (10,125)

black_hue_min = 137
black_saturation_min = 9 
black_value_min = 0 
black_hsv_min=np.array([black_hue_min,black_saturation_min,black_value_min])

black_hue_max = 222
black_saturation_max = 91 
black_value_max = 64
black_hsv_max=np.array([black_hue_max,black_saturation_max,black_value_max])

mm.append(MM.M_and_M(color_id, "Black", blackCircleColor, black_hsv_min,black_hsv_max,blackTextLocation ))  # Create Red Tracking Object

# GREEN
color_id += 1
greenCircleColor = (0,255,0)
greenTextLocation = (10,150)

green_hue_min = 42
green_saturation_min = 49 
green_value_min = 42 
green_hsv_min=np.array([green_hue_min,green_saturation_min,green_value_min])

green_hue_max = 76
green_saturation_max = 173 
green_value_max = 192
green_hsv_max=np.array([green_hue_max,green_saturation_max,green_value_max])

mm.append(MM.M_and_M(color_id, "Green",greenCircleColor, green_hsv_min,green_hsv_max, greenTextLocation))  # Create Red Tracking Object

##########
# Create video camera object and start streaming to it.
##########
cap = cv2.VideoCapture(0) # 0 == Continuous stream


# set up visual imaging for the trigger line that is the count line when crossed
cnt_down=0
y_trigger=160
trigger_line_color=(255,0,0)
trigger_line= np.array([[0, y_trigger],[720, y_trigger]])

counter=0

# Debug variables used to see how long it takes to process a frame.
millis1=0
millis2=0

##########
# Begin the count loop that reads/processes one frame at a time
##########
try:
    while(cap.isOpened()):
        # Capture a still image from the video stream
        ret, frame = cap.read() #read a frame
    
        #Debug code to gauge loop timing
        '''
        if millis1 != 0: 
            millis2 = millis1
            millis1 = int(round(time.time() * 1000))
        else:
            millis1 = int(round(time.time() * 1000))
        millis = millis1-millis2
        print "MiliSeconds per processing frame: ", millis

        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        #frame = imutils.resize(frame, width=min(640, frame.shape[1]))
        '''

        ###############
        # Blur - HSV - Mask - erode - dilate
        ###############
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)

        # Convert image to HSV
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        ##########
        # Loop on each color
        ##########
        for mmColor in mm:

            # Set up the min and max HSV settings 
            mask=cv2.inRange(hsvframe, mmColor.getHSV_min(), mmColor.getHSV_max())  # Red Mask
            # Get rid of noise
            mask = cv2.erode(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=3)
    
            # Only return the contours parameter and ignore hierarchy parm, hence [-2]    
            # CHAIN_APPROX_SIMPLE to return less contour points (faster/less memory)
            contours0 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        
            # Find the largest contour in the mask image, then use
            # it to compute the radius used for circle()
            # Design note: Radius could be hard coded and this step skipped for performance 
            # reasons if needed.
            #radius = 13    # Hard code radius
            if len(contours0) != 0:
                c = max(contours0, key=cv2.contourArea)
                if c.all() == 0:
                    print "Warning Contours: ",contours0
                else:
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
            #else:
                #print "Warning: Contour Area empty sequence"

            #Iterate through the objects found
            mmColor.rstTrackNext()
            for cnt in contours0:
    
                # Find center of current object
            	M = cv2.moments(cnt)
            	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
                #print (radius)
            	# only proceed if the radius meets a minimum size
            	if radius > min_radius:
                    #print "DEBUG: radius meets minimum size"
    
                    #TODO: Add max size and logic to split into multiple centroids if too big.


            	    # draw a circle around the centroid of the detected object
                    # in the original RGB frame.  Not the HSV masked frame.
                    # parameters (image, center, radius, color, thickness)
            	    cv2.circle(frame, center, int(radius)+4, mmColor.getCircleColor(), 2) 
                    x, y = center

                    print "DEBUG: Color, Center(x,y) = ", mmColor.getColor(), center 
                    
                    mmColor.addTrackNext(x,y)    # Used to post process multiple mm objects in next steps
        
            # Save the mask for post processing display 
            #TODO: Remove following line???
            locals()["Mask"+mmColor.color]=mask    

            #import pdb; pdb.set_trace() # Begin debug

            ##########
            # Now scan all new mm objects to see if a new ones have dropped in or if pre-existing
            ##########
            mmColor.newObjectCheck()
    

        ##########
        # Display the images
        ##########
        # overlay the trigger line and count onto original image.
        frame = cv2.polylines(frame, [trigger_line], False, trigger_line_color,thickness=4)
    
        for mmColor in mm:
            # Create the Mask images
            temp_mask=(locals()["Mask"+mmColor.color])
            cv2.namedWindow(mmColor.color+' Masked image',cv2.WINDOW_NORMAL)
            cv2.resizeWindow(mmColor.color+' Masked image',320,320)
            cv2.imshow(mmColor.color+' Masked image',temp_mask)

            str_down=mmColor.getColor() + ': '+ str(mmColor.getCount())    
            cv2.putText(frame, str_down, mmColor.getTextLocation(), font, .5, mmColor.getCircleColor(), 2,cv2.LINE_AA) 

        cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame',320,320)
        cv2.imshow('Frame',frame)
    
        
        ##########
        #Abort and exit with 'Q' or ESC
        ##########
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    
    cap.release() #release video file
    cv2.destroyAllWindows() #close all openCV windows

except RuntimeError, e:
            print "runtime error()"

