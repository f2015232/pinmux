import math
# == Parameters == #
N_MUX = 1		# number of selection lines for the mux per io
N_IO = 0
N_MUX_IO = 0
N_UART = 4
N_SPI = 1
N_TWI = 2
N_SD = 2
N_JTAG = 2
Addressing = 'WORD'
ADDR_WIDTH = 32
DATA_WIDTH = 32
# ================ #

# Generating the number of bits for memory map #
lower_offset = 0
if(Addressing == 'BYTE'):
    lower_offset = 0
elif(Addressing == 'HWORD'):
    lower_offset = 1
elif(Addressing == 'WORD'):
    lower_offset = 2
elif(Addressing == 'DWORD'):
    lower_offset = 3
else:
    print('ERROR: Addressing should be one of: BYTE, HWORD, WORD, DWORD')
    exit(1)


def missing_numbers(num_list):
    original_list = [x for x in range(num_list[0], num_list[-1] + 1)]
    num_list = set(num_list)
    return (list(num_list ^ set(original_list)))


# == capture the number of IO cells required == #
pinmapfile = open('pinmap.txt', 'r')
max_io = 0
muxed_cells = []
dedicated_cells = []
pinnumbers = []
for lineno, line in enumerate(pinmapfile):
    line1 = line.split()
    if(len(line1) > 1):
        pinnumbers.append(int(line1[0]))
        if(len(line1) == 2):  # dedicated
            dedicated_cells.append(line1)
        if(len(line1) > 2):
            muxed_cells.append(line1)
pinnumbers = sorted(pinnumbers)

upper_offset = lower_offset + int(math.log(len(muxed_cells), 2))
# ============================================= #
# ======= Multiple checks to see if the user has not screwed ======#
missing_pins = missing_numbers(pinnumbers)

# Check-1: ensure that no pin is present in both muxed and dedicated pins
for muxcell in muxed_cells:
    for dedcel in dedicated_cells:
        if(dedcel[1] in muxcell):
            print("ERROR: " + str(dedcel[1]) + " present \
                                  in dedicated & muxed lists")
            exit(1)

# Check-2: if pin numbering is consistent:
if missing_pins:
    print("ERROR: Following pins have no assignment: " +
          str(missing_numbers(pinnumbers)))
    exit(1)
unique = set(pinnumbers)
duplicate = False
for each in unique:
    count = pinnumbers.count(each)
    if(count > 1):
        print("ERROR: Multiple assignment for pin: " + str(each))
        duplicate = True
if(duplicate):
    exit(1)

# Check-2: confirm if N_* matches the instances in the pinmap
# ============================================================== #

# == user info after parsin ================= #
N_IO = len(dedicated_cells) + len(muxed_cells)
print("Max number of IO: " + str(N_IO))
print("Muxed IOs: " + str(len(muxed_cells)))
print("Dedicated IOs: " + str(len(dedicated_cells)))
# ============================================ #
