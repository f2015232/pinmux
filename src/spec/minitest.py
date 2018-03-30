#!/usr/bin/env python

from spec.interfaces import Pinouts

from spec.ifaceprint import display, display_fns, check_functions
from spec.ifaceprint import display_fixed


def pinspec():
    pinbanks = {
        'B': 28,
    }
    bankspec = {}
    pkeys = sorted(pinbanks.keys())
    offs = 0
    for kn in pkeys:
        bankspec[kn] = offs
        offs += pinbanks[kn]

    pinouts = Pinouts(bankspec)

    # Bank B, 16-47
    pinouts.gpio("", ('B', 0), "B", 0, 0, 28)
    pinouts.rgbttl("", ('B', 0), "B", 1, limit=23)
    pinouts.spi("0", ('B', 10), "B", 2)
    pinouts.quadspi("", ('B', 4), "B", 2)
    pinouts.uart("0", ('B', 16), "B", 2)
    pinouts.i2c("2", ('B', 18), "B", 2)
    pinouts.pwm("", ('B', 21), "B", 2, 0, 3)
    pinouts.sdmmc("0", ('B', 22), "B", 3)
    pinouts.eint("", ('B', 0), "B", 3, 0, 4)
    pinouts.eint("", ('B', 20), "B", 2, 4, 1)
    pinouts.eint("", ('B', 23), "B", 1, 5, 1)
    pinouts.sdmmc("1", ('B', 4), "B", 3)
    pinouts.jtag("1", ('B', 10), "B", 3)
    pinouts.uartfull("0", ('B', 14), "B", 3)
    pinouts.uartfull("1", ('B', 18), "B", 3)
    pinouts.jtag("0", ('B', 24), "B", 2)
    pinouts.spi("1", ('B', 24), "B", 1)
    pinouts.i2c("0", ('B', 0), "B", 2)
    pinouts.uart("1", ('B', 2), "B", 2)
    pinouts.uart("2", ('B', 14), "B", 2)

    print ("""# Pinouts (PinMux)
auto-generated by [[pinouts.py]]

[[!toc  ]]
""")
    display(pinouts)

    print ("\n# Pinouts (Fixed function)\n")

    fixedpins = {
        'CTRL_SYS': [
            'TEST',
            'JTAG_SEL',
            'UBOOT_SEL',
            'NMI#',
            'RESET#',
            'CLK24M_IN',
            'CLK24M_OUT',
            'PLLTEST',
            'PLLREGIO',
            'PLLVP25',
            'PLLDV',
            'PLLVREG',
            'PLLGND',
        ],
        'POWER_GPIO': [
            'VDD_GPIOB',
            'GND_GPIOB',
        ]}

    fixedpins = display_fixed(fixedpins, len(pinouts))

    print ("""# Functions (PinMux)

auto-generated by [[pinouts.py]]
""")

    function_names = {'EINT': 'External Interrupt',
                      'FB': 'MC68k FlexBus',
                      'IIS': 'I2S Audio',
                      'JTAG0': 'JTAG (same as JTAG1, JTAG_SEL=LOW)',
                      'JTAG1': 'JTAG (same as JTAG0, JTAG_SEL=HIGH)',
                      'LCD': '24-pin RGB/TTL LCD',
                      'RG': 'RGMII Ethernet',
                      'MMC': 'eMMC 1/2/4/8 pin',
                      'PWM': 'PWM (pulse-width modulation)',
                      'SD0': 'SD/MMC 0',
                      'SD1': 'SD/MMC 1',
                      'SD2': 'SD/MMC 2',
                      'SPI0': 'SPI (Serial Peripheral Interface) 0',
                      'SPI1': 'SPI (Serial Peripheral Interface) 1',
                      'QSPI': 'Quad SPI (Serial Peripheral Interface) 1',
                      'TWI0': 'I2C 0',
                      'TWI1': 'I2C 1',
                      'TWI2': 'I2C 2',
                      'UARTQ0': 'UART (TX/RX/CTS/RTS) 0',
                      'UARTQ1': 'UART (TX/RX/CTS/RTS) 1',
                      'UART0': 'UART (TX/RX) 0',
                      'UART1': 'UART (TX/RX) 1',
                      'UART2': 'UART (TX/RX) 2',
                      'ULPI0': 'ULPI (USB Low Pin-count) 0',
                      'ULPI1': 'ULPI (USB Low Pin-count) 1',
                      'ULPI2': 'ULPI (USB Low Pin-count) 2',
                      }

    fns = display_fns(bankspec, pinouts, function_names)
    print

    # Scenarios below can be spec'd out as either "find first interface"
    # by name/number e.g. SPI1, or as "find in bank/mux" which must be
    # spec'd as "BM:Name" where B is bank (A-F), M is Mux (0-3)
    # EINT and PWM are grouped together, specially, but may still be spec'd
    # using "BM:Name".  Pins are removed in-order as listed from
    # lists (interfaces, EINTs, PWMs) from available pins.

    minitest = ['ULPI0/8', 'ULPI1', 'MMC', 'SD0', 'UART0',
                'TWI0', 'SPI0', 'B3:SD1', ]
    minitest_eint = ['EINT_0', 'EINT_1', 'EINT_2', 'EINT_3', 'EINT_4']
    minitest_pwm = ['B2:PWM_0']
    descriptions = {
        'MMC': 'internal (on Card)',
        'SD0': 'user-facing: internal (on Card), multiplexed with JTAG1\n'
        'and UART2, for debug purposes',
        'TWI2': 'I2C.\n',
        'E2:SD1': '',
        'SPI1': '',
        'UART0': '',
        'B1:LCD/22': '18-bit RGB/TTL LCD',
        'ULPI0/8': 'user-facing: internal (on Card), USB-OTG ULPI PHY',
        'ULPI1': 'dual USB2 Host ULPI PHY'
    }

    unused_pins = check_functions("MiniTest", bankspec, fns, pinouts,
                                  minitest, minitest_eint, minitest_pwm,
                                  descriptions)

    print ("""# Reference Datasheets

datasheets and pinout links
* <http://datasheets.chipdb.org/AMD/8018x/80186/amd-80186.pdf>
* <http://hands.com/~lkcl/eoma/shenzen/frida/FRD144A2701.pdf>
* <http://pinouts.ru/Memory/sdcard_pinout.shtml>
* p8 <http://www.onfi.org/~/media/onfi/specs/onfi_2_0_gold.pdf?la=en>
* <https://www.heyrick.co.uk/blog/files/datasheets/dm9000aep.pdf>
* <http://cache.freescale.com/files/microcontrollers/doc/app_note/AN4393.pdf>
* <https://www.nxp.com/docs/en/data-sheet/MCF54418.pdf>
* ULPI OTG PHY, ST <http://www.st.com/en/interfaces-and-transceivers/stulpi01a.html>
* ULPI OTG PHY, TI TUSB1210 <http://ti.com/product/TUSB1210/>
""")

    return pinouts, bankspec, pinbanks, fixedpins
