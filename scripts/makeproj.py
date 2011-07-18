# makeproj.py
# Automates the construction of a project in a filesytem
#
import os
import subprocess

#################### Begin project definition ##########################

# The name of the project to be made
projname = 'teensy'

# The project directory in my home directory
projdir = '/home/john/projects'

# The revcode (like a, b, 1, 2).  Note that you can just change this and
# run the script again to create a new rev.
revcode = 'a'

#################### End project definition ############################


# Make the top level of the project...if it hasn't been made already
def maketop():
    if os.access(projdir + '/' + projname,os.F_OK):
        print('Project directory already exists.')
    else:
        print('Creating ' + projdir + '/' + projname + '.')
        os.mkdir(projdir + '/' + projname)

# Make the datasheets subdirectory below the top level
def makesheets():
    dirname = 'datasheets'
    fullpath = (projdir + '/' + projname + '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print('Datasheet directory already exists.')
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)

# Make the notes subdirectory below the top level
def topnotes():
    dirname = 'notes'
    fullpath = (projdir + '/' + projname + '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print('Notes directory already exists.')
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)

# Create the top progress file
def progress():
    fullpath = (projdir + '/' + projname + '/' + 'progress.org')
    if os.access(fullpath,os.F_OK):
        print('Progress file already exists.')
    else:
        print('Creating ' + fullpath + '.')
        fid = open(fullpath,'w')
        fid.close()

# Make the revision directory
def makerev():
    dirname = 'rev' + revcode
    fullpath = (projdir + '/' + projname + '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print('Revision ' + revcode + ' directory already exists.')
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make the revision's data directory
def revdata():
    dirname = 'data'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' data directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make the revision's drawings directory
def revdraw():
    dirname = 'drawings'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' drawings directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make the revision's schematics directory
def revschem():
    dirname = 'schematics'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' schematics directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make the revision's layout directory
def revlay():
    dirname = 'layout'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' layout directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make the revision's pictures directory
def revpics():
    dirname = 'pictures'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' pictures directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make the revision's howto directory
def revhow():
    dirname = 'howto'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' howto directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Make a directory for the embedded code used in a project's revision
def revemcode():
    dirname = 'code'
    fullpath = (projdir + '/' + projname + '/' + 'rev' + revcode +
        '/' + dirname)
    if os.access(fullpath,os.F_OK):
        print("Revision '" + revcode +
            "' code directory already exists.")
    else:
        print('Creating ' + fullpath + '.')
        os.mkdir(fullpath)
        if isversion(projdir + '/' + projname):
            retval = subprocess.call(['svn','add',fullpath])



# Check to see if a directory is under version control
def isversion(fullpath):
    retval = subprocess.call(['svn','info',fullpath]) # 0 if working copy
    if retval == 1:
        return(False)
    else:
        return(True)



# Import the created project and check out a working copy -- if the
# project is not already under version control.
def svnimport():
    fullpath = (projdir + '/' + projname)
    if isversion(fullpath):
        return
    else:
        retval = subprocess.call(['svn','import',fullpath,
            'svn://www.jrranalytics.com/projects/'+projname,
            '-m','Initial import'])
        os.rename(fullpath,fullpath + '_nosvn')
        retval = subprocess.call(['svn','checkout',
            'svn://www.jrranalytics.com/projects/'+projname,
            fullpath])


# Add the externals definitions
def svnextern():
    fullpath = (projdir + '/' + projname)
    os.chdir(fullpath) # Change into the project directory
    fid = open('externlist','w') # Make a file to contain extern defs
    fid.write('eda svn://www.jrranalytics.com/eda' + '\n')
    fid.write('eda/notes/geda/doctools svn://www.jrranalytics.com/doctools' + '\n')
    fid.write('eda/notes/avr/doctools svn://www.jrranalytics.com/doctools' + '\n')
    fid.write('notes/doctools svn://www.jrranalytics.com/doctools' + '\n')
    fid.write('rev' + revcode +
        '/howto/doctools svn://www.jrranalytics.com/doctools' + '\n')
    fid.close()
    retval = subprocess.call(['svn','propset','svn:externals','-F',
        'externlist','.'])

# Deleting a project from the repository
# svn delete -m "Deleting project dir" svn://www.jrranalytics.com/projects/junkproj

def main():
    if os.access(projdir,os.W_OK):
        maketop()
        makesheets()
        topnotes()
        progress()
        makerev()
        revdata()
        revdraw()
        revschem()
        revlay()
        revpics()
        revhow()
        revemcode()
        svnimport()
        svnextern()
        retval = subprocess.call(['svn','update',projdir + '/' + projname])
    else:
        print('Not able to write to the project directory.')

if __name__ == "__main__":
    main()
