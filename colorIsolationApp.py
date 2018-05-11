"""
This python tool is a manual analysis phase tool that aids in determining the proper HSV settings by color. Manually adjust the sliders until the video only shows the colored object in white with the remainder of the screen black.  Then press show for the HSV min / max settings to be printed to the terminal.  This is effectively providing trained data into an OpenCV application that is being used for color isolation or differentiation.


Copyright 2018 Don Harbin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import numpy as np
import cv2
import os
import threading
import time
import sys

from Tkinter import *   # Library for slider widgets
import tkFileDialog
from PIL import Image
from PIL import ImageTk


def start_video():
    global videostarted, stopEvent, cap, thread

    # Create video camera object and start streaming to it.
    cap = cv2.VideoCapture(0) # 0 == Continuous

    # The video_image loop must use tkinter threading or the sliders
    # won't work, so this sets up threading before calling video_image()
    if videostarted == False:    
        videostarted = True
        stopEvent=threading.Event()
        thread=threading.Thread(target=video_image,args=())
        thread.start()
    else:
        print "Video already running"

def video_image():
    # grab a reference to the image panels
    global panelV1

    try:
        while not stopEvent.is_set():
            # Capture a still image from the video stream
            ret, frame = cap.read() # Read a new frame
            frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

	    '''
	    Keep for debug
	    '''
            # Canny test code, only called w/ imshow() below
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #edged = cv2.Canny(gray, 50, 100)
    
           # Convert image to HSV
            hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Set up the min and max HSV settings
            lower=np.array([barH.get(),barS.get(),barV.get()])
            upper=np.array([barH2.get(),barS2.get(),barV2.get()])
            mask=cv2.inRange(hsvframe, lower, upper)
            mask=Image.fromarray(mask)
            mask=ImageTk.PhotoImage(mask)

	    '''
	    Keep for debug
	    '''
            #cv2.imshow("Original",frame)
            #cv2.imshow("Edged",edged)
            #cv2.imshow("HSV",hsvframe)
            #cv2.imshow("Mask", mask)

            # convert the images to PIL format...
            #pilframe=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            #pilframe=Image.fromarray(pilframe)
            #pilframe=ImageTk.PhotoImage(pilframe)

	
            #If the panels are None, initialize them
            if panelV1 is None:
                print "enter panelV1 None"
                # the first panel will store our original image
                panelV1 = Label(master,image=mask)
                panelV1.image = mask
                #panelV1.pack(side="right", padx=10,pady=10)
                panelV1.pack()

            # otherwise, update the image panels
            else:
                # update the panels
                #print "enter panelV1 update"
                panelV1.configure(image=mask)
                panelV1.image = mask
                panelV1.pack()


                ch=cv2.waitKey(10)   # 1 == capture every 10 millisec
                if ch & 0xFF == ord('q'):  # "q" to exit loop
                    break

        # Required to release the device and prevent having to reset system 
        cap.release()
        cv2.destroyAllWindows()

        print "exit video_image()"

    except RuntimeError, e:
        print "runtime error()"


def slider_init():
    global barH, barH2, barS, barS2, barV, barV2
    '''
    Set up sliders
    '''
    #H value 
    barH = Scale(master, from_=0, to=255, orient=HORIZONTAL, label="H min", length=600, tickinterval=128)
    barH.set(30)
    barH.pack()

    barH2 = Scale(master, from_=0, to=255, orient=HORIZONTAL, label="H max", length=600, tickinterval=128)
    barH2.set(250)
    barH2.pack()

    #S value 
    barS = Scale(master, from_=0, to=255, orient=HORIZONTAL,label="S min", length=600, tickinterval=128)
    barS.set(30)
    barS.pack()

    barS2 = Scale(master, from_=0, to=255, orient=HORIZONTAL,label="S max", length=600, tickinterval=128)
    barS2.set(250)
    barS2.pack()

    #V value 
    barV = Scale(master, from_=0, to=255, orient=HORIZONTAL,label="V min",  length=600, tickinterval=128)
    barV.set(30)
    barV.pack()

    barV2 = Scale(master, from_=0, to=255, orient=HORIZONTAL,label="V max",  length=600, tickinterval=128)
    barV2.set(250)
    barV2.pack()

def show_values():
    print ("Hval min: %d Hval/max: %d " %(barH.get(),barH2.get()))
    print ("Sval min: %d Sval/max: %d " %(barS.get(),barS2.get()))
    print ("Vval min: %d Vval/max: %d " %(barV.get(),barV2.get()))

def closeout():
    print("closing...")

    stopEvent.set()
    #video_image.stop()

    time.sleep(1)
    # Required to release the device and prevent having to reset system 
    print("cap.release...")
    cap.release()
    time.sleep(1)
    '''
    print("cv2.destroyAllWindows...")
    cv2.destroyAllWindows()

    print("stop thread...")
    thread.join()
    '''

    print("quit...")
    master.destroy()
    print("for good")
    os._exit(1)
#<><><<><><><><><><>
#<><><<><><><><><><>

master=Tk()

'''
Set up image box from Video Stream
'''
panelV1 = None
videostarted=False
stopEvent=None

# Initialize sliders for color tuning
slider_init()

# Create button that Prints current HSV value of slider to the command line.
Button(master, text='Show', command=show_values).pack()

 
#vbtn = Button(master, text="Start Video Stream", command=video_image)
#vbtn.pack(side="bottom", fill="both",expand="yes",padx="10", pady="10")
Button(master, text="Start Video Stream", command=start_video).pack(side="bottom", fill="both",expand="yes",padx="10", pady="10")

# set a callback to handle when the window is closed
master.wm_title("colorisolationappV1")
master.wm_protocol("WM_DELETE_WINDOW", closeout)

master.mainloop() #tk call to run application

