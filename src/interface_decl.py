
class Pin(object):
    """ pin interface declaration.
        * name is the name of the pin
        * ready, enabled and io all create a (* .... *) prefix
        * action changes it to an "in" if true
    """

    def __init__(self, name,
                 ready=True,
                 enabled=True,
                 io=False,
                 action=False,
                 bitspec=None):
        self.name = name
        self.ready = ready
        self.enabled = enabled
        self.io = io
        self.action = action
        self.bitspec = bitspec if bitspec else '1'

    def ifacefmt(self, fmtfn=None):
        res = '    '
        status = []
        if self.ready:
            status.append('always_ready')
        if self.enabled:
            status.append('always_enabled')
        if self.io:
            status.append('result="io"')
        if status:
            res += '(*'
            res += ','.join(status)
            res += '*)'
        res += " method "
        if self.io:
            res += "\n                      "
        name = fmtfn(self.name)
        if self.action:
            res += " Action "
            res += name
            res += ' (Bit#(%s) in)' % self.bitspec
        else:
            res += " Bit#(%s) " % self.bitspec
            res += name
        res += ";"
        return res

    def ifacedef(self, fmtoutfn=None, fmtinfn=None, fmtdecfn=None):
        res = '      method '
        if self.action:
            fmtname = fmtinfn(self.name)
            res += "Action  "
            res += fmtdecfn(self.name)
            res += '(Bit#(%s) in);\n' % self.bitspec
            res += '         %s<=in;\n' % fmtname
            res += '      endmethod'
        else:
            fmtname = fmtoutfn(self.name)
            res += "%s=%s;" % (self.name, fmtname)
        return res


class Interface(object):
    """ create an interface from a list of pinspecs.
        each pinspec is a dictionary, see Pin class arguments
    """

    def __init__(self, pinspecs):
        self.pins = []
        for p in pinspecs:
            if p.get('outen') is True:  # special case, generate 3 pins
                _p = {}
                _p.update(p)
                del _p['outen']
                for psuffix in ['out', 'outen', 'in']:
                    _p['name'] = "%s_%s" % (p['name'], psuffix)
                    _p['action'] = psuffix != 'in'
                    self.pins.append(Pin(**_p))
            else:
                self.pins.append(Pin(**p))

    def ifacefmt(self, *args):
        res = '\n'.join(map(self.ifacefmtdecpin, self.pins)).format(*args)
        return '\n' + res

    def ifacefmtdecfn(self, name):
        return name

    def ifacefmtdecfn2(self, name):
        return name

    def ifacefmtoutfn(self, name):
        return name

    def ifacefmtinfn(self, name):
        return "wr%s" % name

    def ifacefmtdecpin(self, pin):
        return pin.ifacefmt(self.ifacefmtdecfn)

    def ifacefmtpin(self, pin):
        return pin.ifacedef(self.ifacefmtoutfn, self.ifacefmtinfn,
                            self.ifacefmtdecfn2)

    def ifacedef(self, *args):
        res = '\n'.join(map(self.ifacefmtpin, self.pins)).format(*args)
        return '\n' + res + '\n'


class MuxInterface(Interface):

    def ifacefmtdecfn2(self, name):
        return "cell{0}_mux"

    def ifacefmtdecfn(self, name):
        return "cell{0}_mux"

    def ifacefmtinfn(self, name):
        return "wrmux{0}"

class IOInterface(Interface):

    #def ifacefmtdecfn(self, name):
    #    return "cell{0}_mux"

    def ifacefmtoutfn(self, name):
        return "cell{0}_out.%s" % (name[3:-4])

    def ifacefmtinfn(self, name):
        return "cell{0}_in"


# ========= Interface declarations ================ #

mux_interface = MuxInterface([{'name': 'cell{0}', 'ready':False,
                      'enabled':False,
                     'bitspec': '{1}', 'action': True}])

io_interface = IOInterface([{'name': 'io_outputval_{0}', 'enabled': False},
                          {'name': 'io_output_en_{0}', 'enabled': False},
                          {'name': 'io_input_en_{0}', 'enabled': False},
                          {'name': 'io_pullup_en_{0}', 'enabled': False},
                          {'name': 'io_pulldown_en_{0}', 'enabled': False},
                          {'name': 'io_drivestrength_{0}', 'enabled': False},
                          {'name': 'io_pushpull_en_{0}', 'enabled': False},
                          {'name': 'io_opendrain_en_{0}', 'enabled': False},
                          {'name': 'io_inputval_{0}', 'action': True, 'io': True},
                          ])

# == Peripheral Interface definitions == #
# these are the interface of the peripherals to the pin mux
# Outputs from the peripherals will be inputs to the pinmux
# module. Hence the change in direction for most pins

uartinterface_decl = Interface([{'name': 'tx_{0}', 'action': True},
                                {'name': 'rx_{0}'},
                                ])

spiinterface_decl = Interface([{'name': 'sclk_{0}', 'action': True},
                               {'name': 'mosi_{0}', 'action': True},
                               {'name': 'ss_{0}', 'action': True},
                               {'name': 'miso_{0}'},
                               ])

twiinterface_decl = Interface([{'name': 'sda{0}', 'outen': True},
                               {'name': 'scl{0}', 'outen': True},
                               ])

sdinterface_decl = Interface([{'name': 'sd{0}_clk', 'action': True},
                              {'name': 'sd{0}_cmd', 'action': True},
                              {'name': 'sd{0}_d0', 'outen': True},
                              {'name': 'sd{0}_d1', 'outen': True},
                              {'name': 'sd{0}_d2', 'outen': True},
                              {'name': 'sd{0}_d3', 'outen': True}
                              ])

jtaginterface_decl = Interface([{'name': 'jtag{0}_tdi'},
                                {'name': 'jtag{0}_tms'},
                                {'name': 'jtag{0}_tclk'},
                                {'name': 'jtag{0}_trst'},
                                {'name': 'jtag{0}_tdo', 'action': True}])

pwminterface_decl = Interface([{'name': "pwm{0}", 'action': True}])

# ======================================= #

# basic test
if __name__ == '__main__':

    def _pinmunge(p, sep, repl, dedupe=True):
        """ munges the text so it's easier to compare.
            splits by separator, strips out blanks, re-joins.
        """
        p = p.strip()
        p = p.split(sep)
        if dedupe:
            p = filter(lambda x: x, p)  # filter out blanks
        return repl.join(p)

    def pinmunge(p):
        """ munges the text so it's easier to compare.
        """
        # first join lines by semicolons, strip out returns
        p = p.split(";")
        p = map(lambda x: x.replace('\n', ''), p)
        p = '\n'.join(p)
        # now split first by brackets, then spaces (deduping on spaces)
        p = _pinmunge(p, "(", " ( ", False)
        p = _pinmunge(p, ")", " ) ", False)
        p = _pinmunge(p, " ", " ")
        return p

    from interface_def import io_interface_def
    print io_interface_def.format(0)
    print io_interface.ifacedef(0)
    assert io_interface_def.format(0) == io_interface.ifacedef(0)

    mux_interfacetest = '''
          method Action cell{0}_mux(Bit#({1}) in);'''
    print pinmunge(mux_interfacetest.format(0,1))
    print pinmunge(mux_interface.ifacefmt(0, 1))
    from interface_def import mux_interface_def
    print repr(mux_interface_def.format(0, 1))
    print repr(mux_interface.ifacedef(0, 1))
    assert mux_interface_def.format(0,1) == mux_interface.ifacedef(0,1)

