# partman.py
# A set of part management modules
import os

# These scripts will always refer to paths relative to where this
# script is actually located.
os.chdir(os.path.dirname(os.path.realpath(__file__)))


# iscom -- Check to see if a line is commented out
# Usage: iscom(<complete line from a file>)
# Returns: True (for a line beginning with #) or False
# Example:
# iscom('#Some comment') returns True
def iscom(line):
    return line.startswith('#')


# sortparts(filename) -- Sort a file of Part <whitespace> attribute
# by part number.
# WARNING: Clobbers the old file
def sortparts(filename):
    rawdict = {}
    sortdict = {}
    if os.path.isfile(filename):
        fin = open(filename,'r')
        fot = open('junk.dat','w')
        rawfile = fin.read()
        for line in rawfile.split('\n'):
            if line != '' and not iscom(line):
                fields = line.split()
                jrrpn = fields[0]
                if len(fields) >= 3: # This will happen for description file
                    blurb = fields[1]
                    for item in fields[2:]:
                        blurb += ' ' + item
                    rawdict[jrrpn] = blurb
                else:
                    rawdict[jrrpn] = fields[1]
            elif iscom(line):
                fot.write(line + '\n') # Copy the first few comment lines
        sortlist = sorted(rawdict, key=lambda partnum:
            1e6 * int(partnum.split('-')[0]) +
            1 * int(partnum.split('-')[1]))
        for part in sortlist:
            fot.write(part + '\t\t\t' + rawdict[part] + '\n')
        fot.close()
        fin.close()
        os.remove(filename)
        os.rename('junk.dat',filename)
    else:
        print(filename + ' not found')

# part2org(filename) -- Convert a file of jrr part <whitespace> vendor part
#                       to work with org mode's table
# WARNING: Clobbers the old file
def part2org(filename):
    rawdict = {}
    if os.path.isfile(filename):
        fin = open(filename,'r')
        fot = open('junk.dat','w')
        fot.write('-*- mode: Org; mode: Auto-Revert; -*-' + '\n')
        fot.write('#+STARTUP: align' + '\n' + '\n')
        rawfile = fin.read()
        for line in rawfile.split('\n'):
            if line != '' and not iscom(line):
                fields = line.split()
                jrrpn = fields[0]
                if len(fields) >= 3: # This will happen for description file
                    blurb = fields[1]
                    for item in fields[2:]:
                        blurb += ' ' + item
                    rawdict[jrrpn] = blurb
                else:
                    rawdict[jrrpn] = fields[1]
            elif iscom(line):
                fot.write(line + '\n') # Copy the first few comment lines
        fot.write('|JRR part' + '|Vendor part|' + '\n')
        fot.write('|-' + '\n')
        for part in rawdict:
            fot.write('|' + str(part) + '|' + str(rawdict[part]) + '|' +'\n')
        fot.write('|' + '\n') # Extra line for adding additional parts
        fot.write('|-' + '\n')
        fot.write('# Add new parts at the bottom of the table.' + '\n')
        fot.write('# Use tabs to cycle through columns and to ' + '\n')
        fot.write('# move to next row.' + '\n')
        fin.close()
        fot.close()
        os.remove(filename)
        os.rename('junk.dat',filename)
    else:
        print(filename + ' not found')

# isorgdata(string)
# Takes a line from an org-mode table file and returns true if it's
# part of the table data lines
def isorgdata(line):
    nodatachars = ['#','-','|-']
    isdata = True
    for char in nodatachars:
        if line.startswith(char):
            isdata = False
    if len(line.split('|')) == 1:
        isdata = False
    return isdata

# isjrrpart(string)
# Takes a string and decides if it represents a jrr part
def isjrrpart(entry):
    ispart = True
    entryparts = entry.split('-')
    if len(entryparts) != 2:
        ispart = False
    else:
        for piece in entryparts:
            try:
                int(piece)
            except:
                ispart = False
    return ispart

# isblankrow(string)
# Returns true if a row in an org table is blank
def isblankrow(line):
    isblank = True
    fields = line.split('|')
    for field in fields:
        if field.strip() != '':
            isblank = False
    return isblank

""" org2dict(filename)
    Takes in a file containing an org-mode table with:
    Part number | something else | something more | 
    and returns a dictionary with part number keys and a list of values. """
def org2dict(filename):
    rawdict = {}
    if os.path.isfile(filename):
        fin = open(filename,'r')
        rawfile = fin.read()
        for line in rawfile.split('\n'):
            if isorgdata(line):
                fields = line.split('|')
                if isjrrpart(fields[1]): #fields[0] will be ''
                    jrrpart = fields[1].strip()
                    dictlist = []
                    for entry in fields[2:-1]:
                        dictlist.append(entry.strip())
                    rawdict[jrrpart] = dictlist
        fin.close()
    else:
        print(filename + ' not found')
    return rawdict

# orgheader(filename)
# Takes in a file containing an org-mode table with:
# JRR part | something else | something more |
# and returns a list of items in the header.  Always returns a two-item
# list: [list of header items, list of customization line below header]
# If there is no column customization, second list item will be empty
def orgheader(filename):
    if os.path.isfile(filename):
        fin = open(filename,'r')
        rawfile = fin.read()
        fin.close()
        found = False
        count = 0
        headlist = []
        custlist = []
        for line in rawfile.split('\n'):
            if isorgdata(line) and not isblankrow(line):
                fields = line.split('|')
                if not (isjrrpart(fields[1])) and (not found): #fields[0] will be ''
                    headlist = fields[1:-1]
                    headline = count
                    found = True
            count += 1
        if found: # We found a header
            nextline = rawfile.split('\n')[headline+1]
            if isorgdata(nextline) and not isblankrow(nextline):
                # We must have some column customizations
                fields = nextline.split('|')
                if not isjrrpart(fields[1]):
                    custlist = fields[1:-1]
        else:
            print('Table header not found in ' + filename)
            return('none')
    else:
        print(filename + ' not found')
    return([headlist,custlist])


""" sortorg(filename,blanknum)
    Reads in a table of org-mode data:
    Part number | something | something else
    ...and sorts it by part number.
    
    Inserts blanknum blank rows at the bottom to allow a user to add
    entries by hand.
    WARNING: clobbers the file with the sorted version. """
def sortorg(filename,blanknum):
    sortdict = {}
    if os.path.isfile(filename):
        rawdict = org2dict(filename)
        fin = open(filename,'r')
        fot = open('junk.dat','w')
        rawfile = fin.read()
        for line in rawfile.split('\n'):
            if iscom(line) or line.startswith('-*-'):
                fot.write(line + '\n') # Copy the first few comment lines
        fot.write('|-' + '\n')
        if len(orgheader(filename)[1]) == 0:
            for item in orgheader(filename)[0]: #Write the table header
                fot.write('|' + item)
            fot.write('|' + '\n')
            fot.write('|-' + '\n')
        else:
            for item in orgheader(filename)[0]: #Write the table header
                fot.write('|' + item)
            fot.write('|' + '\n')
            for item in orgheader(filename)[1]: #Write the table customizations
                fot.write('|' + item)
            fot.write('|' + '\n')
            fot.write('|-' + '\n')
        sortlist = sorted(rawdict, key=lambda partnum:
            1e6 * int(partnum.split('-')[0]) +
            1 * int(partnum.split('-')[1]))
        for part in sortlist:
            fot.write('|' + part)
            for item in rawdict[part]:
                fot.write('|' + item)
            fot.write('|' + '\n')
            fot.write('|-' + '\n')
        count = 0
        while (count < blanknum):
            fot.write('|' + '\n') # Extra lines for adding additional parts
            fot.write('|-' + '\n')
            count += 1
        fot.close()
        fin.close()
        os.remove(filename)
        os.rename('junk.dat',filename)
    else:
        print(filename + ' not found')

# org2table(filename)
# Reads in a table of org-mode data and writes it out to a LaTeX longtable.
def org2table(filename):
    if os.path.isfile(filename):
        fin = open(filename,'r')
        rawfile = fin.read()
        fullpath = os.path.realpath(filename)
        dirpath = os.path.split(fullpath)[0]
        endname = os.path.split(fullpath)[1]
        basename = endname.split('.')[0]
        numcol = len(orgheader(filename)[0])
        fot = open(dirpath + '/' + basename + '.tex','w') # Write back to the same place
        fot.write(r'\documentclass[letterpaper]{article}' + '\n')
        fot.write(r'\usepackage{longtable}' + '\n')
        fot.write(r'\usepackage[margin=0.5in]{geometry}' + '\n')
        fot.write(r'\begin{document}' + '\n')
        fot.write(r'\begin{center}' + '\n')
        fot.write(r'\begin{longtable}{')
        for item in orgheader(filename)[0]:
            fot.write('|c')
        fot.write('|}' + '\n')
        fot.write(r'\hline' + '\n')
        count = 1
        for item in orgheader(filename)[0]:
            if count < numcol:
                fot.write(item + '&')
            else:
                fot.write(item + r'\\' + '\n')
            count += 1
        fot.write(r'\hline' + '\n')
        fot.write(r'\endfirsthead' + '\n')
        fot.write(r'\hline' + '\n')
        fot.write(r'\multicolumn{' + str(numcol) + '}{c}{' + r'\small' +
            r'\slshape' + ' continued on next page}' + r'\\' + '\n')
        fot.write(r'\hline' + '\n')
        fot.write(r'\endfoot' + '\n')
        fot.write(r'\hline' + '\n')
        fot.write(r'\endlastfoot' + '\n')
        count = 1
        for line in rawfile.split('\n'):
            if isorgdata(line):
                fields = line.split('|')
                if isjrrpart(fields[1]): #fields[0] will be ''
                    count = 1
                    for field in fields[1:-1]:
                        if count < numcol:
                            fot.write(texsafe(field) + '&')
                        else:
                            fot.write(texsafe(field) + r'\\' + '\n')
                        count += 1
        fot.write(r'\end{longtable}' + '\n')
        fot.write(r'\end{center}' + '\n')
        fot.write(r'\end{document}')
        fot.close()
    else:
        print(filename + ' not found')

# texbuild(filename)
# Reads in a table of org-mode data for a building BOM, writes it out
# in a longtable.  Assumes the format part, refdes list, description
def texbuild(filename):
    if os.path.isfile(filename):
        fin = open(filename,'r')
        rawfile = fin.read()
        fullpath = os.path.realpath(filename)
        dirpath = os.path.split(fullpath)[0]
        endname = os.path.split(fullpath)[1]
        basename = endname.split('.')[0]
        numcol = len(orgheader(filename)[0])
        fot = open(dirpath + '/' + basename + '.tex','w') # Write back to the same place
        fot.write(r'\documentclass[letterpaper]{article}' + '\n')
        fot.write(r'\usepackage{longtable}' + '\n')
        fot.write(r'\usepackage[margin=0.5in]{geometry}' + '\n')
        fot.write(r'\usepackage{calc}' + '\n')
        fot.write(r'\begin{document}' + '\n')
        fot.write(r'\begin{center}' + '\n')
        fot.write(r'\textbf{Building BOM}' + '\n')
        fot.write(r'\begin{longtable}{|c|c|l|}' + '\n')
        fot.write(r'\hline' + '\n')
        count = 1
        for item in orgheader(filename)[0]:
            if count < numcol:
                fot.write(item + '&')
            else:
                fot.write(r'\multicolumn{1}{|c|}{' + item + '}' + r'\\' + '\n')
            count += 1
        fot.write(r'\hline' + '\n')
        fot.write(r'\endfirsthead' + '\n')
        fot.write(r'\multicolumn{' + str(numcol) + '}{c}{' + r'\small' +
            r'\slshape' + ' continued from previous page}' + r'\\' + '\n')
        fot.write(r'\hline' + '\n')
        count = 1
        for item in orgheader(filename)[0]:
            if count < numcol:
                fot.write(item + '&')
            else:
                fot.write(r'\multicolumn{1}{|c|}{' + item + '}' + r'\\' + '\n')
            count += 1
        fot.write(r'\hline' + '\n')
        fot.write(r'\endhead' + '\n')
        fot.write(r'\hline' + '\n')
        fot.write(r'\multicolumn{' + str(numcol) + '}{c}{' + r'\small' +
            r'\slshape' + ' continued on next page}' + r'\\' + '\n')
        fot.write(r'\endfoot' + '\n')
        fot.write(r'\hline' + '\n')
        fot.write(r'\endlastfoot' + '\n')
        count = 1
        for line in rawfile.split('\n'):
            if isorgdata(line):
                fields = line.split('|')
                if isjrrpart(fields[1]): #fields[0] will be ''
                    count = 1
                    for field in fields[1:-1]:
                        if count == 1:
                            fot.write(texsafe(field) + '&')
                        elif count == 2:
                            fot.write(r'\parbox[c][\height + 0.5cm]{5cm}{' +
                                r'\centering ' + texsafe(field) + '}' + '&')
                        else:
                            fot.write(r'\parbox[c][\height + 0.5cm]{7cm}{' +
                                texsafe(field) + '}' + r'\\' + '\n')
                            fot.write(r'\hline' + '\n')
                        count += 1

        fot.write(r'\end{longtable}' + '\n')
        fot.write(r'\end{center}' + '\n')
        fot.write(r'\end{document}')
        fot.close()
    else:
        print(filename + ' not found')


# texsafe(string)
# Takes in a string and replaces certain characters
def texsafe(string):
    retstring = string.replace('%','\\%')
    retstring = retstring.replace(',',', ')
    return(retstring)

""" multisort(filename, blanknum)
    Sorts a table of org-mode data that may have repeated part numbers.
    Inserts blanknum blank rows at the bottom. 
    * Preserves comment lines at the top and the table headers. 
    * Use this function for general-purpose org-file sorting. """
def multisort(filename,blanknum):
    sortdict = {}
    if os.path.isfile(filename):
        rawdict = org2dict(filename)
        fin = open(filename,'r')
        fot = open('junk.dat','w')
        rawfile = fin.read()
        for line in rawfile.split('\n'):
            if iscom(line) or line.startswith('-*-'):
                fot.write(line + '\n') # Copy the first few comment lines
        fot.write('|-' + '\n')
        if len(orgheader(filename)[1]) == 0:
            for item in orgheader(filename)[0]: #Write the table header
                fot.write('|' + item)
            fot.write('|' + '\n')
            fot.write('|-' + '\n')
        else:
            for item in orgheader(filename)[0]: #Write the table header
                fot.write('|' + item)
            fot.write('|' + '\n')
            for item in orgheader(filename)[1]: #Write the table customizations
                fot.write('|' + item)
            fot.write('|' + '\n')
            fot.write('|-' + '\n')
        sortlist = sorted(rawdict, key=lambda partnum:
            1e6 * int(partnum.split('-')[0]) +
            1 * int(partnum.split('-')[1]))
        for part in sortlist:
            for line in rawfile.split('\n'):
                if isorgdata(line):
                    fields = line.split('|')
                    if isjrrpart(fields[1]): #fields[0] will be ''
                        jrrpart = fields[1].strip()
                        if jrrpart == part:
                            fot.write(line + '\n')
                            fot.write('|-' + '\n')
        count = 0
        while (count < blanknum):
            fot.write('|' + '\n') # Extra lines for adding additional parts
            fot.write('|-' + '\n')
            count += 1
        fot.close()
        fin.close()
        os.remove(filename)
        os.rename('junk.dat',filename)
    else:
        print(filename + ' not found')
        
        
# tasklist()
# Writes out a task list for use with emacs org-mode
def tasklist():
    taskfile = ('kit' + str(kitnum) + '_tasks.org')
    fot = open(kitdir + '/' + taskfile,'w')
    fot.write('-*- mode: Org; mode: Auto-Revert; -*-' + '\n')
    fot.write('#+TODO: vendor unordered | ordered inkit' + '\n')
    desdict = ven2dict(descfile)
    for part in bomqty:
        if part in desdict:
            fot.write('* vendor ' + desdict[part] + '\n')
            fot.write('** JRR part ' + part + '\n')
            fot.write('** Quantity ' + str(bomqty[part]) + '\n')
        else:
            fot.write('* vendor ' + part + '\n')
            fot.write('** Quantity ' + str(bomqty[part]) + '\n')
    print('Wrote task list to ' + taskfile)
    fot.close()
    
# ven2dict(filename base)
# Reads a file of jrr part <whitespace> whatever
# Returns a dictionary of jrrpart:whatever
def ven2dict(venstr):
    vdict = {}
    fvi = open(venpath + '/' + venstr + '.dat')
    rawdi = fvi.read()
    for line in rawdi.split('\n'):
        if not donread(line):
            fields = line.split()
            if len(fields) == 2:
                vdict[fields[0]] = fields[1]
            elif len(fields) == 1:
                vdict[fields[0]] = 'unknown'
            else:
                keyval = ''
                for field in fields[1:]:
                    keyval += field + ' '
                keyval = keyval.rstrip()
                vdict[fields[0]] = keyval
    fvi.close()
    return vdict
