#!/usr/local/bin/python3

import cv2
import argparse
import os
import sys
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

class VideoCreator(object):
	def __init__(self):
		self.images = []
		self.occasion = None
		self.storage_path = "output.avi"
		self.reverse_order = False

	def get_arguments(self):
		parser = argparse.ArgumentParser(description='Creates a short video.')
		parser.add_argument('imageandtext', nargs='*', help="Path of images or text to display")
		parser.add_argument('-o', '--output', required=False, default='output.avi', help="Output video file")
		parser.add_argument('-oc', '--occasion', required=True, help="Occassion like Birthday, Anniversary, etc.")
		parser.add_argument('--reverse-order', default=False, action="store_true", help="Images to be displayed in reverse order")
		args = vars(parser.parse_args())
		self.images = list(args['imageandtext'])
		self.occasion = args['occasion']
		self.storage_path = args['output']
		self.reverse_order = args['reverse_order']

	def create_video(self):
		# Determine the width and height from the first image
		if self.images == []:
			print("Input image paths or text to create video")
			sys.exit()

		self.images.insert(0, "")

		for image in self.images:
			if os.path.exists(image):
				frame = cv2.imread(image)
				height, width, channels = frame.shape
				break

		font = ImageFont.truetype("orange_juice.ttf",75)
		img=Image.new("RGBA", (width,height),(0,0,0))
		draw = ImageDraw.Draw(img)
		draw.text((width/4, height/3),"Happy",fill=(255,255,255),font=font)
		draw.text((width/4 + 10, height/3+110),self.occasion,fill=(255,255,255),font=font)
		draw = ImageDraw.Draw(img)
		img.save("first.png")
		self.images[0] = "./first.png"

		for i,image in enumerate(self.images):
			if os.path.exists(image) == False:
				img=Image.new("RGBA", (width,height),(0,0,0))
				draw = ImageDraw.Draw(img)
				draw.text((10, 10),image,fill=(255,255,255),font=font)
				draw = ImageDraw.Draw(img)
				img.save("text" + str(i) + ".png")
				self.images[i] = "./text" + str(i) + ".png"

		fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
		out = cv2.VideoWriter(self.storage_path, fourcc, 1.0, (width, height),True)

		if self.reverse_order == True:
			self.images[1:] = list(reversed(self.images[1:]))

		for image in self.images:
			frame = cv2.imread(image)
			rframe = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
			out.write(rframe) 
			cv2.imshow('frame',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'): 
				break

		out.release()
		cv2.destroyAllWindows()
		print("The output video is {}".format(self.storage_path))
