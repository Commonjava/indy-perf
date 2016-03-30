#!/usr/bin/env python

import json
import os
import sys

if len(sys.argv) < 3:
	print "Usage: %s <json-dir> <csv-dir>" % sys.argv[0]
	exit(1)

JSON_DIR=sys.argv[1]
CSV_DIR=sys.argv[2]

if not os.path.isdir(CSV_DIR):
	os.makedirs(CSV_DIR)

count=0
for filename in os.listdir(JSON_DIR):
	paths=[]

	print "Processing %s" % filename
	with open(os.path.join(JSON_DIR, filename)) as f:
		data=json.load(f)
		if data.get('affectedStores') is None:
			continue

		central = data['affectedStores'].get('remote:central')
		if central is not None and central.get('downloadedPaths') is not None:
			for path in central['downloadedPaths']:
				paths.append(path)

		sharedImports = data['affectedStores'].get('hosted:shared-imports')
		if sharedImports is not None and sharedImports.get('downloadedPaths') is not None:
			for path in sharedImports['downloadedPaths']:
				paths.append(path)


	csvname="downloads-%s.csv" % count

	print "Writing %s" % csvname
	with open(os.path.join(CSV_DIR, csvname), 'w') as f:
		f.write("\n".join(paths))
		f.write('\n')

	count+=1

print "Wrote %s CSV files to: %s" % (count, CSV_DIR)

