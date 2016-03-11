#!/usr/local/bin/python3

from utils import VideoCreator
from setproctitle import setproctitle

def console_main():
    setproctitle('Video-Creator')
    video = VideoCreator()
    video.get_arguments()
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
