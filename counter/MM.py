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
    tracks = []
    def __init__(self, color_id, color, hsv_min=[], hsv_max=[]):
        self.uid = color_id    #Unique ID
        self.color = color
        self.hsv_min=hsv_min
        self.hsv_max=hsv_max

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

    def getColor(self):
        return(self.color)

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.x = xn
        self.y = yn
        self.tracks.append([self.x,self.y])

    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done

        
    # Check to see it the trigger line is being crossed
    def cross_trigger_line(self, trigger_line):
        if self.tracks[0][1] < trigger_line < self.tracks[-1][1]: 
            if self.line_crossed==False:
                self.line_crossed=True   # Only return True once
                return True 
            else:
                return False 

    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
    
class MultiPerson:
    def __init__(self, persons, xi, yi):
        self.persons = persons
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        
