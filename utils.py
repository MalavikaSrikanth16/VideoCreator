#!/usr/local/bin/python3

import cv2
import argparse
import os
import sys
import PIL
import random
import subprocess
import textwrap
import time
import shutil
from moviepy.editor import *
from exceptions import FileNotFound
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import re

class VideoCreator(object):

	def __init__(self):	
		self.images = None
		self.occasion = None
		self.storage_path = "output.avi"
		self.reverse_order = False
		self.music = None
		self.videos = None
		self.width = 0
		self.height = 0
		self.fps = 0

	def get_arguments(self):
		parser = argparse.ArgumentParser(description='Creates a short video.')
		parser.add_argument('imgtxt', nargs='*', help="Path of images or text to display (Text must be within double quotes)")
		parser.add_argument('-o', '--output', required=False, default='output', help="Output video file name")
		parser.add_argument('-oc', '--occasion', required=True, help="Occassion like Birthday, Anniversary, etc.")
		parser.add_argument('--reverse-order', default=False, action="store_true", help="Images and Videos to be displayed in reverse order")
		parser.add_argument('-m','--music', help="Path of audio clip to be played when images are displayed")
		parser.add_argument('-v','--video', nargs='*', help="Path of video clips")
		args = vars(parser.parse_args())
		self.images = args['imgtxt']
		self.occasion = args['occasion']
		self.storage_path = args['output']
		self.reverse_order = args['reverse_order']
		self.music = args['music']
		#Converts to a valid file name
		s = args['output']
		s = s.replace(' ', '_')
		s = re.sub(r'(?u)[^-\w]', '', s)
		self.storage_path = s + '.avi'
		self.videos = args['video']
		return (self.images, self.occasion, self.storage_path, self.reverse_order, self.music, self.videos, self.width, self.height, self.fps)


	def get_wtht(self):
		VIDEO_TYPES = ['.avi','.AVI','.wmv','.WMV','.mpg','.MPG','.mpeg','.MPEG','.mp4','.mov'] 
		IMAGE_TYPES = ['.png','.gif','.jpg','.jpeg','.rgb','.tiff','.bmp','.rast','.ppm','.pgm','.pbm','.xbm']
		AUDIO_TYPES = ['.mp3','.MP3','.mpa','.MPA','.flac','.FLAC','.ogg','.OGG','.wav','.WAV','.wma','.WMA']

		for image in self.images: 
			if os.path.splitext(image)[1] in IMAGE_TYPES:  #If it ends with .png,.jpeg,etc. check if valid path or not.
				if os.path.exists(image):
					continue
				else:
					raise FileNotFound(1)
			elif os.path.exists(image):              #If it doesn't end with .png,.jpeg,etc. but path exists raise error as it is not an expected image path or plain text               
				raise FileNotFound(1)

		self.height = 480
		self.width = 640

		tot = 0
		if self.videos != None:
			self.videos = list(self.videos)
			for video in self.videos:
				if os.path.exists(video) and os.path.splitext(video)[1] in VIDEO_TYPES:
					cap = cv2.VideoCapture(video)
					fps = cap.get(cv2.CAP_PROP_FPS)
					tot = tot + fps
					cap.release()
				else:
					raise FileNotFound(2)
			self.fps = tot / len(self.videos)  #fps of output video is taken to be average of fps of individual video inputs.
		else:
			self.fps = 10.0     #If no video inputs then fps of output video is taken as 10.

		if self.music != None:
			if os.path.exists(self.music) and os.path.splitext(self.music)[1] in AUDIO_TYPES:
				return
			else:
				raise FileNotFound(3)					

	def create_video(self):
		
		
		self.images.insert(0, "")

		width = self.width - 40
		height = self.height - 40
		x = 0

		if not os.path.exists('./Nonsense'):
			os.makedirs('./Nonsense')

		font = ImageFont.truetype("orange_juice.ttf",60)
		img=Image.new("RGBA", (width,height),(0,0,0))
		draw = ImageDraw.Draw(img)
		self.occasion = "Happy " + self.occasion
		self.occasion = textwrap.fill(self.occasion,10)
		w,h = draw.textsize(self.occasion,font=font)
		draw.text(((width-25-w)/2, (height-25-h)/2),self.occasion,fill=(255,255,255),font=font)
		draw = ImageDraw.Draw(img)
		img.save("./Nonsense/first.png")
		self.images[0] = "./Nonsense/first.png"

		for i,image in enumerate(self.images):
			if os.path.exists(image) == False:
				font = ImageFont.truetype(random.choice(["orange_juice.ttf","font3.ttf","font5.ttf"]),60)
				img=Image.new("RGBA", (width,height),(0,0,0))
				draw = ImageDraw.Draw(img)
				image = textwrap.fill(image,15)
				w,h = draw.textsize(image,font=font)
				draw.text(((width-10-w)/2, (height-10-h)/2),image,fill=(255,255,255),font=font)
				draw = ImageDraw.Draw(img)
				img.save("./Nonsense/text" + str(i) + ".png")
				self.images[i] = "./Nonsense/text" + str(i) + ".png"

		if len(self.images) > 1:
			if self.reverse_order == True:
				self.images[1:] = list(reversed(self.images[1:]))

		vid = []
		for image in self.images:
			frame = cv2.imread(image)
			rframe = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
			rframe = cv2.copyMakeBorder(rframe,20,20,20,20,cv2.BORDER_CONSTANT,value=[255,255,255])
			M = cv2.getRotationMatrix2D((self.width/2,self.height/2),x,1)		
			rframe = cv2.warpAffine(rframe,M,(self.width,self.height))
			cv2.imwrite('./Nonsense/new.png',rframe)
			vid.append(ImageClip('./Nonsense/new.png').set_duration(5).fadein(0.5).fadeout(0.5))
			x = random.choice([0,10,-10])
			if cv2.waitKey(1) == ord('q'): 
				break

		imgvid = concatenate(vid)
		imgvid.write_videofile('./Nonsense/final.avi',fps=self.fps,codec='mpeg4')

		new = []

		if self.music != None:
			time = VideoFileClip('./Nonsense/final.avi').duration
			audio = AudioFileClip(self.music)
			t = audio.duration
			if t < time:
				finalaudio = afx.audio_loop(audio, duration=time)
			else:
				finalaudio = audio.subclip(0,time)
			finalaudiof = finalaudio.audio_fadeout(5)
			existing = VideoFileClip('./Nonsense/final.avi').set_audio(finalaudiof)
		else:
			existing = VideoFileClip('./Nonsense/final.avi')

		if self.videos == None:
			existing.write_videofile(self.storage_path,fps=self.fps,codec='mpeg4')
			print("The output video is {}".format(self.storage_path))
			return

		if self.reverse_order == True:
			self.videos = list(reversed(self.videos))

		for i,video in enumerate(self.videos):
			clip = VideoFileClip(video)
			audio = clip.audio
			cap = cv2.VideoCapture(video)	
			fps = cap.get(cv2.CAP_PROP_FPS)
			fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
			outp = cv2.VideoWriter("./Nonsense/temp" + str(i) + ".avi", fourcc, fps, (self.width, self.height),True)
			status =  0
			while(cap.isOpened()):
				ret, frame = cap.read()
				if ret == True:
					rframe = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
					rframe = cv2.copyMakeBorder(rframe,20,20,20,20,cv2.BORDER_CONSTANT,value=[255,255,255])
					M = cv2.getRotationMatrix2D((self.width/2,self.height/2),x,1)		
					rframe = cv2.warpAffine(rframe,M,(self.width,self.height))
					if status == 0:
						firstframe = rframe
						cv2.imwrite('./Nonsense/first.png',firstframe)
						new.append(ImageClip('./Nonsense/first.png').set_duration(0.2).fadein(1))
						status = 1
					outp.write(rframe)
					if cv2.waitKey(1) == ord('q'):
						break
				else:
					break
			
			cap.release()
			outp.release()

			new.append(VideoFileClip('./Nonsense/temp' + str(i)  + '.avi').set_audio(audio))

			lastframe = rframe
			cv2.imwrite('./Nonsense/last.png',lastframe)
			new.append(ImageClip('./Nonsense/last.png').set_duration(0.2).fadeout(1))
			
		new.insert(0,existing)
		video = concatenate(new)
		video.write_videofile(self.storage_path,fps=self.fps,codec='mpeg4')
		shutil.rmtree('./Nonsense')
		shutil.rmtree('./__pycache__')
		print("The output video is {}".format(self.storage_path))
