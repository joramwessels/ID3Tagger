#! /usr/bin/python

from exception.ID3Error import ID3Error

class Frame:
	
	def __init__(self, file):
		self.readHeader(file)
		self.readBody(file)
	
	def readHeader(self, file):
		flagMask = 0x1f1f
		header_encoding = "latin1"
		BO = 'big'
		
		frame_id = file.read(4).decode(header_encoding)
		frame_size = int.from_bytes(file.read(4), byteorder=BO)
		frame_flags = int.from_bytes(file.read(2), byteorder=BO)
		
		messages = []
		if frame_flags & flagMask:
			messages += ["Frame flags for '%s' are corrupted." %frame_id]
		if frame_size < 1:
			messages += ["Frame size for frame '%s' is equal to 0." %frame_id]
		if len(messages) > 0:
			raise ID3Error(messages)
		
		self.id = frame_id
		self.size = frame_size
		self.tag_preservation = bool(frame_flags & 0x8000)
		self.file_preservation = bool(frame_flags & 0x4000)
		self.read_only = bool(frame_flags & 0x2000)
		compressed = frame_flags & 0x0080
		encrypted = frame_flags & 0x0040
		contains_group_information = frame_flags & 0x0020
		
		if compressed:
			self.decompressed_size = int.from_bytes(file.read(4), byteorder=BO)
		else:
			self.decompressed_size = None
		if encrypted:
			self.encryption = int.from_bytes(file.read(1), byteorder=BO)
		else:
			self.encryption = None
		if contains_group_information:
			self.group = int.from_bytes(file.read(1), byteorder=BO)
		else:
			self.group = None
	
	def readBody(self, file):
		# TODO size includes appendices?
		body = file.read(self.size)
		self.body = body
	
	def getHeader(self):
		headers = {}
		headers["id"] = self.id
		headers["size"] = self.size
		headers["tag_preservation"] = self.tag_preservation
		headers["file_preservation"] = self.file_preservation
		headers["read_only"] = self.read_only
		headers["decompressed_size"] = self.decompressed_size
		headers["encryption"] = self.encryption
		headers["group"] = self.group
		return headers
	
	def getBody(self):
		return self.body
