# == Parameters == #
N_MUX = 1		# number of selection lines for the mux per io
N_IO = 0
N_MUX_IO = 0
N_UART = 4
N_SPI = 1
N_TWI = 2
# ================ #
# == capture the number of IO cells required == #
pinmapfile = open('pinmap.txt', 'r')
max_io = 0
muxed_cells = []
dedicated_cells = []
for lineno, line in enumerate(pinmapfile):
    line1 = line.split()
    if(len(line1) > 1):
        if(len(line1) == 2):  # dedicated
            dedicated_cells.append(line1)
        if(len(line1) > 2):
            muxed_cells.append(line1)
# ============================================= #

# ======= Multiple checks to see if the user has not screwed ======#

# Check-1: ensure that no pin is present in both muxed and dedicated pins
for muxcell in muxed_cells:
    for dedcel in dedicated_cells:
        if(dedcel[1] in muxcell):
            print("ERROR: " + str(dedcel[1]) + " present \
                                  in dedicated & muxed lists")
            exit(1)
# Check-2: confirm if N_* matches the instances in the pinmap
# ============================================================== #

# == user info after parsin ================= #
N_IO = len(dedicated_cells) + len(muxed_cells)
print("Max number of IO: " + str(N_IO))
print("Muxed IOs: " + str(len(muxed_cells)))
print("Dedicated IOs: " + str(len(dedicated_cells)))
# ============================================ #
