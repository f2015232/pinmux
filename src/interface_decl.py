# ========= Interface declarations ================ #
mux_interface = '''
      method Action cell{0}_mux(Bit#({1}) in);'''

io_interface = '''
      (*always_ready*)   method   Bit#(1) io_outputval_{0};
      (*always_ready*)   method   Bit#(1) io_output_en_{0};
      (*always_ready*)   method   Bit#(1) io_input_en_{0};
      (*always_ready*)   method   Bit#(1) io_pullup_en_{0};
      (*always_ready*)   method   Bit#(1) io_pulldown_en_{0};
      (*always_ready*)   method   Bit#(1) io_drivestrength_{0};
      (*always_ready*)   method   Bit#(1) io_pushpull_en_{0};
      (*always_ready*)   method   Bit#(1) io_opendrain_en_{0};
      (*always_ready,always_enabled,result="io"*)
                 method   Action  io_inputval_{0}(Bit#(1) in);
'''
# == Peripheral Interface definitions == #
# these are the interface of the peripherals to the pin mux
# Outputs from the peripherals will be inputs to the pinmux
# module. Hence the change in direction for most pins

uartinterface_decl = '''
      (*always_ready,always_enabled*) method Action tx_{0}(Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) rx_{0};
'''

spiinterface_decl = '''
      (*always_ready,always_enabled*) method Action sclk_{0} (Bit#(1) in);
      (*always_ready,always_enabled*) method Action mosi_{0} (Bit#(1) in);
      (*always_ready,always_enabled*) method Action ss_{0}   (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) miso_{0};
'''

twiinterface_decl = '''
      (*always_ready,always_enabled*) method Action sda{0}_out (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sda{0}_outen (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) sda{0}_in;
      (*always_ready,always_enabled*) method Action scl{0}_out (Bit#(1) in);
      (*always_ready,always_enabled*) method Action scl{0}_outen (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) scl{0}_in;
'''

sdinterface_decl = '''
      (*always_ready,always_enabled*) method Action sd{0}_clk (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sd{0}_cmd (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sd{0}_d0_out (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sd{0}_d0_outen (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) sd{0}_d0_in;
      (*always_ready,always_enabled*) method Action sd{0}_d1_out (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sd{0}_d1_outen (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) sd{0}_d1_in;
      (*always_ready,always_enabled*) method Action sd{0}_d2_out (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sd{0}_d2_outen (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) sd{0}_d2_in;
      (*always_ready,always_enabled*) method Action sd{0}_d3_out (Bit#(1) in);
      (*always_ready,always_enabled*) method Action sd{0}_d3_outen (Bit#(1) in);
      (*always_ready,always_enabled*) method Bit#(1) sd{0}_d3_in;
'''

jtaginterface_decl = '''
      (*always_ready,always_enabled*) method Bit#(1) jtag{0}_tdi;
      (*always_ready,always_enabled*) method Bit#(1) jtag{0}_tms;
      (*always_ready,always_enabled*) method Bit#(1) jtag{0}_tclk;
      (*always_ready,always_enabled*) method Bit#(1) jtag{0}_trst;
      (*always_ready,always_enabled*) method Action jtag{0}_tdo(Bit#(1) in);
'''

pwminterface_decl = '''
      (*always_ready,always_enabled*) method Action pwm{0}(Bit#(1) in);
'''
# ======================================= #


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
        return '\n'.join(map(str, self.pins))


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
        p = _pinmunge(p, "(", " ( ", False)
        p = _pinmunge(p, ")", " ) ", False)
        p = _pinmunge(p, " ", " ")
        return p

    pwm = Interface([{'name': "pwm{0}", 'action': True}])
    print pwm
    print
    assert pinmunge(str(pwm)) == pinmunge(pwminterface_decl)

    jtag = Interface([{'name': 'jtag{0}_tdi'},
                      {'name': 'jtag{0}_tms'},
                      {'name': 'jtag{0}_tclk'},
                      {'name': 'jtag{0}_trst'},
                      {'name': 'jtag{0}_tdo', 'action': True}])
    print jtag
    print
    assert pinmunge(str(jtag)) == pinmunge(jtaginterface_decl)

    sd = Interface([{'name': 'sd{0}_clk', 'action': True},
                    {'name': 'sd{0}_cmd', 'action': True},
                    {'name': 'sd{0}_d0', 'outen': True},
                    {'name': 'sd{0}_d1', 'outen': True},
                    {'name': 'sd{0}_d2', 'outen': True},
                    {'name': 'sd{0}_d3', 'outen': True}
                    ])
    print sd
    print
    assert pinmunge(str(sd)) == pinmunge(sdinterface_decl)

    twi = Interface([{'name': 'sda{0}', 'outen': True},
                     {'name': 'scl{0}', 'outen': True},
                     ])
    print twi
    print
    assert pinmunge(str(twi)) == pinmunge(twiinterface_decl)

    spi = Interface([{'name': 'sclk_{0}', 'action': True},
                      {'name': 'mosi_{0}', 'action': True},
                      {'name': 'ss_{0}', 'action': True},
                      {'name': 'miso_{0}'},
                    ])
    print spi
    print
    assert pinmunge(str(spi)) == pinmunge(spiinterface_decl)

