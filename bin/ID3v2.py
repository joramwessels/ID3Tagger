#! /usr/bin/python

from exception.ID3Error import ID3Error
from Frame import Frame
from constants import BYTE_ORDER as BO
from constants import ID3_IDENTIFIER as ID3

class ID3v2:
	
	__supported = [3]
	
	def __init__(self, file):
		self.readHeader(file)
		if self.extended_header:
			self.readExtendedHeader(file)
		self.readFrames(file)
	
	def readHeader(self, file):
		flagMask = 0x1f
		sizeMask = 0x80
		
		id = file.read(3)
		version = int.from_bytes(file.read(1), byteorder=BO)
		revision = int.from_bytes(file.read(1), byteorder=BO)
		flags = int.from_bytes(file.read(1), byteorder=BO)
		sizes = [int.from_bytes(file.read(1), byteorder=BO) for i in range(4)]
		size = sizes[0] * 64**3 + sizes[1] * 64**2 + sizes[2] * 64**1 + sizes[3]
		
		unsynchronisation = bool(flags & 0x80)
		extendedHeader = bool(flags & 0x40)
		experimental = bool(flags & 0x20)
		
		messages = []
		if id != ID3:
			messages += ["File does not start with the %b identifier." %ID3]
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
			self.extended_header = extendedHeader
			self.experimental = experimental
			self.size = size
	
	def readExtendedHeaders(self, file):
		acceptableSizes = [6,10]
		
		extendedHeaderSize = int.from_bytes(file.read(4))
		crcAppendix = int.from_bytes(file.read(2)) & 0x8000
		paddingSize = int.from_bytes(file.read(4))
		
		if not extendedHeaderSize in acceptableSizes:
			message = "Extended header size '%i' is invalid."
			raise ID3Error([message %extendedHeaderSize])
		if crcAppendix:
			CRC = int.from_bytes(file.read(4))
			self.CRC = CRC
		else:
			self.CRC = None
		self.padding_size = paddingSize
	
	def readFrames(self, file):
		frameHeaderSize = 10
		bytes = 0
		frames = []
		while bytes < self.size:
			frame = Frame(file)
			bytes += frame.size + frameHeaderSize
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
