def mkmux(p, ifaces, cell, suffix, outenmode):
    comment = 'outen' if outenmode else 'output'
    fmtstr = "\t\t\twr%s==%d?%s:%s\n"  # mux-selector format
    ret = ''
    ret += "      // %s muxer for cell idx %s\n" % (comment, cell[0])
    #line1
    ret += "      %s%s=\n" % (cn(cell[0]), suffix) # line2
    for i in range(
            0, (1 << p.cell_bitwidth) - 1):  # full mux range (minus 1)
        comment = mkcomment(ifaces, cell, i, outenmode)
        cf = fmt(ifaces, cell, i, suffix)
        ret += fmtstr % (cn(cell[0]), i, cf, comment) # complete line
    comment = mkcomment(ifaces, cell, i + 1, outenmode) # comment for last line
    ret += "\t\t\t" + fmt(ifaces, cell, i + 1, suffix) # last line
    ret += ";%s\n" % comment

    return ret

    mkmux(p, ifaces, cell, '_out', False)
    # cell is a line of pinmap.txt
    # ifaces is passed in pinmux_generator .. and it
    # returns 'input', 'out' or 'inout' via ifaces.getifacetype(nameof_Funciton)

def fmt(ifaces, cell, idx, suffix=None):
    idx += 1
    if idx < len(cell):
        cell = cell[idx]
    else:
        cell = '' # when blank entries of deficit cell length
    if not cell:
        return '0'
    temp = transfn(cell)
    x = ifaces.getifacetype(temp)
    if x == 'input':
        return '0' # inputs don't get passed through to the out mux
    if suffix == '_outen' and x == 'out':
        return '1' #port behaves as output when _outen
    return "wr%s%s" % (cell, suffix or '')
def mkcomment(ifaces, cell, idx, outenmode=False):
    """ returns a comment string for the cell when muxed
    """
    idx += 1 #here idx ranges from 0 to (1 << p.cell_bitwidth) - 1)
    if idx >= len(cell):
        return ' // unused'
    cname = cell[idx]
    if not cname:
        return ' // unused'
    temp = transfn(cname)
    x = ifaces.getifacetype(temp)
    print (cname, x)
    if x == 'input':
        return ' // %s is an input' % cname
    if outenmode and x == 'inout':
        return ' // bi-directional'
    if outenmode and x == 'out':
        return ' // %s is an output' % cname

    return ""


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

    rule assign_wrtwi0_sda_in_on_cell2(wrcell2_mux==0);
        wrtwi0_sda_in<=cell2_mux_in;
      endrule

      Yo quería arreglar el error
