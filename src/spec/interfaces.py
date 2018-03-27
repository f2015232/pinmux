#!/usr/bin/env python

class Pinouts(object):
    def __init__(self):
        self.pins = {}
        self.fnspec = {}

    def has_key(self, k):
        return self.pins.has_key(k)

    def add_spec(self, k, v):
        self.fnspec[k] = v

    def update(self, pinidx, v):
        if not self.pins.has_key(pinidx):
            self.pins[pinidx] = v
        else:
            self.pins[pinidx].update(v)

    def keys(self):
        return self.pins.keys()

    def items(self):
        return self.pins.items()

    def get(self, k):
        return self.pins[k]

    def __len__(self):
        return len(self.pins)

    def __delitem__(self, k):
        del self.pins[k]


class Pins(object):

    def __init__(self, fname, pingroup, bankspec, suffix, offs, bank, mux,
             spec=None, limit=None, origsuffix=None):

        # function type can be in, out or inout, represented by - + *
        # strip function type out of each pin name
        self.fntype = {}
        for i in range(len(pingroup)):
            pname = pingroup[i]
            if not pname:
                continue
            fntype = pname[-1]
            if fntype not in '+-*':
                continue
            pname = pname[:-1]
            fntype = {'-': 'in', '+': 'out', '*': 'inout'}[fntype]
            self.fntype[pname] = fntype
            pingroup[i] = pname

        self.fname = fname
        self.pingroup = pingroup
        self.bankspec = bankspec
        self.suffix = suffix
        self.origsuffix = origsuffix or suffix
        self.bank = bank
        self.mux = mux

        # create consistent name suffixes
        pingroup = namesuffix(fname, suffix, pingroup)
        suffix = '' # hack

        res = {}
        names = {}
        idx = 0
        for name in pingroup[:limit]:
            if suffix and name:
                name_ = "%s_%s" % (name, suffix)
            else:
                name_ = name
            if spec and spec.has_key(name):
                continue
            pin = {mux: (name_, bank)}
            offs_bank, offs_ = offs
            idx_ = offs_ + idx
            idx += 1
            idx_ += bankspec[bank]
            res[idx_] = pin
            names[name] = idx_
        for name in pingroup:
            if suffix and name:
                name_ = "%s_%s" % (name, suffix)
            else:
                name_ = name
            if not spec:
                continue
            if not spec.has_key(name):
                continue
            idx_, mux_, bank_ = spec[name]
            idx_ = names[idx_]
            pin = {mux_: (name_, bank_)}
            if res.has_key(idx_):
                res[idx_].update(pin)
            else:
                res[idx_] = pin

        self.pins = res


def i2s(bankspec, suffix, offs, bank, mux=1, spec=None, limit=None):
    i2spins = ['MCK+', 'BCK+', 'LRCK+', 'DI-', 'DO+']
    #for i in range(4):
    #    i2spins.append("DO%d+" % i)
    return Pins('IIS', i2spins, bankspec, suffix, offs, bank, mux, spec, limit,
                origsuffix=suffix)

def emmc(bankspec, suffix, offs, bank, mux=1, spec=None):
    emmcpins = ['CMD+', 'CLK+']
    for i in range(8):
        emmcpins.append("D%d*" % i)
    return Pins('MMC', emmcpins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def sdmmc(bankspec, suffix, offs, bank, mux=1, spec=None,
                start=None, limit=None):
    sdmmcpins = ['CMD+', 'CLK+']
    for i in range(4):
        sdmmcpins.append("D%d*" % i)
    sdmmcpins = sdmmcpins[start:limit]
    return Pins('SD', sdmmcpins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def spi(bankspec, suffix, offs, bank, mux=1, spec=None):
    spipins = ['CLK*', 'NSS*', 'MOSI*', 'MISO*']
    return Pins('SPI', spipins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def quadspi(bankspec, suffix, offs, bank, mux=1, spec=None, limit=None):
    spipins = ['CK*', 'NSS*', 'IO0*', 'IO1*', 'IO2*', 'IO3*']
    return Pins('QSPI', spipins, bankspec, suffix, offs, bank, mux, spec, limit,
                origsuffix=suffix)

def i2c(bankspec, suffix, offs, bank, mux=1, spec=None):
    spipins = ['SDA*', 'SCL*']
    return Pins('TWI', spipins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def jtag(bankspec, suffix, offs, bank, mux=1, spec=None):
    jtagpins = ['MS+', 'DI-', 'DO+', 'CK+']
    return Pins('JTAG', jtagpins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def uart(bankspec, suffix, offs, bank, mux=1, spec=None):
    uartpins = ['TX+', 'RX-']
    return Pins('UART', uartpins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def namesuffix(name, suffix, namelist):
    names = []
    for n in namelist:
        if n:
            names.append("%s%s_%s" % (name, suffix, n))
        else:
            names.append("%s_%s" % (name, suffix))
    return names

def ulpi(bankspec, suffix, offs, bank, mux=1, spec=None):
    ulpipins = ['CK+', 'DIR+', 'STP+', 'NXT+']
    for i in range(8):
        ulpipins.append('D%d*' % i)
    return Pins('ULPI', ulpipins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def uartfull(bankspec, suffix, offs, bank, mux=1, spec=None):
    uartpins = ['TX+', 'RX-', 'CTS-', 'RTS+']
    return Pins('UARTQ', uartpins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def rgbttl(bankspec, suffix, offs, bank, mux=1, spec=None):
    ttlpins = ['CK+', 'DE+', 'HS+', 'VS+']
    for i in range(24):
        ttlpins.append("D%d+" % i)
    return Pins('LCD', ttlpins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def rgmii(bankspec, suffix, offs, bank, mux=1, spec=None):
    buspins = []
    for i in range(4):
        buspins.append("ERXD%d-" % i)
    for i in range(4):
        buspins.append("ETXD%d+" % i)
    buspins += ['ERXCK-', 'ERXERR-', 'ERXDV-',
                'EMDC+', 'EMDIO*',
                'ETXEN+', 'ETXCK+', 'ECRS-',
                'ECOL+', 'ETXERR+']
    return Pins('RG', buspins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def flexbus1(bankspec, suffix, offs, bank, mux=1, spec=None, limit=None):
    buspins = []
    for i in range(8):
        buspins.append("AD%d*" % i)
    for i in range(2):
        buspins.append("CS%d+" % i)
    buspins += ['ALE', 'OE', 'RW', 'TA', 'CLK+',
                'A0', 'A1', 'TS', 'TBST',
                'TSIZ0', 'TSIZ1']
    for i in range(4):
        buspins.append("BWE%d" % i)
    for i in range(2,6):
        buspins.append("CS%d+" % i)
    return Pins('FB', buspins, bankspec, suffix, offs, bank, mux, spec, limit,
                origsuffix=suffix)

def flexbus2(bankspec, suffix, offs, bank, mux=1, spec=None, limit=None):
    buspins = []
    for i in range(8,32):
        buspins.append("AD%d*" % i)
    return Pins('FB', buspins, bankspec, suffix, offs, bank, mux, spec, limit,
                origsuffix=suffix)

def sdram1(bankspec, suffix, offs, bank, mux=1, spec=None):
    buspins = []
    for i in range(16):
        buspins.append("SDRDQM%d*" % i)
    for i in range(12):
        buspins.append("SDRAD%d+" % i)
    for i in range(8):
        buspins.append("SDRDQ%d+" % i)
    for i in range(3):
        buspins.append("SDRCS%d#+" % i)
    for i in range(2):
        buspins.append("SDRDQ%d+" % i)
    for i in range(2):
        buspins.append("SDRBA%d+" % i)
    buspins += ['SDRCKE+', 'SDRRAS#+', 'SDRCAS#+', 'SDRWE#+',
                'SDRRST+']
    return Pins('SDR', buspins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def sdram2(bankspec, suffix, offs, bank, mux=1, spec=None, limit=None):
    buspins = []
    for i in range(3,6):
        buspins.append("SDRCS%d#+" % i)
    for i in range(8,32):
        buspins.append("SDRDQ%d*" % i)
    return Pins('SDR', buspins, bankspec, suffix, offs, bank, mux, spec, limit,
                origsuffix=suffix)

def mcu8080(bankspec, suffix, offs, bank, mux=1, spec=None):
    buspins = []
    for i in range(8):
        buspins.append("MCUD%d*" % i)
    for i in range(8):
        buspins.append("MCUAD%d+" % (i+8))
    for i in range(6):
        buspins.append("MCUCS%d+" % i)
    for i in range(2):
        buspins.append("MCUNRB%d+" % i)
    buspins += ['MCUCD+', 'MCURD+', 'MCUWR+', 'MCUCLE+', 'MCUALE+',
                'MCURST+']
    return Pins('MCU', buspins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def _pinbank(bankspec, prefix, suffix, offs, bank, gpiooffs, gpionum=1, mux=1,
             spec=None):
    gpiopins = []
    for i in range(gpiooffs, gpiooffs+gpionum):
        gpiopins.append("%s%d*" % (bank, i))
    return Pins('GPIO', gpiopins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def eint(bankspec, suffix, offs, bank, gpiooffs, gpionum=1, mux=1, spec=None):
    gpiopins = []
    for i in range(gpiooffs, gpiooffs+gpionum):
        gpiopins.append("%d*" % (i))
    return Pins('EINT', gpiopins, bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def pwm(bankspec, suffix, offs, bank, mux=1, spec=None):
    return Pins('PWM', ['+', ], bankspec, suffix, offs, bank, mux, spec,
                origsuffix=suffix)

def gpio(bankspec, suffix, offs, bank, gpiooffs, gpionum=1, mux=1, spec=None):
    return _pinbank(bankspec, "GPIO", suffix, offs, bank, gpiooffs,
                              gpionum, mux=0, spec=None)

def pinmerge(pins, fn):
    # hack, store the function specs in the pins dict
    fname = fn.fname
    suffix = fn.origsuffix
    bank = fn.bank

    if not hasattr(pins, 'fnspec'):
        pins.fnspec = pins
    if fname == 'GPIO':
        fname = fname + bank
    assert not pins.has_key('EINT')
    if not pins.fnspec.has_key(fname):
        pins.add_spec(fname, {})
    print "fname bank suffix", fname, bank, suffix
    if suffix or fname == 'EINT' or fname == 'PWM':
        specname = fname + suffix
    else:
        specname = fname + bank
    pins.fnspec[fname][specname] = fn


    # merge actual pins
    for (pinidx, v) in fn.pins.items():
        print "pinidx", pinidx
        pins.update(pinidx, v)

