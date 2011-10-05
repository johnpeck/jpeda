# sortparts.py
#
# Sorts parts in the purchasing directory by part number.
#
# Usage: python sortparts.py

#------------------- Begin configuration ------------------------------
partfiles = ['descriptions.dat',
             'digikey.dat',
             'newark.dat',
             'jameco.dat',
             'mcmaster.dat']
#-------------------- End configuration -------------------------------

import os
import sys
""" Bring in the partman module for part file management """
pmpath = os.path.abspath('../scripts')
sys.path.append(pmpath)
import partman

""" Either importing partman or calling partman.multisort sets the
    path to the __file__ variable to 'scripts'.  Create pathnames
    relative to the purchasing directory instead. """
purchdir = os.path.dirname(os.path.realpath(__file__))
purchdir = purchdir.split('scripts')[0] + 'purchasing'

def main():
    for filename in partfiles:
        longname = purchdir + '/' + filename
        print ('Sorting ' + filename + '...'),
        partman.multisort(longname,1)
        print 'done'

if __name__ == "__main__":
    main()
