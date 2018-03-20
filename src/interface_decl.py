
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
                 action=False):
        self.name = name
        self.ready = ready
        self.enabled = enabled
        self.io = io
        self.action = action

    def __str__(self):
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
        if self.action:
            res += " Action "
            res += self.name
            res += ' (Bit#(1) in)'
        else:
            res += " Bit#(1) "
            res += self.name
        res += ";"
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

    def __str__(self):
        return '\n'+'\n'.join(map(str, self.pins))

    def format(self, i):
        return str(self).format(i)

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

# ========= Interface declarations ================ #

mux_interface = '''
      method Action cell{0}_mux(Bit#({1}) in);'''

io_interface = Interface([{'name': 'io_outputval_{0}', 'enabled': False},
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
