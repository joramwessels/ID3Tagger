#! /usr/bin/python
# ID3 30 00

import sys, os
from ID3v2 import ID3v2
from exception.ID3Error import ID3Error

def main():
	try:
		file = open(sys.argv[1], 'rb')
		tag = ID3v2(file)
		frames = tag.getFrames()
		for frame in frames:
			print(frame.id, end='\t')
			try:
				print(frame.content)
			except:
				print("Not parsed")
		file.close()
	except ID3Error as e:
		print(e)

if __name__ == "__main__":
	main()