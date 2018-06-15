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

from random import randint
import time


class M_and_M:
    # Keeps track of individual mm's that are in the view as MM_Objects.
    trackPrevious = []    
    trackNext = []   

    objectID = 0
    max_distance = 300   # Max pixels to assure it's not the same mm object since last pass.
    min_valid_yCoordinate = 200

    class MM_Object:
        age=0
        triggered = False      # Record if this object instance has been counted yet.

        def __init__(self, xi, yi):
            print "Debug: MM_object init x,y= ", xi,yi
            self.x = xi
            self.y = yi

        def setTrigger(self):
            self.triggered = True

        def getTriggerState(self):
            print "Debug: Enter getTriggerState triggered =", self.triggered
            return self.triggered 

        def getX(self):
            return self.x
        def getY(self):
            return self.y

        def updateNewCoords(self, xn, yn):
            print "Debug: Enter updateNewCoords xn, yn, x, y =", xn, yn, self.x, self.y
            self.age += 1
            print "Debug: age =", self.age
            self.x = xn
            self.y = yn

        def getAge(self):
            return self.age

    def __init__(self, color_id, color, circle_color=[], hsv_min=[], hsv_max=[],text_location=[]):
        self.uid = color_id    #Unique ID
        self.color = color     #Text Color field for printing
        self.circle_color=circle_color    #The color of the circle in found Frame objects 
        self.hsv_min=hsv_min
        self.hsv_max=hsv_max
        self.text_location=text_location

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
        self.trackNext.append(M_and_M.MM_Object(xn,yn))
        
    def newObjectCheck(self):
        print "Debug: Enter newObjectCheck"

        # Clean up self.trackPrevious before checking for advanced existing object
        for i in self.trackPrevious:
            print "Debug: newObjectCheck.trackPrevious"
            x=i.getX()
            y=i.getY()
            #Assume that object has rolled out of screen if below min_valid_yCoordinate
            if y > self.min_valid_yCoordinate or i.getTriggerState() == True:
                self.trackPrevious.remove(i)

        if not self.trackPrevious:
            print "Debug: newObjectCheck. No old mm's, add all as new"
            # Add all objects in TrackNext as new mm objects
            for t in self.trackNext:
                self.addNewObject(t.getX(),t.getY())
        else:
            ##########
            # Now ready to run algorithm to check whether object is a new one or previous one that moved.
            ##########
            # First sort the two object arrays ascending by y to make the following steps easier
            self.trackNext.sort(key = lambda a: a.y)
            self.trackPrevious.sort(key = lambda a: a.y)

            for tPrev in self.trackPrevious:
                print "Debug: newObjectCheck tPrev x, y =", tPrev.getX(), tPrev.getY() 
                yp=tPrev.getY()

                for tNext in self.trackNext:
                    yn = tNext.getY()

                    # If not within max_distance pixels then assume new mm.
                    if yn-yp > self.max_distance: 
                        # See if below trigger count line
                        if tNext.getY() > self.min_valid_yCoordinate:
                            if tNext.getTriggerState() == False:
                                self.incrementCount()
                                tNext.setTrigger()
                        self.addNewObject(tNext.getX(),tNext.getY())
                    else:  # Same mm new location
                        tPrev = tNext
                        if tPrev.getY() > self.min_valid_yCoordinate and tPrev.getTriggerState() == False:
                            self.incrementCount()
                            tPrev.setTrigger()
                        
                    
    def addNewObject(self, xn, yn):
        print "Debug: Add new MM Object"
        self.trackPrevious.append(M_and_M.MM_Object(xn,yn))

    def appendNewCoords(self, mmObject,xn, yn):
        return

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

        
    # Check to see it the trigger line is being crossed
    def triggerCheck(self, x, y, y_trigger):
        print "Debug: Enter triggerCheck x,y= ", x, y
        for i in self.track:
            if i.getTriggerState()==False: 
                 print "Debug: triggerCheck i.getY(), y_trigger, y =", i.getY(), y_trigger, y
                 if i.getY() < y_trigger and y_trigger < y:
                     print "Debug: triggerCheck **** call setTrigger() ****"
                     i.setTrigger()
                     return True
        return False

