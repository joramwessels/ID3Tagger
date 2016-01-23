#! /usr/bin/python

import sys, os, re
from exception.ID3Error import ID3Error
from Frame import Frame

def main():
	tag = ID3v2(sys.argv[1])
	print([t.id for t in tag.getFrames()])
	#print([t.body for t in tag.getFrames()])

class ID3v2:
	
	__supported = [3]
	
	def __init__(self, filename):
		file = open(filename, 'rb')
		try:
			self.readHeader(file)
			if self.extended_header:
				self.readExtendedHeader(file)
			self.readBody(file)
		except ID3Error as e:
			print(e)
		file.close()
	
	def readHeader(self, file):
		flagMask = 0x1f
		sizeMask = 0x80
		id3 = b'\x49\x44\x33'
		BO = "big"
		
		id = file.read(3)
		version = int.from_bytes(file.read(1), byteorder=BO)
		revision = int.from_bytes(file.read(1), byteorder=BO)
		flags = int.from_bytes(file.read(1), byteorder=BO)
		sizes = [int.from_bytes(file.read(1), byteorder=BO) for i in range(4)]
		size = sizes[0] * 64**3 + sizes[1] * 64**2 + sizes[2] * 64**1 + sizes[3]
		
		unsynchronisation = bool(flags & 0x80)
		extended_header = bool(flags & 0x40)
		experimental = bool(flags & 0x20)
		
		messages = []
		if id != id3:
			messages += ["File does not start with the %b identifier." %id3]
		if not version in self.__supported:
			messages += ["Version %i is not supported." %version]
		if flags & flagMask:
			messages += ["Header flags are corrupted."]
		if experimental:
			messages += ["Tag is flagged as 'experimental'."]
		if any([b & sizeMask for b in sizes]):
			messages += ["Tag size is corrupted."]
		if len(messages) > 0:
			raise ID3Error(messages)
		else:
			self.version = version
			self.revision = revision
			self.unsynchronisation = unsynchronisation
			self.extended_header = extended_header
			self.experimental = experimental
			self.size = size
	
	def readExtendedHeaders(self, file):
		acceptable_sizes = [6,10]
		
		extended_header_size = int.from_bytes(file.read(4))
		crc_appendix = int.from_bytes(file.read(2)) & 0x8000
		padding_size = int.from_bytes(file.read(4))
		
		if not extended_header_size in acceptable_sizes:
			message = "Extended header size '%i' is invalid."
			raise ID3Error([message %extended_header_size])
		if crc_appendix:
			CRC = int.from_bytes(file.read(4))
			self.CRC = CRC
		else:
			self.CRC = None
		self.padding_size = padding_size
	
	def readBody(self, file):
		frame_header_size = 10
		bytes = 0
		frames = []
		while bytes < self.size:
			frame = Frame(file)
			bytes += frame.size + frame_header_size
			frames.append(frame)
		self.frames = frames
	
	def getHeader(self):
		headers = {}
		headers["version"] = self.version
		headers["revision"] = self.revision
		headers["unsynchronisation"] = self.unsynchronisation
		headers["extended_header"] = self.extended_header
		headers["experimental"] = self.experimental
		headers["size"] = self.size
		return headers
	
	def getExtendedHeader(self):
		headers = {}
		try:
			headers["padding_size"] = self.padding_size
			headers["CRC"] = self.CRC
			return headers
		except AttributeError:
			return None
	
	def getFrames(self):
		return self.frames

if __name__ == "__main__":
	main()