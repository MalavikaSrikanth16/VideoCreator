
import sys

class FileNotFound(Exception):
	"""If file path is invalid"""
	def __init__(self, status_code):
		self.status_code = status_code