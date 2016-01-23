#! /usr/bin/python

class ID3Error(Exception):
	
	def __init__(self, messages, sep="\n - "):
		self.sep = sep
		self.messages = messages
	
	def __str__(self):
		return "ID3Error(s):" + self.sep + self.sep.join(self.messages)
	
	def addMessages(self, additional):
		self.messages.extend(additional)