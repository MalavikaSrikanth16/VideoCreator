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
from transition import mytool
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
		parser.add_argument('imgtxt', nargs='*', help="Path of images or text(within quotes) to display")
		parser.add_argument('-o', '--output', required=False, default='output', help="Output video file name")
		parser.add_argument('-oc', '--occasion', required=True, help="Occassion like Birthday, Anniversary, etc.")
		parser.add_argument('--reverse-order', default=False, action="store_true", help="Images to be displayed in reverse order")
		parser.add_argument('-m','--music', help="Background music")
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
		status = 1
		if len(self.images) > 0:
			for image in self.images:
				if os.path.splitext(image)[1] in IMAGE_TYPES:
					if os.path.exists(image):
						if status == 0:
							continue
						frame = cv2.imread(image)
						self.height, self.width, channels = frame.shape
						status = 0
					else:
						raise FileNotFound(1)
			if status == 1:
				self.height = 480
				self.width = 640
		else:
			self.height = 480
			self.width = 640

		status = 1
		if self.videos != None:
			self.videos = list(self.videos)
			for video in self.videos:
				if os.path.exists(video) and os.path.splitext(video)[1] in VIDEO_TYPES:
					if status == 0:
						continue
					cap = cv2.VideoCapture(video)
					self.fps = cap.get(cv2.CAP_PROP_FPS)
					cap.release()
					status = 0
				else:
					raise FileNotFound(2)
		else:
			self.fps = 10.0
						

	def create_video(self):
		
		self.images.insert(0, "")

		width = self.width - 40
		height = self.height - 40
		x = 0

		if not os.path.exists('./Nonsense'):
			os.makedirs('./Nonsense')

		font = ImageFont.truetype("orange_juice.ttf",75)
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
				font = ImageFont.truetype(random.choice(["orange_juice.ttf","font3.ttf","font5.ttf"]),75)
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

		m = mytool()
		vid = []
		count = 0
		for image in self.images:
			frame = cv2.imread(image)
			rframe = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
			rframe = cv2.copyMakeBorder(rframe,20,20,20,20,cv2.BORDER_CONSTANT,value=[255,255,255])
			M = cv2.getRotationMatrix2D((self.width/2,self.height/2),x,1)		
			rframe = cv2.warpAffine(rframe,M,(self.width,self.height))
			cv2.imwrite('./Nonsense/new.png',rframe)
			m.add_fade_effect('./Nonsense/new.png',0)
			vid.append(VideoFileClip('./Nonsense/final'+str(count)+'.mp4'))
			count = count + 1 
			x = random.choice([0,10,-10])
			if cv2.waitKey(1) & 0xFF == ord('q'): 
				break

		imgvid = concatenate(vid)
		imgvid.write_videofile('./Nonsense/final.avi',fps=self.fps,codec='mpeg4')

		new = []

		if self.videos == None:
			if self.music != None:
				time = VideoFileClip('./Nonsense/final.avi').duration
				audio = AudioFileClip(self.music).subclip(0,time)
				audiof = audio.audio_fadeout(5)
				video = VideoFileClip('./Nonsense/final.avi').set_audio(audiof)
			else:
				video = VideoFileClip('./Nonsense/final.avi')
			video.write_videofile(self.storage_path,fps=self.fps,codec='mpeg4')
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
						m.add_fade_effect('./Nonsense/first.png',1)
						new.append(VideoFileClip('./Nonsense/final'+str(count)+'.mp4'))
						count = count + 1
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
			m.add_fade_effect('./Nonsense/last.png',2)
			new.append(VideoFileClip('./Nonsense/final'+str(count)+'.mp4'))
			count = count + 1

		if self.music != None:
			time = VideoFileClip('./Nonsense/final.avi').duration
			audio = AudioFileClip(self.music).subclip(0,time)
			audiof = audio.audio_fadeout(5)
			existing = VideoFileClip('./Nonsense/final.avi').set_audio(audiof)
		else:
			existing = VideoFileClip('./Nonsense/final.avi')
			
		new.insert(0,existing)
		video = concatenate(new)
		video.write_videofile(self.storage_path,fps=self.fps,codec='mpeg4')
		shutil.rmtree('./Nonsense')
		shutil.rmtree('./__pycache__')
		print("The output video is {}".format(self.storage_path))
