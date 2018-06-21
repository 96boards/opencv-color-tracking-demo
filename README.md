# OpenCV Color Tracking Demo 
This demo is based and tested on the DragonBoard 820c, but should be able to work on varying platforms.  In summary, it counts  objects by color passing in the same direction through the camera field of view.

### Setup
This demo uses Debian builds of the Dragonboard 820c from Linaro. These can currently be found [here](http://snapshots.linaro.org/96boards/dragonboard820c/linaro/debian/ "820c Snapshots"). Build 182 was used for initial development and testing.

Installation of python, OpenCV and PIP install of several python libraries are also required.  There are plenty of sites that describe how to set this up.
 * Instructions for installing OpenCV found here
 

Camera:  I have initially used a USB camera but plan to transition to a camera mezzanine connected to the DB820c
Lighting: It is important to create a setup where lighting is controlled and repeatable.  This is so that when you determine your HSV settings, they are repeatable.  

# Demo usage flow
There are a few steps to perform in order to get the demo set up for your physical environmnet.  

## Determine HSV Settings
First, you must discover the HSV min and max values for your test environment.  This is sensative to lighting and the objects being identified by color. To do this, build out your environment with controlled lighting.  Then run colorIsolationApp.py from this repo on the DB820c.  
`$python colorisolationapp.py`

An example of this tool is shown below: 
![alt text](photos/colorisolationapp.png "HSV Tuning App")

The field of view should contain your targeted environment along with all of the colors you wish to isolate from each other.  With the sliders in the colorIsolationApp.py, move them until only the color of interest can be seen and all other colors are blocked (black).  Press "Show" and the HSV min and max values will be printed to the terminal window.  

Once the above is done for all colors, edit the track_mm.py file and update the HSV values in the initialization section to match the values from step 1.  Save the file and you should be ready to go.

Finally, run the track_mm.py file and watch the counters increment as the associated colors roll through the screen.

## Other notes

Additional tuning is likely required tied to the test environment and how fast color objects are flowing through the field of view.  These include the following:


