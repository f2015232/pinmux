from string import digits
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans


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
digits = maketrans('0123456789', ' ' * 10)  # delete space later


def cn(idx):  # idx is an integer
    return "cell%s_mux" % str(idx)


def transfn(temp):
    """ removes the number from the string of signal name.
    """
    temp = temp.split('_')
    if len(temp) == 2:
        temp[0] = temp[0].translate(digits)
        temp[0] = temp[0] .replace(' ', '')
    return '_'.join(temp)

def fmt(ifaces, cell):
    """ blank entries need to output a 0 to the pin (it could just as
        well be a 1 but we choose 0).  reason: blank entries in
        the pinmap.txt file indicate that there's nothing to choose
        from.  however the user may still set the muxer to that value,
        and rather than throw an exception we choose to output... zero.
    """
    empty = '0' # XXX TODO: fix this, as it's assigned to GenericIOType
    if not cell:
        return empty
    # work out the type.  if it's an input, return empty
    temp = cell[1].translate(digits)
    x = ifaces.getifacetype(temp)
    if x == 'input':
        return empty
    return "%s_io" % cell

def init(p, ifaces):
    """ generates the actual output pinmux for each io-cell.  blank lines
        need to output "0" to the iopad, if there is no entry in
        that column.
    """
    p.pinmux = ' '
    global dedicated_wire
    for cell in p.muxed_cells:
        p.pinmux += "      // output muxer for cell idx %s\n" % cell[0]
        p.pinmux += "      %s_out=" % cn(cell[0])
        for i in range(0, len(cell) - 2):
            p.pinmux += "wr%s" % cn(cell[0]) + \
                "==" + str(i) + "?" + fmt(ifaces, cell[i + 1]) + ":\n\t\t\t"
        p.pinmux += fmt(ifaces, cell[i + 2])
        p.pinmux += ";\n"
        # ======================================================== #

        # check each cell if "peripheral input/inout" then assign its wire
        # Here we check the direction of each signal in the dictionary.
        # We choose to keep the dictionary within the code and not user-input
        # since the interfaces are always standard and cannot change from
        # user-to-user. Plus this also reduces human-error as well :)
        for i in range(0, len(cell) - 1):
            cname = cell[i + 1]
            if not cname: # skip blank entries, no need to test
                continue
            temp = transfn(cname)
            x = ifaces.getifacetype(temp)
            #print (cname, temp, x)
            assert x is not None, "ERROR: The signal : " + \
                str(cname) + \
                " of pinmap.txt isn't present \nin the current" + \
                " dictionary. Update dictionary or fix-typo."
            if x == "input":
                p.pinmux += \
                    mux_wire.format(cell[0], i, "wr" + cname) + "\n"
            elif x == "inout":
                p.pinmux += \
                    mux_wire.format(cell[0], i, "wr" + cname +
                                                "_in") + "\n"
    # ============================================================ #

    # ==================  Logic for dedicated pins ========= #
    for cell in p.dedicated_cells:
        p.pinmux += "      %s_out=%s_io;\n" % (cn(cell[0]), cell[1])
        temp = cell[1].translate(digits)
        x = ifaces.getifacetype(temp)
        if x == "input":
            pinmux = pinmux + \
                dedicated_wire.format(cell[0], "wr" + cell[1]) + "\n"
        elif x == "inout":
            pinmux = pinmux + \
                dedicated_wire.format(cell[0], "wr" + cell[1] + "_in") + "\n"
    # =======================================================#
