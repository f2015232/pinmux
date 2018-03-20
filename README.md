# PinMux Tool

This tools currently generates a BSV code which implements the pin-muxing logic between peripheral ports. 

Currently the code supports the following peripherals:
1. UART (simple RX/TX type)
2. SPI (single spi)

#### TODO:
1. Add more peripheral definitions (only IO information required).
2. Fix a template to specify the user-defined muxing.
3. Provide support for dedicated pins.
4. Provide scheme to prevent short-circuit when inputs are mapped to multiple IOs.


## REQUIREMENTS:
	1. Python2 to generate BSV code.
	2. BSV compiler to generate verilog code from BSV code.

## Quick Start

Set parameters such as number of UARTs, SPIs, IO Cells, etc. in the file src/params.py . 

    $ make gen_pinmux

The above command will generate the bsv code (bsv_src/pinmux.bsv). This bsv code implements the pin-muxing logic as specified by the user (currently the pin-muxing logic is not implemented completely)

    $ make gen_verilog
The above command can be used to generate the verilog from the bsv file. It requires the presence of a BSV compiler. (see:[Bluespec](https://www.bluespec.com))    


    $make
The above command will execute both: gen_pinmux and gen_verilog .

## Steps to Add peripheral interfaces to PinMux

1.	Create interface declaration for the peripheral to be added. Remember these are interfaces defined for the pinmux and hence will be opposite to those defined at the peripheral. For eg. the output TX from the UART will be input (method Action) for the pinmux. These changes will have to be done in src/interface_decl.py
2. Define the wires that will be required to transfer data from the peripheral interface to the IO cell and vice-versa. Create a mkDWire for each input/output between the the peripheral and the pinmux. Also create an implicit wire of GenericIOType	for each cell that can be connected to a each bit from the peripheral. These changes will have to be done in src/wire_def.py
3. Create the definitions for each of the methods defined in Step-1. Use the wires from Step-2 to transfer data to/from each method. These changes will have to be done in src/interface_decl.py
