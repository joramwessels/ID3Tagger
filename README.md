# ID3Tagger
A python program that can organize a music library, both in overall structure as in ID3 tags.

## Backlog ##
* ID3.py
  * 0.1 - Reads ID3v2 headers
  * 0.2 - Reads ISO 8859-1 T000 frames
  * 0.3 - Supports UCS2
  * 0.4 - Reads COMM and APIC frames
  * 0.5 - Supports all encodings
  * 0.6 - Reads all frames
  * 0.7 - Logs corrupted/unreadable files
  * 0.8 - Writes ID3v2 tags
  * 0.9 - Reads ID3v1 tags
  * 0.10- ID3v1 genre reference table
  * 1.0 - Successfully reads all files in the library
* Enricher.py
  * 0.1 - Returns files without the specified field
  * 0.2 - Predicts missing artist information using tags
  * 0.3 - Predicts missing album, year, genre and track number
  * 0.4 - Predicts using folder profile as well as tags
  * 0.5 - Assigns folder image to APIC tag
  * 1.0 - Enriches all files in the library and logs objections
  * 1.1 - Automatically assigns BPM
* Organizer.py
  * 0.1 - Returns items that do not conform to file name format
  * 0.2 - Attempts to recognize file name format using tags
  * 0.3 - Returns files that contain inconsistent information
  * 0.4 - Returns folders that contain inconsistent information
* Choice of formats & user preferences
* Convert to Visual C++ with GUI

## Discovered bugs ##
* None found

## Log ##
* **23-1-2016, 13:00 - 17:00:** Basic structure and models, reading ID3v2 headers
* **24-1-2016, 11:00 - 16:00:** Decoding frame contents
* **20-2-2016, 12:00 - 16:00:** Planning and architectural design

## Useful articles ##
* https://en.wikipedia.org/wiki/Code_page_437
* https://en.wikipedia.org/wiki/ISO/IEC_8859-1
* http://www.columbia.edu/kermit/ucs2.html
