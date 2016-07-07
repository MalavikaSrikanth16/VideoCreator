# VideoCreator

Given an occassion (such as a birthday) with related text, images, audio and video clips, this Python3 program outputs a short video for the specified occassion.

###Installation

VideoCreator depends on the opencv module. To install in ubuntu you can run the script install-opencv.sh

For the other modules: pip3 install -r requirements.txt

###Usage 

python3 create_video.py -oc occassionname -o outputfilename textorimagepath/1 textorimagepath/2 ... -m audiofilepath -v videoclippath/1
videoclippath/2 ... 


