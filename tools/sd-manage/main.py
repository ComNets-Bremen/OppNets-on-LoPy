# A simple tool to manage files in the an SD card connected to a LoPy. The
# operations are,
#
# l - list the contents of the /sd folder
# d - remove a given file
# r - show the contents of a file (assumes a text file)
#
# @author: Asanga Udugama (adu@comnets.uni-bremen.de)
# @date: 16-jun-2020
#
import machine
import os
import sys

# init
sd_present = False

# say tool name
print('SD Card Operations')

# mount SD
try:
    sd = machine.SD()
    os.mount(sd, '/sd')
    sd_present = True
except:
    print('no SD card')

# endless loop
while sd_present:

    # get operation
    print('Operations List:')
    print('  x - Exit')
    print('  l - List folder /sd')
    print('  d - Remove given file')
    print('  r - Dump file contents')
    op = input('Enter Operation: ')

    # exit if x
    if op == 'x':
        break

    # list folder contents
    elif op == 'l':
        filelist = os.listdir('/sd')
        for name in filelist:
            print(name)

    # remove given file
    elif op == 'd':
        filename = input('File to delete: ')
        try:
            os.remove(filename)
        except:
            print(filename, 'not found')

    # list contents of selected file (assumes a text file)
    elif op == 'r':
        filename = input('File to dump: ')
        try:
            with open(filename, mode='r') as lfp:
                for line in lfp:
                    print(line, end='')
        except:
            print(filename, 'not found')

    # wrong operation
    else:
        print('Invalid operation. Try again')
