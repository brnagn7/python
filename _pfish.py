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
import logging

log = logging.getLogger('main._pfish')

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
		logging.error('Unknown Hash Type Specified')
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
	
	
	
