#
# pfish support functions, where all the real work is done
#
# FUNCTIONS:
#
# DisplayMessage()
# ParseCommandLine()
# WalkPath()
# HashFile()
# ValidateDirectory()
# ValidateDirectoryWritable()
#
# CLASSES:
#
# class_CVSWriter
#
# ----------------------------------------------

# IMPORTS:
#
import os
import stat
import time
import hashlib
import argparse
import csv
import logging as log

log = log.getLogger('main._pfish')

# ========================================
#
# FUNCTION: DisplayMessage()
#
# Desc:		displays message
# Input:	message type string
# Actions:	use print function to display message
#

def displayMessage(msg):
	if gl_args.verbose:
		print(msg)
	return

# ========================================
# 
# FUNCTION: ParseCommandLine()
#
# Desc:		process and validate CLI args
# Input:	none
# Actions:	use 'argparse', establish a global variable 'gl_args'
#

def ParseCommandLine():

	parser = argparse.ArgumentParser('Python file system hashing... p-fish')
	parser.add_argument('-v', '-verbose', help='allows progress messages to be displayed', action='store_true')
	
	# setup a group the user must use
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--md5', help='specifies MD5 algorithm', action='store_true')
	group.add_argument('--sha256', help='specifies SHA256 algorithm', action='store_true')
	group.add_argument('--sha512', help='specifies SHA512 algorithm', action='store_true')
	group.add_argument('-d', '--rootPath', type=ValidateDirectory, required=True, help='specifiy the root path for hashing')
	group.add_argument('-r', '--reportPath', type=ValidateDirectoryWritable, required=True, help='specifiy the path for reports and logs')

	# create the object to hold args, and make available to all function in this module
	global gl_args
	global gl_hashType

	gl_args = parser.parse_args()
	if gl_args.md5:
		gl_hashType = 'MD5'
	elif gl_args.sha256:
		gl_hashType = 'SHA256'
	elif gl_args.sha512:
		gl_hashType = 'SHA512'
	else:
		gl_hashType = "Unknown"
		log.error('Unknown Hash Type Specified')
	DisplayMessage("Command line processed. Successfully")
	
	return

	

# ========================================
# 
# FUNCTION: WalkPath()
#
# Desc:		walk the path specified
# Input:	none, uses CLI args
# Actions:	use 'os' and 'sys' modules to traverse directories as root path.
#		For each file discovered, will call HashFile() to perform hashing.
#

def WalkPath():
	
	processCount = 0
	errorCount = 0

	oCVS - _CSVWriter(gl_args.reportPath+'fileSystemReport.csv', gl_hashType)

	# create a loop to process all the files starting at rootPath including sub directories
	log.info('Root Path: ' + gl_args.rootPath)
	for root, dirs, files in os.walk(gl_args.rootPath):
		# for each file call the HashFile function
		for file in files:
			fname = os.path.join(root, file)
			result = HashFile(fname, file, oCVS)
			if result is True:
				processCount += 1
			else:
				ErrorCount += 1

		oCVS.writerClose()
		
		return(processCount)


# ========================================
# 
# FUNCTION: HashFile()
#
# Desc:		Process a single file, hash it, grab metadata
# Input:	theFile = the full path of the file
# Actions:	Attempts to hash the file and extract metadata
#		Calls GenerateReport for successfull hashes
#

def HashFile(theFile, simpleName, o_result):

	# verify path is valid
	if os.path.exists(theFile):
		# verify the path is not a symbolic link
		if not os.path.islink(theFile):
			# verify the file is real
			if os.path.isfile(theFile):

				try:
					# Attempt to open the file
					f = open(theFile, 'rb')
				except IOError:
					# if open fails report error
					log.warning('Open Failed: ' + theFile)
					return
				else:
					try:
						# Get the Basic File Attributes
						# Before attempting to open the file
						# This should preserve the access time on most OS's

						theFileStats = os.stat(theFile)
						(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(theFile)

						# Attempt to read the file
						rd = f.read()

					except IOError:
						# if read fails, then close the file and report error
						f.close()
						log.warning('File Access Error: ' + theFile)
						return
					else:

						# Print the simple file name
						DisplayMessage("Processing File: " + theFile)
						log.info("Processing File: " + theFile)

						# Get the size of the file in Bytes
						fileSize = str(size)

						# Get MAC Times
						modifiedTime = time.ctime(mtime)
						accessTime = time.ctime(atime)
						createdTime = time.ctime(ctime)

						ownerID = str(uid)
						groupID = str(gid)
						fileMode = bin(mode)

						# process the file hashes

						if gl_args.md5:
							# Calculate and Print the MD5
							hash = hashlib.md5()
							hash.update(rd)
							hexMD5 = hash.hexdigest()
							hashValue = hexMD5.upper()
						elif gl_args.sha256:
							hash = hashlib.sha256()
							hash.update(rd)
							hexSHA256 = hash.hexdigest()
							hashValue = hexSHA256.upper()
						elif gl_args.sha512:
							# Calculate and Print the SHA512
							hash = hashlib.sha512()
							hash.update(rd)
							hexSHA512 = hash.hexdigest()
							hashValue = hexSHA512.upper()
						else:
							log.error('Hash not Selected')

							# File processing complete
							# Close the active file
							print "==================================="
							f.close()

						# write one row to the output file

						o_result.writeCSVRow(simpleName, theFile, fileSize, modifiedTime, accessTime, createdTime, hashValue, ownerID, groupID, mode)
						return True
			else:
					log.warning('[' + repr(simpleName) + ', Skipped NOT a File' + ']')
					return False
		else:
					log.warning('[' + repr(simpleName) + ', Skipped Link NOT a File' + ']')
					return False
	else:
					log.warning('[' + repr(simpleName) + ', Path does NOT exist' + ']')
	return False

# ========================================
#
# FUNCTION: ValidateDirectory()
#
# Desc:		validates directory path as existing and readable
# Input:	a string representing the directory path
# Actions:	Validate directory string
#

def ValidateDirectory(theDir):
	# Validate the path is a directory
	if not os.path.isdir(theDir):
		raise argparse.ArgumentTypeError('Directory does not exist')

	# Validate the path is readable
	if os.access(theDir, os.R_OK):
		return theDir
	else:
		raise argparse.ArgumentTypeError('Directory is not readable')


#
# ValidateDirectoryWritable()
#
# Desc: Function that will validate a directory path as
#           existing and writable.  Used for argument validation only
#
# Input: a directory path string
#
# Actions:
#              if valid will return the Directory String
#
#              if invalid it will raise an ArgumentTypeError within argparse
#              which will inturn be reported by argparse to the user
#

def ValidateDirectoryWritable(theDir):
	# Validate the path is a directory
	if not os.path.isdir(theDir):
		raise argparse.ArgumentTypeError('Directory does not exist')

	# Validate the path is writable
	if os.access(theDir, os.W_OK):
		return theDir
	else:
		raise argparse.ArgumentTypeError('Directory is not writable')

# ========================================
#
# CLASS: _CVSWriter
#
#
class _CSVWriter:

	def __init__(self, fileName, hashType):
		try:
			# create a writer object and then write the header row
			self.csvFile = open(fileName, 'wb')
			self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
			self.writer.writerow(('File', 'Path', 'Size', 'Modified Time', 'Accessed Time', 'Created Time', 'hashType', 'Owner', 'Group', 'Mode'))
		except:
			log.error('CSV File Failure')

	def writeCSVRow(self, fileName, filePath, fileSize, mTime, aTime, cTime, hashVal, own, grp, mod):

		self.writer.writerow((fileName, filePath, fileSize, mTime, aTime, cTime, hashVal, own, grp, mod))

	def writerClose(self):
		self.csvFile.close()