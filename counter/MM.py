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
    track = []
    trigger_cnt = 0
    objectID = 0
    max_distance = 100   # Max pixels to assure it's the same mm object since last pass.

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

    ##########
    # Functions to discover, track, and manage found mm's.
    ##########
    def newObjectCheck(self, xn, yn):
        print "Debug: Enter newObjectCheck. x,y= ", xn, yn
        for i in self.track:
            print "Debug: newObjectCheck yn, i.getY() =", yn, i.getY()
            # If not triggered and not within max_distance pixels then assume new mm.
            if i.getTriggerState() == False and abs(yn-i.getY()) > self.max_distance:
                return True    
            else:    # Update existing mm object
                i.updateNewCoords(xn,yn) 
                return False
        return True
                    
    def addNewObject(self, xn, yn):
        print "Debug: Add new MM Object"
        self.track.append(M_and_M.MM_Object(xn,yn))

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

