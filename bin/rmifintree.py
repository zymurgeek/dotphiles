#!/usr/bin/env python

import logging
import os
import sys

def rmIfInTree(dirRootName, subjectPath, containsName, dryRun):
	dirRootName = os.path.abspath(dirRootName)
	subjectPath = os.path.abspath(subjectPath)
	if not os.path.isdir(dirRootName):
		logging.warning(dirRootName + " is not a directory")
		return
	if not os.path.isfile(subjectPath):
		logging.warning(subjectPath + " is not a file")
		return
	logging.debug('Looking for files identical to subject file ' \
	+ subjectPath + ' in directory ' + dirRootName)
	(subjectDir,subjectBase) = os.path.split(subjectPath)
	for compPath, compDirs, compBases in os.walk(dirRootName):
		logging.debug("Checking directory " + compPath)
		if compPath != subjectDir:
			for compBase in compBases:
				if compBase == subjectBase or \
                                (containsName and subjectBase in compBase):
					compPath = os.path.join(compPath, \
					compBase)
					logging.debug('Found comparision ' \
					+ 'file ' + compPath)
                    			cmd = 'cmp -s "' + subjectPath + '" "' \
					+ compPath + '"'
                    			result = os.system(cmd)
                    			if not result:
                        			logging.debug('Removing' \
						+ ' identical subject' \
						+ ' file ' + subjectPath)
						if not dryRun:
                        				os.remove(subjectPath)
						return
					else:
						logging.debug('Keeping non-' \
						+ 'identical subject file ' \
						+ subjectPath)
		else:
			logging.debug("Skipping subject's directory " \
			+ subjectDir)

if __name__ == '__main__':
	usage = "usage: %prog [options] <dir> <file>[...]\n" \
	"Will remove each <file> that exists in the directory tree rooted\n" \
	"at <dir>.  The file must match in name and contents to be removed.\n"\
	"For instance, to remove all files from the current directory tree\n" \
	"that exist on a CD:\n" \
	"find . -type f | xargs %prog /media/CDROM"

	from optparse import OptionParser

	parser = OptionParser(usage)
	parser.add_option("-d", "--dry-run", action="store_true",
		dest="dryRun", default=False,
		help="Don't actually remove any files")
	parser.add_option("-l", "--logging", action="store_true",
		dest="logging", default=False,
		help="Log debug information while running")
	parser.add_option("-c", "--contains-name", action="store_true",
		dest="containsName", default=False,
		help="Match files in <dir> if their name contains <file> " \
                "rather than matches <file> exactly")
	(options, args) = parser.parse_args()
	if options.logging:
		logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s %(levelname)s %(message)s',
			filename='rmifintree.log',
			filemode='w')
		logging.debug("Logging enabled")
	if len(args) < 2:
		print "Not enough command line arguments--try -h for help."
		sys.exit(-1)

	dir = args[0]
	for arg in args[1:]:
           	rmIfInTree(dir, arg, options.containsName, options.dryRun)
