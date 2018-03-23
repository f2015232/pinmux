# ================================== Steps to add peripherals ============
# Step-1:   create interface declaration for the peripheral to be added.
#           Remember these are interfaces defined for the pinmux and hence
#           will be opposite to those defined at the peripheral.
#           For eg. the output TX from the UART will be input (method Action)
#           for the pinmux.
#           These changes will have to be done in interface_decl.py
# Step-2    define the wires that will be required to transfer data from the
#           peripheral interface to the IO cell and vice-versa. Create a
#           mkDWire for each input/output between the peripheral and the
#           pinmux. Also create an implicit wire of GenericIOType for each cell
#           that can be connected to a each bit from the peripheral.
#           These changes will have to be done in wire_def.py
# Step-3:   create the definitions for each of the methods defined above.
#           These changes will have to be done in interface_decl.py
# ========================================================================

# default module imports
import getopt
import os.path
import sys

from bsv.pinmux_generator import pinmuxgen as bsvgen


def printhelp():
    print ('''pinmux_generator.py [-o outputdir] [-v|--validate] [-h|--help]
                                  [-t outputtype]
    -t | outputtype : outputtype, defaults to bsv
    -o outputdir    : defaults to bsv_src.  also location for reading pinmux.txt
                      interfaces.txt and *.txt
    -v | --validate : runs some validation on the pinmux
    -h | --help     : this help message
''')


if __name__ == '__main__':
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'o:vht:',
            ['output=',
             'validate',
             'outputtype=',
             'help',
             'version=',
             ])
    except getopt.GetoptError as err:
        print "ERROR: %s" % str(err)
        printhelp()
        sys.exit(1)

    output_type = 'bsv'
    output_dir = None
    validate = False
    for opt, arg in options:
        if opt in ('-o', '--output'):
            output_dir = arg
        elif opt in ('-t', '--outputtype'):
            output_type = arg
        elif opt in ('-v', '--validate'):
            validate = True
        elif opt in ('-h', '--help'):
            printhelp()
            sys.exit(0)

    gentypes = {'bsv': bsvgen}
    if not gentypes.has_key(output_type):
        print "ERROR: output type '%s' does not exist" % output_type
        printhelp()
        sys.exit(0)
    gentypes[output_type](output_dir, validate)
