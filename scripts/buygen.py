# buygen.py
# Reads the file kitx_fill.dat and generates kitx_vendor.dat files
# to fill the shortages
import os
# The script will always refer to paths relative to where the kitgen.py
# script is actually located.
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import partman
import kitgen

#---------------------------Begin configuration-------------------------

# The relative path from the project/eda/scripts directory to the
# vendor and description files.  
# Should just be ../purchasing
venpath = '../purchasing'

# List of vendor names.  Vendor files will be these names plus ".dat"
venlist = ['digikey','mcmaster','newark','jameco','pololu','sierra']

# --------------------------End of configuration------------------------


# getshort()
# Reads the kitx_fill file to get a shortage list
# Returns a dictionary of JRR part:shortage
def getshort():
    shortdict = {}
    fillfile = ('kit' + str(kitgen.kitnum) + '_fill.dat')
    fillpath = kitgen.kitdir + '/' + fillfile
    rawdict = partman.org2dict(fillpath)
    for part in rawdict:
        try:
            inkit = int(rawdict[part][1])
        except:
            inkit = 0
        shortdict[part] = int(rawdict[part][0]) - inkit
    return shortdict

# needorder(vendor name)
# Goes through the shortage list and figures out if a vendor can source
# the part.
def needorder(venstr):
    venfile = venpath + '/' + venstr + '.dat'
    found = False
    if os.path.isfile(venfile):
        # Shortage list generated from the summary file
        shortdict = partman.org2dict(kitgen.sumpath)
        for part in shortdict:
            if (int(shortdict[part][0]) > 0) and (shortdict[part][1] == venstr):
                found = True
    else:
        print('Did not find file ' + venfile)
    return found


""" venreport(vendor name)
    Takes a vendor name (like from venlist) and creates an output report
    using the summary file to generate the shortage list. """
def venreport(venstr):
    outfile = ('kit' + str(kitgen.kitnum) + '_' + venstr + '.dat')
    venfile = venpath + '/' + venstr + '.dat'
    descdict = partman.org2dict(kitgen.descfile)
    if os.path.isfile(venfile):
        if needorder(venstr):
            fvo = open(kitgen.kitdir + '/' + outfile,'w')
            # Shortage list generated from the summary file
            shortdict = partman.org2dict(kitgen.sumpath)
            vdict = partman.org2dict(venfile)
            fvo.write('-*- mode: Org; mode: Auto-Revert; -*-' + '\n')
            fvo.write('#+STARTUP: align' + '\n')
            fvo.write('#' + '\n')
            fvo.write('#' + '\n')
            fvo.write('|-' + '\n')
            fvo.write('|JRR part' + '|' + venstr + ' part' +
                '|Quantity|' + '\n')
            fvo.write('|-' + '\n')
            count = 0
            for part in shortdict:
                if (shortdict[part][1] == venstr) and (int(shortdict[part][0]) > 0):
                    count += 1
                    fvo.write('|' + part + '|' + vdict[part][0] + '|' +
                        str(shortdict[part][0]) + '|' + '\n')
            fvo.write('|-' + '\n')
            print('Wrote ' + str(count) + ' parts to ' + outfile)
            fvo.close()
            partman.sortorg(kitgen.kitdir + '/' + outfile,0)
            partman.sortorg(venfile,1)
        else:
            print('No parts need to be ordered from ' + venstr)
    else:
        print('venreport: Did not find file ' + venfile)

""" sumreport(dict)
    Goes through each part in the dictionary with qty > 0 and reports:
    Part num | Quantity | Vendor | Remove | Description

    Adding a mark in the "Remove" column disqualifies buying that part
    from that vendor. """
def sumreport(shortdict):
    sumfile = ('kit' + str(kitgen.kitnum) + '_summary.dat')
    descdict = partman.org2dict(kitgen.descfile)
    fos = open(kitgen.kitdir + "/" + sumfile,'w')
    fos.write('-*- mode: Org; mode: Auto-Revert; -*-' + '\n')
    fos.write('#+STARTUP: align' + '\n')
    fos.write('# \n')
    fos.write('# Add an x anywhere in the "Remove" column \n')
    fos.write('# and save this file to disqualify a vendor \n')
    fos.write('# for a given part. \n')
    fos.write('|-' + '\n')
    fos.write('|JRR part' + '|Quantity' + '|Vendor' + '|Remove' +
              '|Description|' + '\n')
    fos.write('| | | | |<70>|' + '\n') # Set description column width
    fos.write('|-' + '\n')
    for part in shortdict:
        if (shortdict[part] > 0):
            foundit = False # Did we find the part in any vendor file?
            for vendor in venlist:
                venfile = venpath + '/' + vendor + '.dat'
                if part in partman.org2dict(venfile):
                    if part in descdict:
                        fos.write('|' + str(part) + '|' +
                        str(shortdict[part]) + '|' + vendor + '| |' + 
                            descdict[part][0] + '\n')
                    else:
                        fos.write('|' + str(part) + '|' + 
                        str(shortdict[part]) + '|' + vendor + '| |' + 
                            'No description' + '\n')
                    fos.write('|-' + '\n')
                    foundit = True
            if not foundit: # The part was not found in any vendor file.
                fos.write('|' + str(part) + '|' + str(shortdict[part]) +
                          '|' + 'None' + '|' +'\n')
                fos.write('|-' + '\n')
                print('Part ' + str(part) + ' was not found in any vendor file :-(')
    fos.close()
    partman.multisort(kitgen.sumpath,0)
    print('* Wrote summary to ' + sumfile)


# hasrepeat()
# Returns true if there are repeated part numbers in the summary file
def hasrepeat():
    fis = open(kitgen.sumpath,'r')
    rawfile = fis.read()
    partqty = {}
    repeats = False
    for line in rawfile.split('\n'):
        if partman.isorgdata(line):
            fields = line.split('|')
            if partman.isjrrpart(fields[1]): #fields[0] will be ''
                jrrpart = fields[1].strip()
                if jrrpart in partqty:
                    partqty[jrrpart] += 1
                    repeats = True
                    print('--fix--> Part ' + jrrpart + ' is repeated.')
                else:
                    partqty[jrrpart] = 1
    fis.close()
    return repeats

# rmchecked()
# Removes lines from the summary file if they have a mark in the "remove"
# column
def rmchecked():
    fin = open(kitgen.sumpath,'r')
    fot = open('junk.dat','w')
    rawfile = fin.read()
    for line in rawfile.split('\n'):
        if partman.iscom(line) or line.startswith('-*-'):
            fot.write(line + '\n') # Copy the first few comment lines
    fot.write('|-' + '\n')
    if len(partman.orgheader(kitgen.sumpath)[1]) == 0:
        for item in partman.orgheader(kitgen.sumpath)[0]: #Write the table header
            fot.write('|' + item)
        fot.write('|' + '\n')
        fot.write('|-' + '\n')
    else:
        for item in partman.orgheader(kitgen.sumpath)[0]: #Write the table header
            fot.write('|' + item)
        fot.write('|' + '\n')
        for item in partman.orgheader(kitgen.sumpath)[1]: #Write the table customizations
            fot.write('|' + item)
        fot.write('|' + '\n')
        fot.write('|-' + '\n')
    for line in rawfile.split('\n'):
        if partman.isorgdata(line):
            fields = line.split('|')
            if partman.isjrrpart(fields[1]) and len(fields[4].strip()) == 0:
            #fields[0] will be ''
                fot.write(line + '\n')
                fot.write('|-' + '\n')
    fot.close()
    fin.close()
    os.remove(kitgen.sumpath)
    os.rename('junk.dat',kitgen.sumpath)
    
""" venpaste(vendor name)
    Creates a file for cut-and-paste into a vendor's website """
def venpaste(venstr):
    outfile = ('kit' + str(kitgen.kitnum) + '_' + venstr + '.pst')
    venfile = ('kit' + str(kitgen.kitnum) + '_' + venstr + '.dat')
    descdict = partman.org2dict(kitgen.descfile)
    # The vendor file will only exist if there are parts in it to be ordered.
    if os.path.isfile(kitgen.kitdir + '/' + venfile):
        buydict = partman.org2dict(kitgen.kitdir + '/' + venfile)
        fot = open(kitgen.kitdir + '/' + outfile,'w')
        for part in buydict:
            """ Newark file format:
                Newark part <tab> Qty <tab> Comment """
            if (venstr == 'newark'):
                fot.write(buydict[part][0] + '\t' + buydict[part][1] + 
                          '\t' + part + ' ' + descdict[part][0] + '\n')
            """ Digikey file format:
                Quantity <tab> Digi-Key part number <tab> Customer reference """
            if (venstr == 'digikey'):
                fot.write(buydict[part][1] + '\t' + buydict[part][0] +
                          '\t' + part + ' ' + descdict[part][0] + '\n')
        print('--> Use ' + outfile + ' for cut and paste.')
        fot.close()

def main():
    """ If the summary file already exists, just check for duplicate
        vendors in it. If the summary file does not exist, this is the 
        first time buygen has been run.  Get the shortages from the 
        fill file."""
    if os.path.isfile(kitgen.sumpath):
        rmchecked()
        if hasrepeat(): # Check for repeated parts
            print('* Modify ' + kitgen.sumfile + ' to remove duplicated parts,')
            print('  then run buygen again.')
            os.system('emacs ' + kitgen.kitdir + '/kit' + str(kitgen.kitnum) +
                        '_summary.dat &')
        else:
            for vendor in venlist:
                venreport(vendor)
                venpaste(vendor)
    else:
        sumreport(getshort())
        if hasrepeat(): # Check for repeated parts
            print('* Modify ' + kitgen.sumfile + ' to remove duplicated parts, ')
            print('  then run buygen again.')
            os.system('emacs ' + kitgen.kitdir + '/kit' + str(kitgen.kitnum) +
                        '_summary.dat &')
        else:
            for vendor in venlist:
                venreport(vendor) 
                venpaste(vendor)


if __name__ == "__main__":
    main()
