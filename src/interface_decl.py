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
# ======================================= #
