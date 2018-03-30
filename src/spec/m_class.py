#!/usr/bin/env python

from spec.interfaces import Pinouts

from spec.ifaceprint import display, display_fns, check_functions
from spec.ifaceprint import display_fixed


def pinspec():
    pinbanks = {'A': 16,
                'B': 28,
                'C': 24,
                'D': 24,
                'E': 24,
                'F': 10,
                'G': 32,
                }
    bankspec = {}
    pkeys = sorted(pinbanks.keys())
    offs = 0
    for kn in pkeys:
        bankspec[kn] = offs
        offs += pinbanks[kn]

    pinouts = Pinouts(bankspec)

    # Bank A, 0-15
    pinouts.gpio("", ('A', 0), "A", 0, 16, 0)
    pinouts.spi("1", ('A', 0), "A", 3)
    pinouts.uartfull("1", ('A', 0), "A", 2)
    pinouts.i2c("1", ('A', 4), "A", 2)
    pinouts.emmc("", ('A', 0), "A", 1)
    #pinouts.uart("2", ('A', 14), "A", 1)
    pinouts.spi("2", ('A', 6), "A", 2)
    pinouts.eint("", ('A', 10), "A", 0, 6)
    pinouts.eint("", ('A', 4), "A", 0, 6, mux=3)
    pinouts.sdmmc("1", ('A', 10), "A", 2)
    pinouts.jtag("1", ('A', 10), "A", 3)
    pinouts.uart("2", ('A', 14), "A", 3)

    # Bank B, 16-47
    pinouts.gpio("", ('B', 0), "B", 0, 28, 0)
    pinouts.rgbttl("0", ('B', 0), "B", 1)
    pinouts.spi("1", ('B', 12), "B", 2)
    pinouts.quadspi("", ('B', 4), "B", 2, limit=4)
    pinouts.uart("3", ('B', 16), "B", 2)
    pinouts.i2c("3", ('B', 18), "B", 2)
    pinouts.pwm("", ('B', 9), "B", 0, 1, mux=2)
    pinouts.pwm("", ('B', 20), "B", 1, 2, mux=2)
    pinouts.sdmmc("1", ('B', 22), "B", 2)
    pinouts.eint("", ('B', 0), "B", 6, 4, mux=3)
    pinouts.flexbus2("", ('B', 4), "B", 3)
    pinouts.i2c("1", ('B', 0), "B", 2)
    pinouts.uart("2", ('B', 2), "B", 2)
    pinouts.uart("4", ('B', 10), "B", 2)

    # Bank C, 48-71
    pinouts.gpio("", ("C", 0), "C", 0, 24, 0)
    pinouts.ulpi("1", ('C', 0), "C", 1)
    pinouts.ulpi("2", ('C', 12), "C", 1)
    pinouts.spi("2", ('C', 8), "C", 2)
    #pinouts.spi("2", ('C', 28), "C", 2)
    pinouts.uartfull("0", ('C', 20), "C", 3)
    pinouts.eint("", ('C', 0), "C", 10, 8, mux=3)
    pinouts.jtag("2", ('C', 8), "C", 3)
    pinouts.eint("", ('C', 12), "C", 22, 8, mux=3)
    pinouts.uart("2", ('C', 22), "C", 2)
    pinouts.i2s("", ('C', 13), "C", 2)
    pinouts.pwm("", ('C', 21), "C", 2, 1, mux=2)

    # Bank D, 72-96

    # ok this is slightly complicated, basically there's extra
    # functions that we want to be on the same pin (but a different mux)
    # because their use is mutually-exclusive.  you can't have FB_TS
    # at the same time as FB_ALE for example.  FB_BWE2 even has two
    # mutually exclusive functions.  these extra functions are
    # specified here, so that when e.g. FB_BWE2 has been positioned,
    # FB_A0 will be placed in bank d, mux column 3, *on the same pin*.
    # this saves messing about, because if FB_BWE2 moved to a
    # different pin so would FB_A0 (and FB_CS2) likewise have to be
    # moved.  and the rest.
    flexspec = {
        'FB_TS': ('FB_ALE', 2, "D"),
        'FB_CS2': ('FB_BWE2', 2, "D"),
        'FB_A0': ('FB_BWE2', 3, "D"),
        'FB_CS3': ('FB_BWE3', 2, "D"),
        'FB_A1': ('FB_BWE3', 3, "D"),
        'FB_TBST': ('FB_OE', 2, "D"),
        'FB_TSIZ0': ('FB_BWE0', 2, "D"),
        'FB_TSIZ1': ('FB_BWE1', 2, "D"),
    }
    #pinouts.mcu8080("", 72, "D", 1)
    pinouts.gpio("", ('D', 0), "D", 0, 24, 0)
    pinouts.flexbus1("", ('D', 0), "D", 1, spec=flexspec)
    pinouts.i2c("2", ('D', 8), "D", 3)
    pinouts.pwm("", ('D', 21), "D", 0, 3, mux=1)
    pinouts.i2c("1", ('D', 10), "D", 3)
    pinouts.i2c("3", ('D', 19), "D", 2)
    pinouts.uartfull("0", ('D', 0), "D", 2)
    pinouts.uart("3", ('D', 21), "D", 2)
    pinouts.uart("4", ('D', 13), "D", 2)
    pinouts.eint("", ('D', 19), "D", 18, 4, mux=3)
    pinouts.eint("", ('D', 23), "D", 9, 1, mux=3)
    pinouts.eint("", ('D', 13), "D", 5, 4, mux=3)
    pinouts.eint("", ('D', 0), "D", 30, 2, mux=3)
    pinouts.i2c("2", ('D', 2), "D", 3)
    pinouts.sdmmc("2", ('D', 4), "D", 2)

    # Bank E
    pinouts.gpio("", ('E', 0), "E", 0, 24, 0)
    pinouts.flexbus2("", ('E', 0), "E", 1)
    pinouts.sdmmc("2", ('E', 0), "E", 2)
    pinouts.sdmmc("3", ('E', 8), "E", 2)
    pinouts.quadspi("", ('E', 18), "E", 2)
    pinouts.uartfull("1", ('E', 14), "E", 2)
    pinouts.i2c("2", ('E', 6), "E", 2)
    pinouts.eint("", ('E', 0), "E", 10, 8, mux=3)
    pinouts.eint("", ('E', 8), "E", 22, 6, mux=3)
    pinouts.emmc("", ('E', 14), "E", 3)

    # Bank F
    pinouts.gpio("", ('F', 0), "F", 0, 10, 0)
    pinouts.i2s("", ('F', 0), "F", 1)
    pinouts.i2c("1", ('F', 6), "F", 2)
    pinouts.pwm("", ('F', 8), "F", 0, 1, mux=2)
    pinouts.pwm("", ('F', 9), "F", 1, 1, mux=2)
    pinouts.uart("4", ('F', 8), "F", 1)
    pinouts.sdmmc("3", ('F', 0), "F", 2)
    pinouts.eint("", ('F', 0), "F", 18, 4, mux=3)
    pinouts.pwm("", ('F', 4), "F", 2, 1, mux=3)
    pinouts.eint("", ('F', 5), "F", 7, 1, mux=3)
    pinouts.eint("", ('F', 6), "F", 28, 4, mux=3)

    # Bank G
    pinouts.gpio("", ('G', 0), "G", 0, 32, 0)
    pinouts.rgmii("", ('G', 0), "G", 1)
    pinouts.ulpi("3", ('G', 20), "G", 1)
    pinouts.rgbttl("1", ('G', 0), "G", 2)
    pinouts.quadspi("", ('G', 26), "G", 3)
    pinouts.flexbus2("", ('G', 0), "G", 3)
    pinouts.sdmmc("2", ('G', 24), "G", 3, limit=2)
    pinouts.sdmmc("2", ('G', 28), "G", 2, start=2)

    print ("""# Pinouts (PinMux)
auto-generated by [[pinouts.py]]

[[!toc  ]]
""")
    display(pinouts)

    print ("\n# Pinouts (Fixed function)\n")

    fixedpins = {
        'DDR3': [
            'SDQ0',
            'SDQ1',
            'SDQ2',
            'SDQ3',
            'SDQ4',
            'SDQ5',
            'SDQ6',
            'SDQ7',
            'SDQ8',
            'SDQ9',
            'SDQ10',
            'SDQ11',
            'SDQ12',
            'SDQ13',
            'SDQ14',
            'SDQ15',
            'SDQ16',
            'SDQ17',
            'SDQ18',
            'SDQ19',
            'SDQ20',
            'SDQ21',
            'SDQ22',
            'SDQ23',
            'SDQ24',
            'SDQ25',
            'SDQ26',
            'SDQ27',
            'SDQ28',
            'SDQ29',
            'SDQ30',
            'SDQ31',
            'SVREF0',
            'SVREF1',
            'SVREF2',
            'SVREF3',
            'SDQS0',
            'SDQS0#',
            'SDQS1',
            'SDQS1#',
            'SDQS2',
            'SDQS2#',
            'SDQS3',
            'SDQS3#',
            'SDQM0',
            'SDQM1',
            'SDQM2',
            'SDQM3',
            'SCK#',
            'SCK',
            'SCKE0',
            'SCKE1',
            'SA0',
            'SA1',
            'SA2',
            'SA3',
            'SA4',
            'SA5',
            'SA6',
            'SA7',
            'SA8',
            'SA9',
            'SA10',
            'SA11',
            'SA12',
            'SA13',
            'SA14',
            'SBA0',
            'SBA1',
            'SBA2',
            'SWE',
            'SCAS',
            'SRAS',
            'SCS0',
            'SCS1',
            'SZQ',
            'SRST',
            'SDBG0',
            'SDBG1',
            'ADBG',
            'ODT0',
            'ODT1'],
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
        'POWER_DRAM': [
            'VCC0_DRAM',
            'VCC1_DRAM',
            'VCC2_DRAM',
            'VCC3_DRAM',
            'VCC4_DRAM',
            'VCC5_DRAM',
            'VCC6_DRAM',
            'VCC7_DRAM',
            'VCC8_DRAM',
            'VCC9_DRAM',
            'GND0_DRAM',
            'GND1_DRAM',
            'GND2_DRAM',
            'GND3_DRAM',
            'GND4_DRAM',
            'GND5_DRAM',
            'GND6_DRAM',
            'GND7_DRAM',
            'GND8_DRAM',
            'GND9_DRAM',
        ],
        'POWER_CPU': [
            'VDD0_CPU',
            'VDD1_CPU',
            'VDD2_CPU',
            'VDD3_CPU',
            'VDD4_CPU',
            'VDD5_CPU',
            'GND0_CPU',
            'GND1_CPU',
            'GND2_CPU',
            'GND3_CPU',
            'GND4_CPU',
            'GND5_CPU',
        ],
        'POWER_DLL': [
            'VDD0_DLL',
            'VDD1_DLL',
            'VDD2_DLL',
            'GND0_DLL',
            'GND1_DLL',
            'GND2_DLL',
        ],
        'POWER_INT': [
            'VDD0_INT',
            'VDD1_INT',
            'VDD2_INT',
            'VDD3_INT',
            'VDD4_INT',
            'VDD5_INT',
            'VDD6_INT',
            'VDD7_INT',
            'VDD8_INT',
            'VDD9_INT',
            'GND0_INT',
            'GND1_INT',
            'GND2_INT',
            'GND3_INT',
            'GND4_INT',
            'GND5_INT',
            'GND6_INT',
            'GND7_INT',
            'GND8_INT',
            'GND9_INT',
        ],
        'POWER_GPIO': [
            'VDD_GPIOA',
            'VDD_GPIOB',
            'VDD_GPIOC',
            'VDD_GPIOD',
            'VDD_GPIOE',
            'VDD_GPIOF',
            'VDD_GPIOG',
            'GND_GPIOA',
            'GND_GPIOB',
            'GND_GPIOC',
            'GND_GPIOD',
            'GND_GPIOE',
            'GND_GPIOF',
            'GND_GPIOG',
        ]}

    fixedpins = display_fixed(fixedpins, len(pinouts))

    print ("""# Functions (PinMux)

auto-generated by [[pinouts.py]]
""")

    function_names = {'EINT': 'External Interrupt',
                      'FB': 'MC68k FlexBus',
                      'IIS': 'I2S Audio',
                      'JTAG1': 'JTAG (same as JTAG2, JTAG_SEL=LOW)',
                      'JTAG2': 'JTAG (same as JTAG1, JTAG_SEL=HIGH)',
                      'LCD': '24-pin RGB/TTL LCD',
                      'RG': 'RGMII Ethernet',
                      'MMC': 'eMMC 1/2/4/8 pin',
                      'PWM': 'PWM (pulse-width modulation)',
                      'SD1': 'SD/MMC 1',
                      'SD2': 'SD/MMC 2',
                      'SD3': 'SD/MMC 3',
                      'SPI1': 'SPI (Serial Peripheral Interface) 1',
                      'SPI2': 'SPI (Serial Peripheral Interface) 2',
                      'QSPI': 'Quad SPI (Serial Peripheral Interface) 1',
                      'TWI1': 'I2C 1',
                      'TWI2': 'I2C 2',
                      'TWI3': 'I2C 3',
                      'UARTQ0': 'UART (TX/RX/CTS/RTS) 0',
                      'UARTQ1': 'UART (TX/RX/CTS/RTS) 1',
                      'UART2': 'UART (TX/RX) 2',
                      'UART3': 'UART (TX/RX) 3',
                      'UART4': 'UART (TX/RX) 4',
                      'ULPI1': 'ULPI (USB Low Pin-count) 1',
                      'ULPI2': 'ULPI (USB Low Pin-count) 2',
                      'ULPI3': 'ULPI (USB Low Pin-count) 3',
                      }

    fns = display_fns(bankspec, pinouts, function_names)
    print

    # Scenarios below can be spec'd out as either "find first interface"
    # by name/number e.g. SPI1, or as "find in bank/mux" which must be
    # spec'd as "BM:Name" where B is bank (A-F), M is Mux (0-3)
    # EINT and PWM are grouped together, specially, but may still be spec'd
    # using "BM:Name".  Pins are removed in-order as listed from
    # lists (interfaces, EINTs, PWMs) from available pins.

    # EOMA68 scenario.  not totally complete (some GPIO needed for PMIC)
    # One interface to be connected to the MCU to give RTC and boot/dbg
    # VBUS_EN, OTG_ID etc. are all not included below, there is plenty
    # of spare GPIO.

    eoma68 = ['B1:LCD/22', 'ULPI1/8', 'ULPI2', 'MMC', 'SD1', 'UART3',
              'TWI3', 'SPI2', 'E2:SD2', ]
    eoma68_eint = ['EINT_16', 'EINT_17', 'EINT_18', 'EINT_19']
    eoma68_pwm = ['D1:PWM_2']
    descriptions = {
        'MMC': 'internal (on Card)',
        'SD1': 'user-facing: internal (on Card), multiplexed with JTAG1\n'
        'and UART2, for debug purposes',
        'TWI3': 'EOMA68-compliance: must be entirely free of devices.\n'
        'Address 0x51 used (externally) for EOMA68 EEPROM Id',
        'E2:SD2': 'EOMA68-compliance',
        'SPI2': 'EOMA68-compliance',
        'UART3': 'EOMA68-compliance',
        'B1:LCD/22': 'EOMA68-compliance, 18-bit RGB/TTL LCD',
        'ULPI1/8': 'user-facing: internal (on Card), USB-OTG ULPI PHY',
        'ULPI2': 'EOMA68-compliance: dual USB2 Host ULPI PHY'
    }

    unused_pins = check_functions("EOMA68", bankspec, fns, pinouts,
                                  eoma68, eoma68_eint, eoma68_pwm,
                                  descriptions)

    # Industrial scenario.  not totally complete (some GPIO needed for PMIC)
    # One interface to be connected to the MCU to give RTC, boot/dbg,
    # option of CAN Bus, ADC, DAC, OWB, more GPIO, more PWM etc. etc.
    # Focus is on getting as many UARTs, SPIs and TWIs as possible.
    # OTG_ID (if to be used) would require dropping some functions in order
    # to free up GPIO.  LCD could be reduced to 15-bit (freeing 3).
    # MMC could be reduced to 4-bit-wide, used as SD/MMC (freeing 4).
    # QSPI could be used in 1-bit (MOSI/MISO) mode (freeing up 2 more).

    industrial = ['D1:FB/17', 'E1:FB/8', 'B1:LCD/22', 'ULPI1/8', 'ULPI2/8',
                  'MMC', 'B2:SD1',
                  'JTAG1', 'A3:UART2', 'E2:UART1', 'C3:UART0',
                  'F2:TWI1', 'D2:TWI2', 'D2:TWI3', 'SPI2', 'QSPI', 'F2:SD3']
    industrial_pwm = ['F2:PWM_0', 'F2:PWM_1', 'D1:PWM_2']
    industrial_eint = ['EINT_24', 'EINT_25', 'EINT_26', 'EINT_27',
                       'EINT_20', 'EINT_21', 'EINT_22', 'EINT_23']

    unused_pins = check_functions("Industrial", bankspec, fns, pinouts,
                                  industrial, industrial_eint, industrial_pwm)

    # Industrial scenario, using an SPI-based LCD instead of RGB/TTL
    # not totally complete (some GPIO needed for PMIC)
    # One interface to be connected to the MCU to give RTC, boot/dbg,
    # option of CAN Bus, ADC, DAC, OWB, more GPIO, more PWM etc. etc.
    # Focus is on getting as many UARTs, SPIs and TWIs as possible,
    # leaving some GPIO spare from the RGB/TTL bank (SPI CS#)
    # also possibility of freeing up FlexBus CS# with a little reorg.

    industrial = ['D1:FB/17', 'E1:FB/8', 'B2:SPI1', 'ULPI1/8', 'ULPI2/8',
                  'MMC', 'B2:SD1',
                  'JTAG1',
                  'A3:UART2', 'E2:UART1', 'C3:UART0', 'B2:UART4', 'B2:UART3',
                  'F2:TWI1', 'D2:TWI2', 'D2:TWI3', 'SPI2', 'QSPI', 'F2:SD3']
    industrial_pwm = ['F2:PWM_0', 'F2:PWM_1', 'D1:PWM_2']
    industrial_eint = ['EINT_24', 'EINT_25', 'EINT_26', 'EINT_27',
                       'EINT_20', 'EINT_21', 'EINT_22', 'EINT_23']
    ind_descriptions = {
        'B2:SPI1': 'Used for 320x240 or 640x480 etc. SPI-based LCD.\n'
        'Frees up large numbers of GPIO from RGB/TTL bank'
    }
    unused_pins = check_functions("Industrial with SPI-LCD",
                                  bankspec, fns, pinouts,
                                  industrial, industrial_eint, industrial_pwm,
                                  ind_descriptions)

    # Smartphone / Tablet - basically the same thing

    tablet = ['B1:LCD/22', 'ULPI1/8', 'ULPI2/8',
              'MMC', 'SD1',
              'F1:IIS',  # I2C Audio
              'TWI2',   # I2C Audio
              'E2:UART1',  # WIFI/BT
              'E2:SD2',   # WIFI
              'C3:UART0',  # GPS
              'D2:UART3',
              'D2:UART4',
              'D3:TWI1', 'D2:TWI3', 'SPI2', 'QSPI']
    tablet_pwm = ['F2:PWM_0',  # LCD_BACKLIGHT
                  'F2:PWM_1', 'D1:PWM_2']
    tablet_eint = ['EINT_24',  # BT_HOST_WAKE
                   'EINT_25',  # WIFI_HOST_WAKE
                   'EINT_26',  # CTP_INT
                   'EINT_27',  # GSENSOR_INT
                   'EINT_8',  # GPS_INT
                   'EINT_7',  # TILT_SENSOR_INT
                   'EINT_22',  # COMPASS_INT
                   'EINT_23',  # MCU_INT
                   'EINT_16',  # PMIC_INT
                   'EINT_17',  # PWR_BUTTON_INT
                   'EINT_30',  # OTG_ID
                   'EINT_31',
                   ]
    descriptions = {
        'B1:LCD/22':
        'RGB/TTL LCD, 800x480 or use SN75LVDS83b for up to 1440x900',
        'MMC': 'eMMC: main internal storage',
        'ULPI1/8': 'USB-OTG, connect to ULPI OTG PHY (for charging)\n'
                   'as well as USB Host or USB Device',
        'ULPI2/8': 'USB2 Host, connect to ULPI PHY w/and 4-port USB2 Hub\n'
        'for example GL850G or FE1.1. '
        'Connects to 2/3/4G/LTE Modem, 2x USB-Camera (VC0345)',
        'SD1': 'internal, multiplexed with JTAG1\n'
               'and UART2, for debug purposes',
        'F1:IIS': 'I2C Audio, connect to AC97 Audio IC',
        'TWI2': 'Connect to AC97 Audio IC',
        'E2:UART1': 'Connect to BT on AP6234/AP6335',
        'E2:SD2': 'Connect to WIFI on AP6234/AP6335',
        'QSPI': 'Boot Storage (connection to companion / debug / boot MCU)\n'
                'Only actually needs MISO/MOSI, bootstrap loader v. small\n'
                'Bootstrap loader checks eMMC, USB-OTG, SD/MMC, SPI, etc.',
        'SPI2': 'Spare? SPI, connect to higher-speed sensor?',
        'D2:UART3': 'Spare? UART (or 2 extra GPIO / EINT)',
        'D2:UART4': 'Spare? UART (or 2 extra GPIO)',
        'D3:TWI1': 'Connect to PMIC',
        'D2:TWI3': 'Connect to sensors (Trackpad? CTP GSENSOR TILT COMPASS)',
        'GPIO': '9 spare GPIO pins for miscellaneous functions:\n'
                'wake-up of BT, WIFI, LCD power, sensor power etc.\n'
                '4 GPIO may be needed for PWM Audio from Modem.\n'
                'LED lights for camera will be needed.\n'
                'Some phones may have clam-shell or lid switch.\n'
                'Some Modems have spare GPIO (over AT commandset).\n'
                'AXP209 PMIC has 4x GPIO, accessible over I2C.\n'
                'SPI2, UART3-4, PWM1-2 may also be spare (10 extra GPIO).\n'
                'If more needed, companion MCU may be used (48+ pin variant)\n'
                'which also includes ADC, DAC, more PWM etc.',
        'F2:PWM_0': 'LCD Backlight',
        'F2:PWM_1': 'Spare? PWM (or extra GPIO / EINT)',
        'D1:PWM_2': 'Spare? PWM (or extra GPIO / EINT)',
        'EINT_24': 'BT_HOST_WAKE',
        'EINT_25': 'WIFI_HOST_WAKE',
        'EINT_26': 'CTP_INT',
        'EINT_27': 'GSENSOR_INT',
        'EINT_8': 'GPS_INT',
        'EINT_7': 'TILT_SENSOR_INT',
        'EINT_22': 'COMPASS_INT',
        'EINT_23': 'MCU_INT',
        'EINT_16': 'PMIC_INT',
        'EINT_17': 'PWR_BUTTON_INT',
        'EINT_30': 'OTG_ID',
        'EINT_31': 'Spare?',
    }
    unused_pins = check_functions("Smartphone / Tablet",
                                  bankspec, fns, pinouts,
                                  tablet, tablet_eint, tablet_pwm,
                                  descriptions)

    # Laptop

    laptop = ['D1:FB/17', 'E1:FB/8', 'B1:LCD/22', 'ULPI1/8', 'ULPI2/8',
              'MMC', 'SD1',
              'F1:IIS',  # I2C Audio
              'TWI2',   # I2C Audio
              'E2:UART1',  # WIFI/BT
              'E2:SD3',   # WIFI
              'D2:TWI3', 'QSPI']
    laptop_pwm = ['F2:PWM_0',  # LCD_BACKLIGHT
                  ]
    laptop_eint = ['EINT_20',  # BT_HOST_WAKE
                   'EINT_21',  # WIFI_HOST_WAKE
                   'EINT_9',  # MCU_INT
                   'EINT_31',  # PMIC_INT
                   ]
    descriptions = {
        'D1:FB/17': 'FlexBus.  Connect to DM9000 or AX99896A MCU-style Bus\n'
        '10/100 Ethernet PHY.',
        'E1:FB/8': 'FlexBus bus bits 8-15, needed to make a 16-bit bus width',
        'B1:LCD/22': 'RGB/TTL LCD, use SN75LVDS83b for '
                     'LVDS or SSD2828 for MIPI,\n'
        'or a Chrontel CH7039, CH7038, CH7034 or CH7018 for dual\n'
        'display output (eDP/LVDS and HDMI/VGA) '
        'conversion.',
        'MMC': 'eMMC: main internal storage',
        'ULPI1/8': 'USB-OTG, connect to ULPI OTG PHY (for charging)\n'
        'as well as USB Host or USB Device',
        'ULPI2/8': 'USB2 Host, connect to ULPI PHY w/and 4-port USB2 Hub\n'
        'for example GL850G or FE1.1. '
        'Connects to USB-Camera (VC0345 and 3x external USB Ports)',
        'SD1': 'internal, multiplexed with JTAG1\n'
        'and UART2, for debug purposes',
        'F1:IIS': 'I2C Audio, connect to AC97 Audio IC',
        'TWI2': 'Connect to AC97 Audio IC',
        'E2:UART1': 'Connect to BT on AP6234/AP6335',
        'E2:SD3': 'Connect to WIFI on AP6234/AP6335',
        'QSPI': 'Boot Storage (connection to companion / debug / boot MCU)\n'
        'Only actually needs MISO/MOSI, bootstrap loader v. small\n'
        'Bootstrap loader checks eMMC, USB-OTG, SD/MMC, SPI, etc.\n'
        'MCU implements keyboard-matrix for keyboard (also trackpad?)',
        'D2:TWI3': 'Connect to PMIC',
        'GPIO': 'Plenty of spare GPIO pins for miscellaneous functions\n'
        'MCU EINT-capable GPIO may be used to generate extra EINTs\n'
        'on the single MCU_INT line, if really needed',
        'F2:PWM_0': 'LCD Backlight',
        'EINT_20': 'BT_HOST_WAKE',
        'EINT_21': 'WIFI_HOST_WAKE',
        'EINT_9': 'MCU_INT',
        'EINT_31': 'PMIC_INT',
    }
    unused_pins = check_functions("Laptop / Netbook",
                                  bankspec, fns, pinouts,
                                  laptop, laptop_eint, laptop_pwm,
                                  descriptions)

    # IoT

    iot = ['B1:LCD', 'ULPI2/8', 'ULPI1/8',
           'MMC', 'SD1',
           'F1:IIS',  # I2C Audio
           #'TWI2',   # I2C Audio
           'C3:UART0',  # HSPA UART
           'E2:UART1',  # BT UART
           'C2:SPI2',  # HSPI SPI
           'E2:SD3',   # WIFI
           'D3:TWI1',  # sensors CTP,
           'D2:TWI3', 'QSPI']
    iot_pwm = ['F2:PWM_0',  # LCD_BACKLIGHT
               ]
    iot_eint = ['EINT_5',  # 'HSPA_MST_RDY',
                'EINT_6',  # 'HSPA_SL_RDY',
                'EINT_7',  # 'HSPA_RING',
                'EINT_8',  # 'WL_PMU_EN',
                'EINT_9',  # HSPA_GPIO1
                'EINT_10',  # IR_DT
                'EINT_11',  # 'BT_PCM_CLK',
                'EINT_12',  # 'BT_PCM_DIN',
                'EINT_13',  # 'BT_PCM_SYNC',
                'EINT_14',  # 'BT_PCM_DOUT',
                'EINT_16',  # 'USB_DRVVBUS',
                'EINT_17',  # 'USB_VBUSDET',
                'EINT_21',  # 'USB_ID',
                'EINT_30',  # 'CTP_INT',
                'EINT_31',  # 'SD_DET#',
                ]
    descriptions = {
        'B1:LCD':
        'RGB/TTL LCD, use SN75LVDS83b for LVDS or SSD2828 for MIPI,\n'
        'or a Chrontel CH7039, CH7038, CH7034 or CH7018 for dual\n'
        'display output (eDP/LVDS and HDMI/VGA) '
        'conversion.',
        'MMC': 'eMMC: main internal storage',
        'F1:IIS': 'I2C Audio, connect to AC97 Audio IC',
        'ULPI2/8': 'USB-OTG, connect to ULPI OTG PHY (for charging)\n'
                   'as well as USB Host or USB Device',
        'ULPI1/8': 'USB2 Host, connect to ULPI PHY',
        'SD1': 'internal, multiplexed with JTAG1\n'
               'and UART2, for debug purposes',
        'C3:UART0': 'Connect to HSPA UART',
        'E2:UART1': 'Connect to BT UART',
        'E2:SD3': 'Connect to WIFI',
        'C2:SPI2': 'HSPA SPI',
        'QSPI': 'Boot Storage (connection to companion / debug / boot MCU)\n'
                'Only actually needs MISO/MOSI, bootstrap loader v. small\n'
                'Bootstrap loader checks eMMC, USB-OTG, SD/MMC, SPI, etc.\n'
                'MCU implements keyboard-matrix for keyboard (also trackpad?)',
        'D2:TWI3': 'Connect to PMIC',
        'D3:TWI1': 'Connect to sensors CTP',
        'GPIO': 'Plenty of spare GPIO pins for miscellaneous functions\n'
                'MCU EINT-capable GPIO may be used to generate extra EINTs\n'
                'on the single MCU_INT line, if really needed',
        'F2:PWM_0': 'LCD Backlight',
        'GPIOD_D4': 'WL_WAKE_AP',
        'GPIOD_D5': 'BT_WAKE_AP',
        'GPIOD_D6': 'AP_WAKE_BT',
        'GPIOD_D7': 'AP_CK32KO',
        'GPIOD_D8': 'HSPA_PWRON',
        'GPIOD_D9': 'BT_RST_N',
        'GPIOE_E5': 'HSPA_ON_OFF',
        'GPIOD_D2': 'HSPA_SHUTDOWN',
        'GPIOD_D3': 'CTP_RST',
        'GPIOD_D12': 'LCD_RDN',
        'GPIOD_D17': 'LCD_WRN',
        'GPIOD_D18': 'LCD_RS',
        'GPIOD_D21': 'LCD_CSN',

        'EINT_5': 'HSPA_MST_RDY',
        'EINT_6': 'HSPA_SL_RDY',
        'EINT_7': 'HSPA_RING',
        'EINT_8': 'WL_PMU_EN',
        'EINT_9': 'HSPA_GPIO1',
        'EINT_10': 'IR_DT',
        'EINT_11': 'BT_PCM_CLK',
        'EINT_12': 'BT_PCM_DIN',
        'EINT_13': 'BT_PCM_SYNC',
        'EINT_14': 'BT_PCM_DOUT',

        'EINT_16': 'USB_DRVVBUS',
        'EINT_17': 'USB_VBUSDET',
        'EINT_21': 'USB_ID',
        'EINT_30': 'CTP_INT',
        'EINT_31': 'SD_DETN',
    }
    unused_pins = check_functions("IoT",
                                  bankspec, fns, pinouts,
                                  iot, iot_eint, iot_pwm,
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
