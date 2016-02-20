#! /usr/bin/python

from exception.ID3Error import ID3Error

# ID3 byte string at the start of the tag.
ID3_IDENTIFIER = b'\x49\x44\x33'

# Byte order
BYTE_ORDER = "big"

# Frame header encoding
FRAME_HEADER_ENCODING = "latin1"

# Encoding flags
def encoding(byte):
	if byte == b'\x00':
		return "latin1"
	elif byte == b'\x01':
		return "utf16"
	else:
		raise ID3Error("Encoding '%b' is unknown." %byte)

def terminator(byte):
	if byte == b'\x00':
		return b'\x00'
	elif byte == b'\x01':
		return b'\x00\x00'
	else:
		raise ID3Error("Encoding '%b' is unknown." %byte)

def latin(raw):
	for i in range(len(raw)):
		if raw[i] == 0:
			return raw[:i].decode("latin1")
	return raw.decode("latin1")

def utf16(raw):
	BOM = raw[:2]
	for i in range(2,len(raw)-3):
		if raw[i:i+2] == b'\x00\x00':
			return raw[:i-1].decode("utf16")
	try :
		return raw.decode("utf16")
	except:
		return raw

def decode(enc, raw):
	if enc == 0:
		return latin(raw)
	elif enc == 1:
		return utf16(raw)
	else:
		return raw