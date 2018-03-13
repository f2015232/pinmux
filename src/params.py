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

# check if the user has not screwed up by ensuring that no pin is
# present in both muxed and dedicated pins
# TODO

# =========================================== #
N_IO = len(dedicated_cells) + len(muxed_cells)
print("Max number of IO: " + str(N_IO))
print("Muxed IOs: " + str(len(muxed_cells)))
print("Dedicated IOs: " + str(len(dedicated_cells)))
# ============================================ #
