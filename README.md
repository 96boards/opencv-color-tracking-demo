# OpenCV Color Tracking Demo 
This demo is based and tested on the DragonBoard 820c, but should be able to work on varying platforms.  In summary, it counts  objects by color passing in the same direction through the camera field of view.  It can count multiple objects simultaneously.  The OpenCV functionality leveraged by this demo includes the following:
  * Object segmentation using color
  * Valid object identification by size  
  * Frame stitching to track and count multiple simultaneous moving objects by color
  * Provides hooks to monitor performance when algorithm changes to OpenCV library calls are made for identification tuning
  * Provides hooks to export results to the cloud

### Setup
This demo uses Debian builds of the Dragonboard 820c from Linaro. These can currently be found [here](http://snapshots.linaro.org/96boards/dragonboard820c/linaro/debian/ "820c Snapshots"). Build 182 was used for initial development and testing. 
A follow-on install using Debian Build 222 for The Boot Image and Root File System and Bootloader Build 37 was performed to validate the installation exmaple instuctions below.

**Software Installation Example**
1. Install the base software following the instructions on 96boards.org for DB820c.
* It's recommended to use latest builds and to also install the latest bootloader.
* **Important:** Don't forget to install the proprietary firmware found in *linux-board-support-package-r01700.zip*!  The demo won't work without it.  This zip contains a sub-folder called *proprietary-linux*.  Once you have attained this file, copy all the files from this sub-folder into the */lib/firmware* directory of the DB820c that you have just installed your Debian build on.

**Warning** This example requires building OpenCV from source.  This build on the DB820c (herein called the Target) requires a lot of board resources.  It's recommended to ssh into the Target and to have no applications, browsers or windows of any kind open during this installation process.  Build failures were experienced when Chromium was open, and these went away when did from a remote terminal.

**Note:** All commands in this section are executed on the Target from a ssh terminal window on the development host using `ssh linaro@<IP address of the Target>`.

2. Prep for sofware installation
  ```
  sudo apt-get -y update
  sudo apt-get -y upgrade
  systemctl daemon-reload
  ```
3. Install base packages
  ```
  sudo apt-get install -y build-essential cmake pkg-config
  sudo apt-get install -y libjpeg62-turbo-dev libtiff5-dev libpng-dev
  ```
4. Install Jasper - since there is no installation package, must build from source
  ```
  cd ~
  mkdir jasper
  cd jasper
  wget http://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.10.tar.gz
  tar -vzxf jasper-2.0.10.tar.gz
  cd jasper-2.0.10
  mkdir BUILD
  cd BUILD
  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release -DCMAKE_SKIP_INSTALL_RPATH=YES -DCMAKE_INSTALL_DOCDIR=/usr/share/doc/jasper-2.0.10 ..
  makesudo make install
  cd ~
  ```
5. Continue installing additional packages
  ```
  sudo apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev
  sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
  sudo apt-get install -y libxvidcore-dev libx264-dev
  
  sudo apt-get install -y libgtk-3-dev
  sudo apt-get install -y libatlas-base-dev gfortran
  
  sudo apt-get install -y python2.7-dev
  sudo apt-get install -y python3-dev
  
  sudo apt-get install -y python-pip
  pip install numpy
  pip install imutils
  ```
  
6. Download, build and install OpenCV version 3.2.0 (update commands/directory names below if a different version is used)
  ```
  cd ~
  wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip
  unzip opencv.zip
  wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.2.0.zip
  unzip opencv_contrib.zip
  
  cd opencv3.2.0
  mkdir build
  cd build
  cmake -D CMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.2.0/modules ..
  ```
  **Hack Note:** To get the OpenCV to build, I had to resolve a ffmpeg version incompatibility.  Instead of changing versions, run the following script from the command line to make the build work:
  ```
  sed -i '1s/^/#define AV_CODEC_FLAG_GLOBAL_HEADER (1 << 22)\n#define CODEC_FLAG_GLOBAL_HEADER AV_CODEC_FLAG_GLOBAL_HEADER\n#define AVFMT_RAWPICTURE 0x0020\n/' ~/opencv-3.2.0/modules/videoio/src/cap_ffmpeg_impl.hpp
  ```
  Now ready to build:
  ```
  make -j2
  sudo make install
  sudo ldconfig
  ```
7. The Python 2.7 bindings for OpenCV 3 should now be located in /usr/local/lib/python-2.7/site-packages/ . You can verify this using the ls command and having a similar output to the following:
  ```
  ls -l /usr/local/lib/python2.7/dist-packages/
  total 2928
  -rw-r--r-- 1 root staff 2994784 Aug  2 03:20 cv2.so
  ```
8. Verify that OpenCV 3.2 installed as expected
  ```
  linaro@linaro-alip:~/opencv-3.2.0/build$ python
  Python 2.7.15 (default, Jul 28 2018, 11:29:29)
  [GCC 8.1.0] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import cv2
  >>> cv2.__version__
      '3.2.0'
  >>> quit()
  ```
  
Installation is complete and you should be ready to run the demo now!
  
Useful installation references:
 * [Ubuntu 16.04: How to install OpenCV](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
 * [OpenCV build instructions](https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html)
 * [Installing OpenCV on Debian Linux](https://indranilsinharoy.com/2012/11/01/installing-opencv-on-linux/)
 * [96Boards Forum entry](https://discuss.96boards.org/t/opencv-3-2-install-dependencies-error/2139/2)
  
**Required Hardware:**

Camera:  I have initially used a USB camera but plan to transition to a camera mezzanine connected to the DB820c

Lighting: It is important to create a setup where lighting is controlled and repeatable.  This is so that when you determine your HSV settings, they are repeatable.  

Example of physical setup components is shown below.  It can be seen that a PVC pipe was cut to allow a camera to see the objects as they flow by.  It was set up on a 10 degree incline.

<img src=photos/DemoSetup.jpg width=40% height=50% />
<img src=photos/SetupSideView.gif width=40% height=50% />
<img src=photos/SetupTopViewV2.gif width=50% height=50%/>

A small light turned out to be important to control the lighting.  Initial prototype was just a shoebox spray painted white on the inside. A hole was cut in top for light and camera placement. 

# Demo usage flow
There are a few steps to perform in order to get the demo set up for your physical environmnet.  

## Determine HSV Settings
First, you must discover the HSV min and max values for your test environment.  This is sensative to lighting and the objects being identified by color. To do this, build out your environment with controlled lighting.  Then run colorIsolationApp.py from this repo on the DB820c.  
`$python colorisolationapp.py`

An example of this tool is shown below: 
![alt text](photos/colorisolationapp.png "HSV Tuning App")

The field of view should contain your targeted environment along with all of the colors you wish to isolate from each other.  With the sliders in the colorIsolationApp.py, move them until only the color of interest can be seen and all other colors are blocked (black).  Press "Show" and the HSV min and max values will be printed to the terminal window.  Save these values for the next step.

Once the above is done for all colors, edit the `track_mm.py` file and update the HSV values in the initialization section for each color to match the values from the above step.  Save the file and you should be ready to go.

## Run the Demo

Finally, run the track_mm.py file and watch the counters increment as the associated colors roll through the screen.
`python track_mm.py 2> /dev/null`

The default configuration will display all six color masks as well as the frame image.  These look like the following:
![alt text](photos/Frame.png "Frame image")
![alt text](photos/BlueMask.png "Blue Mask")

# Debugging and tuning
 * If you start the app and it quietly closes, make sure your camera is connected
 * To see how long is required to process one frame, uncomment the following code in track_mm.py
 ```
        #Debug code to gauge loop timing
        if millis1 != 0: 
            millis2 = millis1
            millis1 = int(round(time.time() * 1000))
        else:
            millis1 = int(round(time.time() * 1000))
        millis = millis1-millis2
        print "MiliSeconds per processing frame: ", millis
 ```
## Customizing the tracking algorithm
There are surely many creative algorithms to track and count the objects as they move the field of view.  The primary routine that does this in the `def newObjectCheck(self):` method in the `MM.py` file.  Since the objects can move at variable speeds, stitching the objects across frames will have corner cases where it is challenging to determine if the object is new or a previously existing object that has moved. If you come up with one, please let me know!  I would love to see other creative ways to solve this while increasing accuracy.

## Customizing the OpenCV filters
In the initial implementation, I have primarily used the following code in `track_mm.py` to clean up the colored objects moving through the frame:
```
            # Set up the min and max HSV settings 
            mask=cv2.inRange(hsvframe, mmColor.getHSV_min(), mmColor.getHSV_max())  # Red Mask
            # Get rid of noise
            mask = cv2.erode(mask, kernel7, iterations=1)
            mask = cv2.dilate(mask, kernel7, iterations=3)
    
            # Only return the contours parameter and ignore hierarchy parm, hence [-2]    
            # CHAIN_APPROX_SIMPLE to return less contour points (faster/less memory)
            contours0 = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
```
Various kernel sizes and erode/dialate functions from OpenCV are encouraged to be experimented with, with the goal of decreasing the time taken to process each frame.  Current implementation is around 65-70mS per frame.  The faster each frame is processed, the tracking algorithm can then be tightened up for more accurate tracking.  I would also be interested in seeing and testing creative solutions that can decrease this loop time.  A faster and more expensive camera could a quick way to increase accuracy.  I started out with a simple off-the-shelf USB camera that's only 30 fps.  Another option is to redesign and create a multi-threading solution that captures frames in parallel to the frame processing.

# Other notes

Additional tuning is likely required tied to the test environment and how fast color objects are flowing through the field of view.  These include the following:


