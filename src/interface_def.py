# === templates for interface definitions ====== #
mux_interface_def = '''
      method Action  cell{0}_mux(Bit#({1}) in);
         wrcell{0}_mux<=in;
      endmethod
'''
io_interface_def = '''
      method io_outputval_{0}=cell{0}_mux_out.outputval;
      method io_output_en_{0}=cell{0}_mux_out.output_en;
      method io_input_en_{0}=cell{0}_mux_out.input_en;
      method io_pullup_en_{0}=cell{0}_mux_out.pullup_en;
      method io_pulldown_en_{0}=cell{0}_mux_out.pulldown_en;
      method io_drivestrength_{0}=cell{0}_mux_out.drivestrength;
      method io_pushpull_en_{0}=cell{0}_mux_out.pushpull_en;
      method io_opendrain_en_{0}=cell{0}_mux_out.opendrain_en;
      method Action  io_inputval_{0}(Bit#(1) in);
         cell{0}_mux_in<=in;
      endmethod
'''
uartinterface_def = '''
      method uart{0}_rx=wruart{0}_rx;
      method Action uart{0}_tx(Bit#(1) in);
         wruart{0}_tx<=in;
      endmethod
'''
spiinterface_def = '''
      method Action spi{0}_sclk (Bit#(1) in);
         wrspi{0}_sclk<=in;
      endmethod
      method Action spi{0}_mosi (Bit#(1) in);
         wrspi{0}_mosi<=in;
      endmethod
      method Action spi{0}_nss   (Bit#(1) in);
         wrspi{0}_nss<=in;
      endmethod
      method Bit#(1) spi{0}_miso=wrspi{0}_miso;
'''

twiinterface_def = '''

      method Action twi{0}_sda_out (Bit#(1) in);
         wrtwi{0}_sda_out<=in;
      endmethod
      method Action twi{0}_sda_outen (Bit#(1) in);
         wrtwi{0}_sda_outen<=in;
      endmethod
      method twi{0}_sda_in=wrtwi{0}_sda_in;

      method Action twi{0}_scl_out (Bit#(1) in);
         wrtwi{0}_scl_out<=in;
      endmethod
      method Action twi{0}_scl_outen (Bit#(1) in);
         wrtwi{0}_scl_outen<=in;
      endmethod
      method twi{0}_scl_in=wrtwi{0}_scl_in;

'''

sdinterface_def = '''
      method Action sd{0}_clk (Bit#(1) in);
        wrsd{0}_clk<=in;
      endmethod
      method Action sd{0}_cmd (Bit#(1) in);
        wrsd{0}_cmd<=in;
      endmethod
      method Action sd{0}_d0_out (Bit#(1) in);
        wrsd{0}_d0_out<=in;
      endmethod
      method Action sd{0}_d0_outen (Bit#(1) in);
        wrsd{0}_d0_outen<=in;
      endmethod
      method sd{0}_d0_in=wrsd{0}_d0_in;
      method Action sd{0}_d1_out (Bit#(1) in);
        wrsd{0}_d1_out<=in;
      endmethod
      method Action sd{0}_d1_outen (Bit#(1) in);
        wrsd{0}_d1_outen<=in;
      endmethod
      method sd{0}_d1_in=wrsd{0}_d1_in;
      method Action sd{0}_d2_out (Bit#(1) in);
        wrsd{0}_d2_out<=in;
      endmethod
      method Action sd{0}_d2_outen (Bit#(1) in);
        wrsd{0}_d2_outen<=in;
      endmethod
      method sd{0}_d2_in=wrsd{0}_d2_in;
      method Action sd{0}_d3_out (Bit#(1) in);
        wrsd{0}_d3_out<=in;
      endmethod
      method Action sd{0}_d3_outen (Bit#(1) in);
        wrsd{0}_d3_outen<=in;
      endmethod
      method sd{0}_d3_in=wrsd{0}_d3_in;
'''

jtaginterface_def = '''
      method Bit#(1) jtag{0}_tdi=wrjtag{0}_tdi;
      method Bit#(1) jtag{0}_tms=wrjtag{0}_tms;
      method Bit#(1) jtag{0}_tclk=wrjtag{0}_tclk;
      method Bit#(1) jtag{0}_trst=wrjtag{0}_trst;
      method Action jtag{0}_tdo(Bit#(1) in);
        wrjtag{0}_tdo<=in;
      endmethod
'''

pwminterface_def = '''
      method Action pwm{0}_pwm(Bit#(1) in);
        wrpwm{0}_pwm<=in;
      endmethod
'''
# ============================================== #
