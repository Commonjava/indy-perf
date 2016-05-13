#!/usr/bin/env python

import os
import sys
import urllib
import glob
import json


if len(sys.argv) < 2:
	print "Usage: %s <output-dir> [<repo-url>]" % sys.argv[0]
	exit(1)

repo_url = 'http://repo.maven.apache.org/maven2/'
out_dir = sys.argv[1]

def download(path):
	url = "%s%s" % (repo_url, path)
	print url

	outfile = os.path.join(out_dir, path)
	if os.path.isfile(outfile):
		return
	
	outdir = os.path.dirname(outfile)
	if not os.path.isdir(outdir):
		os.makedirs(outdir)

	urllib.urlretrieve(url, outfile)

print "Storing downloads in: %s" % out_dir

if len(sys.argv) > 2:
	repo_url = sys.argv[2]
	if not repo_url.endswith('/'):
		repo_url += '/'
	print "Downloading from: %s" % repo_url

build_files = glob.glob('inputs/build-data/*.json')

paths = set()
for build_file in build_files:
	with open(build_file) as f:
		build = json.load(f)
		for path in build['downloads']:
			if path not in paths:
				download(path)
				paths.add(path)

print "Downloaded %s files to: %s" % (len(paths), out_dir)
