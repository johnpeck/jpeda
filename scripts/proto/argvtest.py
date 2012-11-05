# argvtest.py
# Tests accepting arguments via stdin
import sys # provides sys.argv -- the list of command-line arguments
           # passed to the interpreter.

if (len(sys.argv) == 1):
    print('Usage')
    sys.exit()
else:
    print ('You passed me the string %s' % sys.argv[1])

print 'And...moving on'
