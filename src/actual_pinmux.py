from parse import *
from string import digits


# dictionary of properties of signals that are supported.
dictionary = {
    "uart_rx"	: "input",
    "uart_tx"	: "output",
    "spi_sclk"	: "output",
    "spi_mosi"	: "output",
    "spi_ss"	: "output",
    "spi_miso"	: "input",
    "twi_sda"	: "inout",
    "twi_scl"	: "inout"
}


# ============== common bsv templates ============ #
# first argument is the io-cell number being assigned.
# second argument is the mux value.
# Third argument is the signal from the pinmap file
mux_wire = '''
      rule assign_{2}_on_cell{0}(wrmux{0}=={1});
        {2}<=cell{0}_in;
      endrule
'''
dedicated_wire = '''
      rule assign_{1}_on_cell{0};
        {1}<=cell{0}_in;
      endrule
'''
# ============================================================
pinmux = ''' '''
digits = str.maketrans(dict.fromkeys('0123456789'))

for cell in muxed_cells:
    pinmux = pinmux + "      cell" + str(cell[0]) + "_out="
    i = 0
    while(i < len(cell) - 1):
        pinmux = pinmux + "wrmux" + \
            str(cell[0]) + "==" + str(i) + "?" + cell[i + 1] + "_io:"
        if(i + 2 == len(cell) - 1):
            pinmux = pinmux + cell[i + 2] + "_io"
            i = i + 2
        else:
            i = i + 1
    pinmux = pinmux + ";\n"
    # ======================================================== #

    # check each cell if "peripheral input/inout" then assign its wire
    # Here we check the direction of each signal in the dictionary.
    # We choose to keep the dictionary within the code and not user-input
    # since the interfaces are always standard and cannot change from
    # user-to-user. Plus this also reduces human-error as well :)
    for i in range(0, len(cell) - 1):
        temp = cell[i + 1].translate(digits)
        x = dictionary.get(temp)
        if(x is None):
            print(
              "Error: The signal : " +
              str(cell[i + 1]) +
              " in lineno: " +
              str(lineno) + "of pinmap.txt isn't present in the \
              current dictionary.\nUpdate dictionary or fix-typo.")
            exit(1)
        if(x == "input"):
            pinmux = pinmux + \
              mux_wire.format(cell[0], i, "wr" + cell[i + 1]) + "\n"
        elif(x == "inout"):
            pinmux = pinmux + \
                mux_wire.format(cell[0], i, "wr" + cell[i + 1] +
                                            "_in") + "\n"
# ============================================================ #

# ==================  Logic for dedicated pins ========= #
for cell in dedicated_cells:
    pinmux = pinmux + "      cell" + \
        str(cell[0]) + "_out=" + cell[1] + "_io;\n"
    temp = cell[1].translate(digits)
    x = dictionary.get(temp)
    if(x == "input"):
        pinmux = pinmux + \
            dedicated_wire.format(cell[0], "wr" + cell[1]) + "\n"
    elif(x == "inout"):
        pinmux = pinmux + \
            dedicated_wire.format(cell[0], "wr" + cell[1] + "_in") + "\n"
# =======================================================#
