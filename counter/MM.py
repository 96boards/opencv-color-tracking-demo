"""
Summary: This file contains the classes allocated for each color and each object per color.  One M_and_M object is created per color that is to be tracked. 


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

from random import randint
import time

##########
# Class: For each color
##########
class M_and_M:

    objectID = 0

    # Tuning parameters:
    # The fact that objects can move at different speeds are what will keep this from being 100% accurate.
    # So tune as close as possible for your solution. Notes to increase precision:
    #   1) the faster the video capture/OpenCV processing loop in track.py, the more accurate the results.
    #   2) a faster camera.  Used 30 fps one here.  
    #   3) the more predictable the speeds of the objects, the better. Turns out Peanut M&Ms have quite a 
    #      variant in shapes that impact consitant velocity/acceleration.
    max_distance = 300   # Max pixels to assure it's not the same mm object since last pass.
    min_distance = 40    # Min
    min_valid_yCoordinate = 30     # if below 100, assume will survive next pass
    max_valid_yCoordinate = 300    # if abov 300, assume it's gone

    ##########
    # Class:  For each MM
    ##########
    class MM_Object:

        def __init__(self, xi, yi, trigger):
            #print "Debug: MM_object init x,y= ", xi,yi
            self.x = xi
            self.y = yi
            self.triggered=trigger    # Record if this object instance has been counted yet.
            self.age=0

        def setTrigger(self):
            self.triggered = True
        def getTriggerState(self):
            #print "Debug: Enter getTriggerState triggered =", self.triggered
            return self.triggered 
        def setTriggerState(self, trig):
            self.triggered=trig

        def getX(self):
            return self.x
        def setX(self, xi):
            self.x=xi

        def getY(self):
            return self.y
        def setY(self, yi):
            self.y=yi

        def updateNewCoords(self, xn, yn):
            #print "Debug: Enter updateNewCoords xn, yn, x, y =", xn, yn, self.x, self.y
            self.incrementAge()
            self.x = xn
            self.y = yn

        def getAge(self):
            return self.age
        def setAge(self, a):
            self.age = a
        def incrementAge(self):
            #print "Debug: age =", self.age
            self.age += 1

    def __init__(self, color_id, color, age_t, circle_color=[], hsv_min=[], hsv_max=[],text_location=[]):
        # Keeps track of individual mm's that are in the view as MM_Objects.
        self.trackPrevious = []    
        self.trackNext = []   

        self.uid = color_id    #Unique ID
        self.color = color     #Text Color field for printing
        self.circle_color=circle_color    #The color of the circle in found Frame objects 
        self.hsv_min=hsv_min
        self.hsv_max=hsv_max
        self.text_location=text_location
        self.age_threshold=age_t

        #Initializat Local Class variables
        self.count=0		#Initialize color count
        self.x=None
        self.y=None

        self.age=0
         
        self.trigger_line_crossed=False
        self.disappear=None

    def getHSV_min(self):
        return(self.hsv_min)

    def getHSV_max(self):
        return(self.hsv_max)

    def getColorID(self):

        return(self.uid)

    def getColor(self):
        return(self.color)

    def getCircleColor(self):
        return(self.circle_color)

    def getTextLocation(self):
        return(self.text_location)

    def incrementCount(self):
        self.count +=1

    def getCount(self):
        return(self.count)

    ##########
    # Functions to discover, track, and manage found mm's.
    ##########
    def rstTrackNext(self):
        self.trackNext = []   

    def addTrackNext(self, xn, yn):
        self.trackNext.append(M_and_M.MM_Object(xn,yn, False))
        
    def newObjectCheck(self):
        #print "Debug: Enter newObjectCheck"

        # Clean up self.trackPrevious before checking for advanced existing object
        for i in self.trackPrevious:
            x=i.getX()
            y=i.getY()
            age=i.getAge()
            print "Debug: newObjectCheck.trackPrevious y age ", y, age

            # Assume that object has rolled out of screen very quickly and never got logged 
            if age > self.age_threshold:
                if i.getTriggerState() == False:
                    print "Debug: Aged out INCREMENT COUNT"
                    self.incrementCount()
                self.trackPrevious.remove(i)
            else:
                i.incrementAge()


        if not self.trackPrevious:
            #print "Debug: newObjectCheck. No old mm's, add all as new"
            # Add all objects in TrackNext as new mm objects
            for t in self.trackNext:
                print "Debug: newObjectCheck. Process new object y = ", t.getY()
                if t.getY() > self.min_valid_yCoordinate and t.getTriggerState() == False:
                    print "Debug: INCREMENT COUNT"
                    self.incrementCount()
                    t.setTrigger()
                self.addNewObject(t.getX(),t.getY(),t.getTriggerState())
        else:
            ##########
            # Now ready to run algorithm to check whether object is a new one or previous one that moved.
            ##########
            # First sort the two object arrays ascending by y to make the following steps easier
            self.trackNext.sort(key = lambda a: a.y)
            self.trackPrevious.sort(key = lambda a: a.y)

            for tPrev in self.trackPrevious:
                yp=tPrev.getY()
                xp=tPrev.getX()
                print "Debug: newObjectCheck tPrev x, y =", xp, yp

                for tNext in self.trackNext:
                    print "Debug: newObjectCheck tPrev y, tNext y =", yp, tNext.getY() 
                    yn = tNext.getY()

                    # If not within valid band, assume new mm.
                    if yn > yp and (abs(yn-yp) > self.max_distance or abs(yn-yp) < self.min_distance): 
                        # See if below trigger count line
                        print "Debug: newObjectCheck valid range exceeded - new"
                        if tNext.getY() > self.min_valid_yCoordinate:
                            if tNext.getTriggerState() == False:
                                print "Debug: newObjectCheck INCREMENT COUNT max"
                                self.incrementCount()
                                tNext.setTrigger()

                        self.addNewObject(tNext.getX(),tNext.getY,tNext.getTriggerState())
                        self.trackNext.remove(tNext)
                    else:  # Same mm new location
                        print "Debug: newObjectCheck new location"

                        if yn > yp:
                            # import pdb; pdb.set_trace()
                            tPrev.setX(tNext.getX())
                            tPrev.setY(tNext.getY())
                            if tPrev.getTriggerState() == False:
                                tPrev.setTriggerState(tNext.getTriggerState())
                            tPrev.setAge(0)
        
                            self.trackNext.remove(tNext)

                            if tPrev.getY() > self.min_valid_yCoordinate and tPrev.getTriggerState() == False:
                                print "Debug: newObjectCheck INCREMENT COUNT moved"
                                self.incrementCount()
                                tPrev.setTrigger()
                        break    # Consumed the tPrev object here so go grab a new one

            # Check for remaining new objects seen, process each one, and move to trackPrevious[]
            for tNext in self.trackNext:
                print "Debug: newObjectCheck - add remaining new objects from tNext to tPrev"
                yp=tNext.getY()
                xp=tNext.getX()
                if yp > self.min_valid_yCoordinate:
                    print "Debug: newObjectCheck cleanup INCREMENT COUNT"
                    self.incrementCount()
                    temp_trig=True
                else:
                    temp_trig=False

                self.addNewObject(xp, yp, temp_trig)

    def addNewObject(self, xn, yn, trigger_state):
        print "Debug: Add new MM Object"
        self.trackPrevious.append(M_and_M.MM_Object(xn,yn,trigger_state))

    def appendNewCoords(self, mmObject,xn, yn):
        return

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

        
    # Check to see it the trigger line is being crossed
    def triggerCheck(self, x, y, y_trigger):
        #print "Debug: Enter triggerCheck x,y= ", x, y
        for i in self.track:
            if i.getTriggerState()==False: 
                 #print "Debug: triggerCheck i.getY(), y_trigger, y =", i.getY(), y_trigger, y
                 if i.getY() < y_trigger and y_trigger < y:
                     #print "Debug: triggerCheck **** call setTrigger() ****"
                     i.setTrigger()
                     return True
        return False

