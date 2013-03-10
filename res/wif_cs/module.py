__author__ = 'pmeier'

import os

ORIG = '/home/pmeier/Workspace/WIFvassal/res/wif_cs'
DEST = '/home/pmeier/Workspace/WIFvassal/mod/WiFdab/images'

for d in os.listdir(ORIG):
    if d.startswith('cs'):
        print 'moving', d
        for f in os.listdir('./{:s}'.format(d)):
            print '{}_{}'.format(d, f)
            with open(os.path.join(ORIG, d, f), 'r') as ipf:
                with open(os.path.join(DEST, '_'.join([d, f])), 'w') as opf:
                    opf.write(ipf.read())
