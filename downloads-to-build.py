#!/usr/bin/env python

import os
import sys
from random import randint, sample
import re
import json

DOWNLOAD_DATA='inputs/download-data'
DOWNLOAD_FILE_RE='downloads-([0-9]+).csv'
BUILD_DATA='inputs/build-data'

groupBases = ['com', 'org', 'net', 'io']

words = [line.rstrip() for line in open('inputs/words.txt')]
versionParts = list(range(10))

def generate_coord():
	gid = sample(groupBases, 1)
	gid.extend(sample(words, randint(1,5)))
	coord = {
		'gid': ".".join(gid),
		'aid': "-".join(sample(words, randint(1,4))),
		'ver': ".".join("{0}".format(n) for n in sample(versionParts, randint(1,3)))
	}
	return "%(gid)s:%(aid)s:%(ver)s" % coord


print "Iterating download listings in: "
for df in os.listdir(DOWNLOAD_DATA):
	print "Checking: %s" % df
	m = re.match(DOWNLOAD_FILE_RE, df)
	if m is not None:
		downloadFile = os.path.join(DOWNLOAD_DATA, df)
		print "Reading: %s" % downloadFile
		build = {
			'uploadCoords': [generate_coord()],
			'downloads': [line.rstrip() for line in open(downloadFile)]
		}

		buildFile = os.path.join(BUILD_DATA, "build-%s.json" % m.group(1))
		print "Writing: %s" % buildFile

		with open(buildFile, 'w') as bf:
			json.dump(build, bf, indent=2)
	else:
		print "%s is not a download CSV file." % os.path.join(DOWNLOAD_DATA, df)




