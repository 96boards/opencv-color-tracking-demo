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
import datetime


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
color_id = 0          # One for each color
min_radius = 5        # Adjust to size of m & m. Impacted by distance from camera

#DEBUG import pdb; pdb.set_trace() # Begin debug

# Create color objects
red_hue_min = 0
red_saturation_min = 81 
red_value_min = 63 
red_hsv_min=np.array([red_hue_min,red_saturation_min,red_value_min])

red_hue_max = 12
red_saturation_max = 256 
red_value_max = 148
red_hsv_max=np.array([red_hue_max,red_saturation_max,red_value_max])

mm.append(MM.M_and_M(color_id, "Red",red_hsv_min,red_hsv_max))  # Create Red Tracking Object


#TODO: Increment color_id for each new color


# Create video camera object and start streaming to it.
cap = cv2.VideoCapture(0) # 0 == Continuous stream


# set up visual imaging for the trigger line that is the count line when crossed
cnt_down=0
trigger_line_color=(255,0,0)
trigger_line= np.array([[0, 160],[320, 160]])

counter=0

try:
    while(cap.isOpened()):
        # Capture a still image from the video stream
        ret, frame = cap.read() #read a frame
    
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        #frame = imutils.resize(frame, width=min(640, frame.shape[1]))
        
        ###############
        # Blur - HSV - Mask - erode - dilate
        ###############
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)

        # Convert image to HSV
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # Set up the min and max HSV settings 
        mask=cv2.inRange(hsvframe, mm[0].getHSV_min(), mm[0].getHSV_max())  # Red Mask
        # Get rid of noise
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=3)

        # Only return the contours parameter and ignore hierarchy, hence [-2]    
        # CHAIN_APPROX_SIMPLE to return less contour points
        contours0 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    

       	# Find the largest contour in the mask image, then use
        # it to compute the radius used for circle()
        c = max(contours0, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        #Iterate through the objects found
        for cnt in contours0:

                # Find center of current object
        	M = cv2.moments(cnt)
        	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
                #print (radius)
        	# only proceed if the radius meets a minimum size
        	if radius > min_radius:
                    #print "DEBUG: radius meets minimum size"

        	    # draw a circle around the centroid of the detected object
                    # in the original RGB frame.  Not the HSV masked frame.
                    # parameters (image, center, radius, color, thickness)
        	    cv2.circle(frame, center, int(radius)+4, (0, 0, 255), 2)  #TODO: Make multiple colors

                    # Update list of tracked points for this object
                    mm[0].updateCoords(x, y)     #TODO: Figure out how to do for multiple objects

                #TODO: Compare first and last coordinate to see if crossed trigger line
                #TODO: If crossed, increment counter & mark object as "counted"
    
        """    
        _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)        
        for cnt in contours0:
            cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
            area = cv2.contourArea(cnt)
    
                #################
                # Assure object is still in the frame and isn't erased
                #################     
            for i in m_and_ms:   
                i.updateDisappear(i.getDisappear()+1) 
                if i.getDisappear() > 25:
                    m_and_ms.remove(i)
            
            if area > areaTH:
                #################
                #   Object Tracking
                #################            
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x,y,w,h = cv2.boundingRect(cnt)
    
                print('x{} y{} w{} h{}'.format( x, y, w, h))
    
                
                new = True                 
                for i in m_and_ms:
                    if abs(x-i.getX()) <= w_margin and abs(y-i.getY()) <= h_margin:
                        new = False
                        i.updateCoords(cx,cy)  
                        i.updateDisappear(0) # Clear
                        break
                if new == True:
                    m = MM.M_and_M(color_id,cx,cy, max_p_age)
                    m_and_ms.append(m)
                    color_id += 1    
     
                cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
                img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
                cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
                cv2.imshow('img',img)
    
        #########################
        # Determine path/location of each m&m
        #########################
        for i in m_and_ms:
            if len(i.getTracks()) >= 2:
                pts = np.array(i.getTracks(), np.int32)
                pts = pts.reshape((-1,1,2))
                frame = cv2.polylines(frame,[pts],False,i.getRGB())
                if i.cross_trigger_line(trigger_line) = True:
                    cnt_down+=1
                    print('Timestamp: {:%H:%M:%S} DOWN {}'.format(datetime.datetime.now(), cnt_down))
    
            cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.7,i.getRGB(),1,cv2.LINE_AA)
        """

        #########################
        # overlay the trigger line and count onto image.
        #########################
        str_down='DOWN: '+ str(cnt_down)    #TODO: Change from 'DOWN' to 'Color', like "Red" from class M_and_M class object
        frame = cv2.polylines( frame, [trigger_line], False, trigger_line_color,thickness=4)
        cv2.putText(frame, str_down, (10,50), font, .5, (0,0,255), 2,cv2.LINE_AA) 
    
        # Display the images
        cv2.imshow('Masked image',mask)
        cv2.imshow('Frame',frame)
    
        
        #Abort and exit with 'Q' or ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    
    cap.release() #release video file
    cv2.destroyAllWindows() #close all openCV windows

except RuntimeError, e:
            print "runtime error()"

