#!/usr/local/bin/python3

from utils import VideoCreator
from setproctitle import setproctitle
import sys
from subprocess import call
from exceptions import FileNotFound

def console_main():
    setproctitle('Video-Creator')
    #sys.stdout = open('out.log','w')
    #sys.stderr = open('err.log','w')

    #call(['.','-o','images','-oc','-v','-m','--reverse-order'], stdout = f, stderr = f1)
    video = VideoCreator()
    video.get_arguments()

    if video.images == [] and video.videos is None:
        print("Input images, text or video")
        sys.exit()

    try:
        video.get_wtht()
    except FileNotFound as err:
        if err.status_code == 1:
            print("Invalid image path")
        elif err.status_code == 2:
            print("invalid video path")
        sys.exit()

    video.create_video()
    return

def main():
    """ Called when the command is executed
        Calls the function that starts the script
        handles KeyboardInterrupt
    """
    try:
        console_main()
    except KeyboardInterrupt:
        print ("Program stopped by user.")

if __name__ == '__main__': 
    main()
