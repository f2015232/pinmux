from string import digits
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans


# dictionary of properties of signals that are supported.
dictionary = {
    "uart_rx"	: "input",
    "uart_tx"	: "output",
    "spi_sclk"	: "output",
    "spi_mosi"	: "output",
    "spi_ss"	: "output",
    "spi_miso"	: "input",
    "twi_sda"	: "inout",
    "twi_scl"	: "inout",
    "sd_clk": "output",
    "sd_cmd": "output",
    "sd_d": "inout",
    "pwm_pwm": "output"
}


# ============== common bsv templates ============ #
# first argument is the io-cell number being assigned.
# second argument is the mux value.
# Third argument is the signal from the pinmap file
mux_wire = '''
      rule assign_{2}_on_cell{0}(wrcell{0}_mux=={1});
        {2}<=cell{0}_mux_in;
      endrule
'''
dedicated_wire = '''
      rule assign_{1}_on_cell{0};
        {1}<=cell{0}_mux_in;
      endrule
'''
# ============================================================
digits = maketrans('0123456789', ' '*10)  # delete space later


def cn(idx):
    return "cell%s_mux" % str(idx)


def init(p):
    p.pinmux = ' '
    global dedicated_wire
    for cell in p.muxed_cells:
        p.pinmux += "      %s_out=" % cn(cell[0])
        i = 0
        while(i < len(cell) - 1):
            p.pinmux += "wr%s" % cn(cell[0]) + \
                "==" + str(i) + "?" + cell[i + 1] + "_io:\n\t\t\t"
            if(i + 2 == len(cell) - 1):
                p.pinmux += cell[i + 2] + "_io"
                i = i + 2
            else:
                i = i + 1
        p.pinmux += ";\n"
        # ======================================================== #

        # check each cell if "peripheral input/inout" then assign its wire
        # Here we check the direction of each signal in the dictionary.
        # We choose to keep the dictionary within the code and not user-input
        # since the interfaces are always standard and cannot change from
        # user-to-user. Plus this also reduces human-error as well :)
        for i in range(0, len(cell) - 1):
            temp = cell[i + 1].translate(digits)
            temp = temp.replace(' ', '')
            x = dictionary.get(temp)
            if(x is None):
                print(
                    "ERROR: The signal : " +
                    str(cell[i + 1]) +
                    " of pinmap.txt isn't present in the current dictionary.\
                  \nUpdate dictionary or fix-typo.")
                exit(1)
            if(x == "input"):
                p.pinmux += \
                    mux_wire.format(cell[0], i, "wr" + cell[i + 1]) + "\n"
            elif(x == "inout"):
                p.pinmux += \
                    mux_wire.format(cell[0], i, "wr" + cell[i + 1] +
                                                "_in") + "\n"
    # ============================================================ #

    # ==================  Logic for dedicated pins ========= #
    for cell in p.dedicated_cells:
        p.pinmux += "      %s" % cn(cell[0]) + \
            "_out=" + cell[1] + "_io;\n"
        temp = cell[1].translate(digits)
        x = dictionary.get(temp)
        if(x == "input"):
            pinmux = pinmux + \
                dedicated_wire.format(cell[0], "wr" + cell[1]) + "\n"
        elif(x == "inout"):
            pinmux = pinmux + \
                dedicated_wire.format(cell[0], "wr" + cell[1] + "_in") + "\n"
    # =======================================================#
