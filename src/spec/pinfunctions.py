#!/usr/bin/env python

def i2s(suffix, bank):
    return ['MCK+', 'BCK+', 'LRCK+', 'DI-', 'DO+']

def emmc(suffix, bank):
    emmcpins = ['CMD+', 'CLK+']
    for i in range(8):
        emmcpins.append("D%d*" % i)
    return emmcpins

def sdmmc(suffix, bank):
    sdmmcpins = ['CMD+', 'CLK+']
    for i in range(4):
        sdmmcpins.append("D%d*" % i)
    return sdmmcpins

def spi(suffix, bank):
    return ['CLK*', 'NSS*', 'MOSI*', 'MISO*']

def quadspi(suffix, bank):
    return ['CK*', 'NSS*', 'IO0*', 'IO1*', 'IO2*', 'IO3*']

def i2c(suffix, bank):
    return ['SDA*', 'SCL*']

def jtag(suffix, bank):
    return ['MS+', 'DI-', 'DO+', 'CK+']

def uart(suffix, bank):
    return ['TX+', 'RX-']

def ulpi(suffix, bank):
    ulpipins = ['CK+', 'DIR+', 'STP+', 'NXT+']
    for i in range(8):
        ulpipins.append('D%d*' % i)
    return ulpipins

def uartfull(suffix, bank):
    return ['TX+', 'RX-', 'CTS-', 'RTS+']

def rgbttl(suffix, bank):
    ttlpins = ['CK+', 'DE+', 'HS+', 'VS+']
    for i in range(24):
        ttlpins.append("D%d+" % i)
    return ttlpins

def rgmii(suffix, bank):
    buspins = []
    for i in range(4):
        buspins.append("ERXD%d-" % i)
    for i in range(4):
        buspins.append("ETXD%d+" % i)
    buspins += ['ERXCK-', 'ERXERR-', 'ERXDV-',
                'EMDC+', 'EMDIO*',
                'ETXEN+', 'ETXCK+', 'ECRS-',
                'ECOL+', 'ETXERR+']
    return buspins

def flexbus1(suffix, bank):
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
    return buspins

def flexbus2(suffix, bank):
    buspins = []
    for i in range(8, 32):
        buspins.append("AD%d*" % i)
    return buspins

def sdram1(suffix, bank):
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
    return buspins

def sdram2(suffix, bank):
    buspins = []
    for i in range(3, 6):
        buspins.append("SDRCS%d#+" % i)
    for i in range(8, 32):
        buspins.append("SDRDQ%d*" % i)
    return buspins

def mcu8080(suffix, bank):
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
    return buspins

class RangePin(object):
    def __init__(self, suffix, prefix=None):
        self.suffix = suffix
        self.prefix = prefix or ''

    def __getitem__(self, s):
        res = []
        for idx in range(s.start or 0, s.stop or -1, s.step or 1):
            res.append("%s%d%s" % (self.prefix, idx, self.suffix))
        return res

def eint(suffix, bank):
    return RangePin("*")

def pwm(suffix, bank):
    return RangePin("+")

def gpio(suffix, bank):
    return ("GPIO%s" % bank, RangePin(prefix=bank, suffix="*"))


# list functions by name here

pinspec = (('IIS', i2s),
           ('MMC', emmc),
           ('SD', sdmmc),
           ('SPI', spi),
           ('QSPI', quadspi),
           ('TWI', i2c),
           ('JTAG', jtag),
           ('UART', uart),
           ('UARTQ', uartfull),
           ('LCD', rgbttl),
           ('ULPI', ulpi),
           ('RG', rgmii),
           ('FB', flexbus1),
           ('FB', flexbus2),
           ('SDR', sdram1),
           ('SDR', sdram2),
           ('EINT', eint),
           ('PWM', pwm),
           ('GPIO', gpio),
          )

