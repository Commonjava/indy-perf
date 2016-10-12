#!/usr/bin/env python

import os
import sys
import urllib
import glob
import json


# if len(sys.argv) < 2:
#   print "Usage: %s <output-dir> [<repo-url>]" % sys.argv[0]
#   exit(1)

builds_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'inputs/build-data')
#repo_url = 'http://repo.maven.apache.org/maven2/'
repo_url='http://localhost:8080/api/remote/central/'
#out_dir = sys.argv[1]

def download(path):
    url = "%s%s" % (repo_url, path)
    print url
    urllib.urlretrieve(url, '/dev/null')


#print "Storing downloads in: %s" % out_dir

if len(sys.argv) > 1:
    repo_url = sys.argv[1]
    if not repo_url.endswith('/'):
        repo_url += '/'
    print "Populating: %s" % repo_url

build_files = glob.glob(os.path.join(builds_dir, '*.json'))

paths=[]

for build_file in build_files:
    with open(build_file) as f:
        build = json.load(f)
        for path in build['downloads']:
            if path not in paths:
                download(path)
                paths.append(path)

print "Populated %s files in: %s" % (len(paths), repo_url)
