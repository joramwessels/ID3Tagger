#! /usr/bin/python

from exception.ID3Error import ID3Error
from constants import FRAME_HEADER_ENCODING, decode, encoding, terminator, latin, utf16
from constants import BYTE_ORDER as BO

class Frame:
	
	def __init__(self, file):
		header = self.readHeader(file)
		for key, value in header.items():
			setattr(self, key, value)
		# TODO size includes appendices?
		raw = file.read(self.size)
		body = parseBody(self.id, raw)
		for key, value in body.items():
			setattr(self, key, value)
	
	def readHeader(self, file):
		flagMask = 0x1f1f
		messages = []
		header = {}
		
		frame_id = file.read(4).decode(FRAME_HEADER_ENCODING)
		frame_size = int.from_bytes(file.read(4), byteorder=BO)
		frame_flags = int.from_bytes(file.read(2), byteorder=BO)
		compressed = frame_flags & 0x0080
		encrypted = frame_flags & 0x0040
		contains_group_information = frame_flags & 0x0020
		
		if frame_flags & flagMask:
			messages += ["Frame flags for '%s' are corrupted." %frame_id]
		if frame_size < 1:
			messages += ["Frame size for frame '%s' is equal to 0." %frame_id]
		
		header["id"] = frame_id
		header["size"] = frame_size
		header["tag_preservation"] = bool(frame_flags & 0x8000)
		header["file_preservation"] = bool(frame_flags & 0x4000)
		header["read_only"] = bool(frame_flags & 0x2000)
		
		if compressed:
			header["decompressed_size"] = int.from_bytes(file.read(4), byteorder=BO)
		if encrypted:
			header["encryption"] = int.from_bytes(file.read(1), byteorder=BO)
		if contains_group_information:
			header["group"] = int.from_bytes(file.read(1), byteorder=BO)
		
		return header

def parseT000(raw):
	# Text encoding	$xx
	# Information	<text string according to encoding>
	enc = raw[0]
	dec = decode(enc, raw[1:])
	return {"content":dec}

def parseW000(raw):
	# URL			<text string>
	return {"content":latin(raw)}

def parseTXXX(raw):
	# Text encoding	$xx
	# Description	<text string according to encoding> $00 (00)
	# Value			<text string according to encoding>
	return {"raw":raw}

def parseWXXX(raw):
	# Text encoding	$xx
	# Description	<text string according to encoding> $00 (00)
	# URL			<text string>
	return {"raw":raw}

def parseIPLS(raw):
	# Text encoding	$xx
	# People list	<text strings according to encoding>
	return {"raw":raw}

def parseMCDI(raw):
	# CD TOC		<binary data>
	return {"raw":raw}

def parseETCO(raw):
	# Time stamp format	$xx
	return {"raw":raw}

def parseMLLT(raw):
	return {"raw":raw}

def parseSYTC(raw):
	return {"raw":raw}

def parseUSLT(raw):
	return {"raw":raw}

def parseSYLT(raw):
	return {"raw":raw}

def parseCOMM(raw):
	# TODO
	enc = raw[0:1]
	lang = raw[1:4]
	desc = decode(enc, raw[4:])
	i = raw[4:].index(terminator(enc)) + len(terminator(enc))
	cont = decode(enc, raw[i:])
	return {"raw":raw, "language":lang, "description":desc, "content":cont}

def parseRVAD(raw):
	return {"raw":raw}

def parseEQUA(raw):
	return {"raw":raw}

def parseRVRB(raw):
	return {"raw":raw}

def parseAPIC(raw):
	return {"raw":raw}

def parseGEOB(raw):
	return {"raw":raw}

def parsePCNT(raw):
	return {"raw":raw}

def parsePOPM(raw):
	return {"raw":raw}

def parseRBUF(raw):
	return {"raw":raw}

def parseAENC(raw):
	return {"raw":raw}

def parseLINK(raw):
	return {"raw":raw}

def parsePOSS(raw):
	return {"raw":raw}

def parseUSER(raw):
	return {"raw":raw}

def parseOWNE(raw):
	return {"raw":raw}

def parseCOMR(raw):
	return {"raw":raw}

def parseENCR(raw):
	return {"raw":raw}

def parseGRID(raw):
	return {"raw":raw}

def parsePRIV(raw):
	return {"raw":raw}

global parser
parser = {	"TXXX":parseTXXX,
			"WXXX":parseWXXX,
			"IPLS":parseIPLS,
			"MCDI":parseMCDI,
			"ETCO":parseETCO,
			"MLLT":parseMLLT,
			"SYTC":parseSYTC,
			"USLT":parseUSLT,
			"SYLT":parseSYLT,
			"COMM":parseCOMM,
			"RVAD":parseRVAD,
			"EQUA":parseEQUA,
			"RVRB":parseRVRB,
			"APIC":parseAPIC,
			"GEOB":parseGEOB,
			"PCNT":parsePCNT,
			"POPM":parsePOPM,
			"RBUF":parseRBUF,
			"AENC":parseAENC,
			"LINK":parseLINK,
			"POSS":parsePOSS,
			"USER":parseUSER,
			"OWNE":parseOWNE,
			"COMR":parseCOMR,
			"ENCR":parseENCR,
			"GRID":parseGRID,
			"PRIV":parsePRIV}

def parseBody(frameID, raw):
	if frameID.startswith('T'):
		return parseT000(raw)
	elif frameID.startswith('W'):
		return parseW000(raw)
	elif frameID in parser.keys():
		return parser[frameID](raw)
	else:
		return raw
