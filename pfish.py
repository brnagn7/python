#
# File:		Python File System Hash (pfish.py)
#
# Author:	Ed Mooney
#
# Date: 	28 APR 2017
#
# Version:	1.0
#
# Desc:		Walks through the file system, and hashes every file it finds, creates a report.
#

import logging		# Python Standard Library Logger
import time		# Python STL time functions
import sys		# Python STL system specs
import _pfish		# Our own module _pfish.py

if __name__=='__main__':
	
	PFISH_VERSION = '1.0'

	# Turn on logging
	logging.basicConfig(filename='pFishLog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
	# Process the CLI args
	_pfish.ParseCommandLine()
	# Record the starting time
	startTime = time.time()
	# Welcome message
	logging.info(")
	logging.info('Welcome to pfish version ' + PFISH_VERSION + ' ... New Scan Started...')
	logging.info(")
	_pfish.DisplayMessage('Welcome to pfish ... version ' + PFISH_VERSION)
	# Record some system information
	logging.info('System: ' + sys.platform)
	logging.info('Version: ' + sys.version)

	# Traverse the file system and hash the files
	filesProcessed = _pfish.WalkPath()

	# Record the end time and calculate the duration
	endTime() = time.time()
	duration = endTime - startTime
	logging.info('Files Processed: ' + str(filesProcessed))
	logging.info('Elapsed Time: ' + str(duration) + ' seconds')
	logging.info(")
	logging.info('Program Terminated Normally')
	logging.info(")
	
	_pfish.DisplayMessage("Program End")

# EOF
