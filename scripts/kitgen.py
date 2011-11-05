# kitgen.py
# Generate files that can be used to order parts for circuit boards.
# Uses the output from gnetlist's bom2 script
import sys, os

# The script will always refer to paths relative to where the kitgen.py
# script is actually located.
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import partman

#---------------------------Begin configuration-------------------------

""" The relative path from the project/eda/scripts directory to the
    schematics directory.  
    Should be something like ../../reva/schematics with just the rev 
    letter changed. """
schpath = '../../implement/schematics'

# The kit number (should just be an integer)
kitnum = 11

# The kit quantity (how many boards do you want to build)
kitqty = 3

# List of part descriptions
descfile = '../purchasing/descriptions.dat'

# --------------------------End of configuration------------------------

schpath = os.path.abspath(schpath)
kitdir = schpath + '/kit' + str(kitnum)
sumfile = ('kit' + str(kitnum) + '_summary.dat')
sumpath = (kitdir + "/" + sumfile)
bomname = 'gnet.bom'

# Create the full vendor file list including path
def makevens():
    global venfiles
    venfiles = []
    for vendor in venlist:
        venfiles.append(venpath + '/' + vendor + '.dat')
    return venfiles

# Make a directory to store the kit information
def makekitdir():
    if (not os.access(kitdir,os.F_OK)):
        os.mkdir(kitdir)
        print ('* Created ' + kitdir)
    else:
        print('* ' + kitdir + " already exists.  I'll overwrite it.")
    return kitdir

# donread -- Tests whether or not we should read a line from a file
# True -- Line should be skipped
def donread(line):
    test = (line == '') or (line.startswith('#'))
    return test

# Create an attribs file for gnetlist to read
def makeattribs():
    fat = open('attribs','w')
    fat.write('device' + '\n')
    fat.write('value' + '\n')
    fat.write('part' + '\n')
    fat.write('footprint' + '\n')
    

""" Create a dictionary of JPart:quantity for parts found in the 
    schematic (or rather, in the BOM output from the schematic).

    This is coded to operate on the 'bom2' gnetlist output. """
def partcount():
    bomqty = {}
    makeattribs()
    # Generate BOM file with gnetlist
    print('-------------------Output from gnetlist-------------------')
    os.system('gnetlist -g bom2 ' + schpath + '/' + '*.sch ' + '-o ' +
         bomname)
    print('----------------------------------------------------------')
    fbm = open(bomname,'r')
    rawbom = fbm.read()
    for line in rawbom.split("\n")[1:-1]:
    # Split individual lines up based on colon
        if not donread(line):
            fields = line.split(":")
            # fields[3] is the JPart number.
            bomqty[fields[3]] = kitqty * len(fields[0].split(","))
    fbm.close()
    print('* Found ' + str(len(bomqty)) + ' unique parts in design.')
    return bomqty

# Create the kitx_fill.dat file
# This file will take numbers of parts already in the kit.
def makefill():
    bomqty = partcount()
    fillfile = ('kit' + str(kitnum) + '_fill.dat')
    descdict = partman.org2dict(descfile)
    fot = open(kitdir + '/' + fillfile,'w')
    fot.write('-*- mode: Org; mode: Auto-Revert; -*-' + '\n')
    fot.write('#+STARTUP: align' + '\n')
    fot.write('#' + '\n')
    fot.write('# Update the quantity of parts in the kit and run buygen.py'
        + '\n')
    fot.write('#' + '\n')
    fot.write('|-' + '\n')
    fot.write('|JRR part' + '|Needed' + '|In Kit' + '|Description|' +
        '\n')
    fot.write('| | | |<70>|' + '\n') # To set description column width
    fot.write('|-' + '\n')
    for part in bomqty:
        if part in descdict:
            fot.write('|' + part + '|' + str(bomqty[part]) + '| |' + descdict[part][0] + '|' + '\n')
            fot.write('|-' + '\n')
        else:
            fot.write('|' + part + '|' + str(bomqty[part]) + '| |' + 'No description' + '|' + '\n')
            fot.write('|-' + '\n')
    fot.write('|-')
    print('* Fill kit by editing ' + fillfile +
            ' with emacs.  Then run buygen.py' + '\n' +
            '  to see what needs to be ordered.')
    fot.close()
    partman.sortorg(kitdir + '/' + fillfile,0)

# buildbom()
# Writes out a bill of materials that can be used to assemble the
# circuit board.  The format should be:
# JRR part <whitespace> Ref1,Ref2,Ref3,... <whitespace> Part description
def buildbom():
    buildfile = ('kit' + str(kitnum) + '_build.bom')
    fob = open(kitdir + '/' + buildfile,'w')
    refdict = {} # Dictionary of JRR part: refdes list
    fbm = open(bomname,'r')
    rawbom = fbm.read()
    for line in rawbom.split('\n')[1:]:
        if not donread(line):
            fields = line.split(":")
            #fields[3] is the JRR part number.
            refdict[fields[3]] = fields[0]
    descdict = partman.org2dict(descfile) # Description dictionary
    fob.write('-*- mode: Org; mode: Auto-Revert; -*-' + '\n')
    fob.write('#+STARTUP: align' + '\n')
    fob.write('#' + '\n')
    fob.write('|-' + '\n')
    fob.write('|JRR part' + '|References' + '|Description|' + '\n')
    fob.write('| | |<70>|' + '\n') # To set description column width
    fob.write('|-' + '\n')
    for part in refdict:
        if part in descdict:
            fob.write('|' + part + '|' + str(refdict[part]) + '|' +
                descdict[part][0] + '|' + '\n')
            fob.write('|-' + '\n')
        else:
            fob.write('|' + part + '|' + str(refdict[part]) + '|' +
                'unknown' + '|' + '\n')
            fob.write('|-' + '\n')
    fbm.close()
    fob.close()
    partman.sortorg(kitdir + '/' + buildfile,0)
    partman.texbuild(kitdir + '/' + buildfile)
    print('* Assembly BOM written to ' + buildfile + ' and ' +
        buildfile.split('.')[0] + ".tex. Execute 'latex " + '\n' +
        '  '  + buildfile.split('.')[0] + ".tex' " +
        'to process .tex file.')


def main():
    partman.sortorg(descfile,1) # Sort the description file
    kitdir = makekitdir() # Make the kit directory
    makefill() # Make the fill file -- update this and run buygen
    buildbom() # Create the bom used to stuff the board
    if os.path.isfile(sumpath): # Remove the summary file if it exists
        print('* Removing existing ' + sumpath)
        os.remove(sumpath)
    os.system('emacs ' + kitdir + '/kit' + str(kitnum) + '_fill.dat &')

if __name__ == "__main__":
    main()
