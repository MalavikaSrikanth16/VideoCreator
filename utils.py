#!/usr/local/bin/python3

import cv2
import argparse
import os
import sys

class VideoCreator(object):
	def __init__(self):
		self.images = []
		self.occasion = None
		self.storage_path = "output.avi"	
		self.same_order = False
		self.reverse_order = False

	def get_arguments(self):
		parser = argparse.ArgumentParser(description='Creates a short video.')
		parser.add_argument('images', nargs='*', help="Path of images")
		parser.add_argument('-o', '--output', required=False, default='output.avi', help="Output video file")
		parser.add_argument('-oc', '--occasion', required=True, help="Occassion like Birthday, Anniversary, etc.")
		parser.add_argument('--same-order', default = False, action="store_true", help="Images to be displayed in the same order")
		parser.add_argument('--reverse-order', default=False, action="store_true", help="Images to be displayed in reverse order")
		args = vars(parser.parse_args())
		self.images = args['images']
		self.occasion = args['occasion']
		self.storage_path = args['output']
		self.same_order = args['same_order']
		self.reverse_order = args['reverse_order']

	def create_video(self):
		dir_path = '.'
		# Determine the width and height from the first image
		if self.images == []:
			print("Input image paths to create video")
			sys.exit()
		image_path = self.images[0]
		frame = cv2.imread(image_path)
		cv2.imshow('frame',frame)
		height, width, channels = frame.shape

		fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
		out = cv2.VideoWriter(self.storage_path, fourcc, 1.0, (width, height),True)
		for image in self.images:
			image_path = image
			frame = cv2.imread(image_path)
			rframe = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
			out.write(rframe) 
			cv2.imshow('frame',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'): 
				break
		out.release()
		cv2.destroyAllWindows()
		print("The output video is {}".format(self.storage_path))
