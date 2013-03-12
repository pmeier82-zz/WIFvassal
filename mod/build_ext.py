#!/bin/env python

import zipfile, os, sys

MOD = 'WiFdab_counters'
DIR = '/home/pmeier/Workspace/WIFvassal/mod'
DIR = '/home/pmeier/Workspace/WIFvassal/mod/WiFdab_ext'
NEW = '.'.join([MOD, 'zip'])
#NEW = 'new.zip'

if not os.path.isdir(os.path.join(DIR, MOD)):
    print 'no directory', os.path.join(DIR, MOD)
    sys.exit(1)
else:
    print 'found directory', os.path.join(DIR, MOD)

if os.path.exists(os.path.join(DIR, NEW)):
    os.remove(os.path.join(DIR, NEW))
    print 'removed archive', os.path.join(DIR, NEW)

with zipfile.ZipFile(os.path.join(DIR, NEW), 'w') as zf:
    for path, dirs, files in os.walk(os.path.join(DIR, MOD)):
        for f in files:
            dirname = ''
            if os.path.basename(path) != MOD:
                dirname = os.path.basename(path)
            zf.write(os.path.join(path, f),
                     '/'.join([dirname, f]))

print 'all done!'
