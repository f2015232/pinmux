# === templates for interface definitions ====== #
mux_interface_def = '''
      method Action cell{0}_mux (Bit#({1}) in );
         wrmux{0}<=in;
      endmethod
'''
io_interface_def = '''
      method io_outputval_{0}=cell{0}_out.outputval;
      method io_output_en_{0}=cell{0}_out.output_en;
      method io_input_en_{0}=cell{0}_out.input_en;
      method io_pullup_en_{0}=cell{0}_out.pullup_en;
      method io_pulldown_en_{0}=cell{0}_out.pulldown_en;
      method io_drivestrength_{0}=cell{0}_out.drivestrength;
      method io_pushpull_en_{0}=cell{0}_out.pushpull_en;
      method io_opendrain_en_{0}=cell{0}_out.opendrain_en;
      method Action  io_inputval_{0}(Bit#(1) in);
         cell{0}_in<=in;
      endmethod
'''
uartinterface_def = '''
      method rx_{0}=wruart{0}_rx;
      method Action tx_{0}(Bit#(1) in);
         wruart{0}_tx<=in;
      endmethod
'''
spiinterface_def = '''
      method Action sclk_{0} (Bit#(1) in);
         wrspi{0}_sclk<=in;
      endmethod
      method Action mosi_{0} (Bit#(1) in);
         wrspi{0}_mosi<=in;
      endmethod
      method Action ss_{0}   (Bit#(1) in);
         wrspi{0}_ss<=in;
      endmethod
      method Bit#(1) miso_{0}=wrspi{0}_miso;
'''

twiinterface_def = '''

      method Action sda{0}_out (Bit#(1) in);
         wrtwi{0}_sda_out<=in;
      endmethod
      method Action sda{0}_outen (Bit#(1) in);
         wrtwi{0}_sda_outen<=in;
      endmethod
      method sda{0}_in=wrtwi{0}_sda_in;

      method Action scl{0}_out (Bit#(1) in);
         wrtwi{0}_scl_out<=in;
      endmethod
      method Action scl{0}_outen (Bit#(1) in);
         wrtwi{0}_scl_outen<=in;
      endmethod
      method scl{0}_in=wrtwi{0}_scl_in;

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
      method Action pwm{0}(Bit#(1) in);
        wrpwm{0}<=in;
      endmethod
'''
# ============================================== #
