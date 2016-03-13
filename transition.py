# fade.py
# This code creates two slides with fade-in and fade-out
import os
import sys
import subprocess
import psutil

class mytool:
	def __init__(self):
		self.count = 0
		self.copied_file = ['./in001.png', './in002.png']

	def add_fade_effect(self, filename, status):
		for f in self.copied_file:
			cmd = map(lambda x: '%s' %x, ['cp', filename, f])
			subprocess.call(cmd)

		in_framerate = 1./3
		out_framerate = 10.0
		cmd = ['ffmpeg', '-r', in_framerate, '-i','in%03d.png','-c:v','libx264',
              '-r', out_framerate, '-y','-pix_fmt','yuv420p','./Nonsense/slide.mp4']
		cmd = map(lambda x: '%s' %x, cmd)
		subprocess.call(cmd)

		if status != 2:
			cmd = ['ffmpeg', '-i','./Nonsense/slide.mp4','-y','-vf','fade=in:0:10','./Nonsense/slide_fade_in.mp4']
			subprocess.call(cmd)

		if status != 1:
			if status == 0:
				cmd = ['ffmpeg', '-i','./Nonsense/slide_fade_in.mp4','-y','-vf','fade=out:20:10', './Nonsense/slide_fade_in_out.mp4']
			elif status == 2:
				cmd = ['ffmpeg', '-i','./Nonsense/slide.mp4','-y','-vf','fade=out:30:20', './Nonsense/slide_fade_out.mp4']
			subprocess.call(cmd)

		slide_name = './Nonsense/final'+str(self.count)+'.mp4'

		if status == 0:
			cmd = map(lambda x: '%s' %x, ['cp', './Nonsense/slide_fade_in_out.mp4', slide_name])
		elif status == 1:
			cmd = map(lambda x: '%s' %x, ['cp', './Nonsense/slide_fade_in.mp4', slide_name])
		elif status == 2:
			cmd = map(lambda x: '%s' %x, ['cp', './Nonsense/slide_fade_out.mp4', slide_name])      	
		subprocess.call(cmd)

		for f in self.copied_file:
			cmd = map(lambda x: '%s' %x, ['rm','-f', f])
			subprocess.call(cmd)

		self.count += 1

    
