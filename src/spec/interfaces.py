#!/usr/bin/env python

from copy import deepcopy


def namesuffix(name, suffix, namelist):
    names = []
    for n in namelist:
        if n:
            names.append("%s%s_%s" % (name, suffix, n))
        else:
            names.append("%s_%s" % (name, suffix))
    return names


class Pinouts(object):
    def __init__(self, bankspec):
        self.bankspec = bankspec
        self.pins = {}
        self.fnspec = {}

    def __contains__(self, k):
        return k in self.pins

    def has_key(self, k):
        return k in self.pins

    def add_spec(self, k, v):
        self.fnspec[k] = v

    def update(self, pinidx, v):
        if pinidx not in self.pins:
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

    def __getitem__(self, k):
        return self.pins[k]

    def i2s(self, suffix, offs, bank, mux=1, spec=None, limit=None):
        i2spins = ['MCK+', 'BCK+', 'LRCK+', 'DI-', 'DO+']
        # for i in range(4):
        #    i2spins.append("DO%d+" % i)
        pins = Pins('IIS', i2spins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, limit, origsuffix=suffix)
        self.pinmerge(pins)

    def emmc(self, suffix, offs, bank, mux=1, spec=None):
        emmcpins = ['CMD+', 'CLK+']
        for i in range(8):
            emmcpins.append("D%d*" % i)
        pins = Pins('MMC', emmcpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def sdmmc(self, suffix, offs, bank, mux=1, spec=None,
              start=None, limit=None):
        sdmmcpins = ['CMD+', 'CLK+']
        for i in range(4):
            sdmmcpins.append("D%d*" % i)
        sdmmcpins = sdmmcpins[start:limit]
        pins = Pins('SD', sdmmcpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def spi(self, suffix, offs, bank, mux=1, spec=None):
        spipins = ['CLK*', 'NSS*', 'MOSI*', 'MISO*']
        pins = Pins('SPI', spipins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def quadspi(self, suffix, offs, bank, mux=1, spec=None, limit=None):
        spipins = ['CK*', 'NSS*', 'IO0*', 'IO1*', 'IO2*', 'IO3*']
        pins = Pins('QSPI', spipins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, limit, origsuffix=suffix)
        self.pinmerge(pins)

    def i2c(self, suffix, offs, bank, mux=1, spec=None):
        spipins = ['SDA*', 'SCL*']
        pins = Pins('TWI', spipins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def jtag(self, suffix, offs, bank, mux=1, spec=None):
        jtagpins = ['MS+', 'DI-', 'DO+', 'CK+']
        pins = Pins('JTAG', jtagpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def uart(self, suffix, offs, bank, mux=1, spec=None):
        uartpins = ['TX+', 'RX-']
        pins = Pins('UART', uartpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def ulpi(self, suffix, offs, bank, mux=1, spec=None):
        ulpipins = ['CK+', 'DIR+', 'STP+', 'NXT+']
        for i in range(8):
            ulpipins.append('D%d*' % i)
        pins = Pins('ULPI', ulpipins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def uartfull(self, suffix, offs, bank, mux=1, spec=None):
        uartpins = ['TX+', 'RX-', 'CTS-', 'RTS+']
        pins = Pins('UARTQ', uartpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def rgbttl(self, suffix, offs, bank, mux=1, spec=None):
        ttlpins = ['CK+', 'DE+', 'HS+', 'VS+']
        for i in range(24):
            ttlpins.append("D%d+" % i)
        pins = Pins('LCD', ttlpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def rgmii(self, suffix, offs, bank, mux=1, spec=None):
        buspins = []
        for i in range(4):
            buspins.append("ERXD%d-" % i)
        for i in range(4):
            buspins.append("ETXD%d+" % i)
        buspins += ['ERXCK-', 'ERXERR-', 'ERXDV-',
                    'EMDC+', 'EMDIO*',
                    'ETXEN+', 'ETXCK+', 'ECRS-',
                    'ECOL+', 'ETXERR+']
        pins = Pins('RG', buspins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def flexbus1(self, suffix, offs, bank, mux=1, spec=None, limit=None):
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
        for i in range(2, 6):
            buspins.append("CS%d+" % i)
        pins = Pins('FB', buspins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, limit, origsuffix=suffix)
        self.pinmerge(pins)

    def flexbus2(self, suffix, offs, bank, mux=1, spec=None, limit=None):
        buspins = []
        for i in range(8, 32):
            buspins.append("AD%d*" % i)
        pins = Pins('FB', buspins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, limit, origsuffix=suffix)
        self.pinmerge(pins)

    def sdram1(self, suffix, offs, bank, mux=1, spec=None):
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
        pins = Pins('SDR', buspins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def sdram2(self, suffix, offs, bank, mux=1, spec=None, limit=None):
        buspins = []
        for i in range(3, 6):
            buspins.append("SDRCS%d#+" % i)
        for i in range(8, 32):
            buspins.append("SDRDQ%d*" % i)
        pins = Pins('SDR', buspins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, limit, origsuffix=suffix)
        self.pinmerge(pins)

    def mcu8080(self, suffix, offs, bank, mux=1, spec=None):
        buspins = []
        for i in range(8):
            buspins.append("MCUD%d*" % i)
        for i in range(8):
            buspins.append("MCUAD%d+" % (i + 8))
        for i in range(6):
            buspins.append("MCUCS%d+" % i)
        for i in range(2):
            buspins.append("MCUNRB%d+" % i)
        buspins += ['MCUCD+', 'MCURD+', 'MCUWR+', 'MCUCLE+', 'MCUALE+',
                    'MCURST+']
        pins = Pins('MCU', buspins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def _pinbank(self, prefix, suffix, offs, bank, gpiooffs, gpionum=1, mux=1,
                 spec=None):
        gpiopins = []
        for i in range(gpiooffs, gpiooffs + gpionum):
            gpiopins.append("%s%d*" % (bank, i))
        pins = Pins(prefix, gpiopins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def eint(self, suffix, offs, bank, gpiooffs, gpionum=1, mux=1, spec=None):
        gpiopins = []
        for i in range(gpiooffs, gpiooffs + gpionum):
            gpiopins.append("%d*" % (i))
        pins = Pins('EINT', gpiopins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def pwm(self, suffix, offs, bank, pwmoffs, pwmnum=1, mux=1, spec=None):
        pwmpins = []
        for i in range(pwmoffs, pwmoffs + pwmnum):
            pwmpins.append("%d+" % (i))
        pins = Pins('PWM', pwmpins, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinmerge(pins)

    def gpio(self, suffix, offs, bank, gpiooffs, gpionum=1, mux=1, spec=None):
        self._pinbank("GPIO%s" % bank, suffix, offs, bank, gpiooffs,
                      gpionum, mux=0, spec=None)

    def pinmerge(self, fn):
        # hack, store the function specs in the pins dict
        fname = fn.fname
        suffix = fn.origsuffix
        bank = fn.bank

        if not hasattr(self, 'fnspec'):
            self.fnspec = pins
        if fname == 'GPIO':
            fname = fname + bank
        assert 'EINT' not in self
        if fname not in self.fnspec:
            self.add_spec(fname, {})
        if suffix or fname == 'EINT' or fname == 'PWM':
            specname = fname + suffix
        else:
            specname = fname
        print "fname bank specname suffix ", fname, bank, specname, repr(
            suffix)
        if specname in self.fnspec[fname]:
            # ok so some declarations may bring in different
            # names at different stages (EINT, PWM, flexbus1/2)
            # so we have to merge the names in.  main thing is
            # the pingroup
            tomerge = self.fnspec[fname][specname]
            for p in fn.pingroup:
                if p not in tomerge.pingroup:
                    tomerge.pingroup.append(p)
            tomerge.pins.update(fn.pins)
            tomerge.fntype.update(fn.fntype)
        else:
            self.fnspec[fname][specname] = deepcopy(fn)

        # merge actual pins
        for (pinidx, v) in fn.pins.items():
            self.update(pinidx, v)


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
        suffix = ''  # hack

        res = {}
        names = {}
        idx = 0
        for name in pingroup[:limit]:
            if suffix and name:
                name_ = "%s_%s" % (name, suffix)
            else:
                name_ = name
            if spec and name in spec:
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
            if name not in spec:
                continue
            idx_, mux_, bank_ = spec[name]
            idx_ = names[idx_]
            pin = {mux_: (name_, bank_)}
            if idx_ in res:
                res[idx_].update(pin)
            else:
                res[idx_] = pin

        self.pins = res
