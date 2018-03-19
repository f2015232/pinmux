# == Intermediate wire definitions ==#
muxwire = '''
      Wire#(Bit#({1}))   wrmux{0} <-mkDWire(0);'''
generic_io = '''
      GenericIOType cell{0}_out=unpack(0);
      Wire#(Bit#(1)) cell{0}_in <-mkDWire(0);
'''
uartwires = '''
      Wire#(Bit#(1)) wruart{0}_rx <-mkDWire(0);
      Wire#(Bit#(1)) wruart{0}_tx <-mkDWire(0);
      GenericIOType uart{0}_rx_io=GenericIOType{{outputval:0, output_en:0,
                input_en:1, pullup_en:0, pulldown_en:0, pushpull_en:0,
                drivestrength:0, opendrain_en:0}};
      GenericIOType uart{0}_tx_io=GenericIOType{{outputval:wruart{0}_tx,
                output_en:1, input_en:0, pullup_en:0, pulldown_en:0,
                pushpull_en:0, drivestrength:0, opendrain_en:0}};
'''
spiwires = '''
      Wire#(Bit#(1)) wrspi{0}_sclk <-mkDWire(0);
      Wire#(Bit#(1)) wrspi{0}_mosi <-mkDWire(0);
      Wire#(Bit#(1)) wrspi{0}_ss   <-mkDWire(0);
      Wire#(Bit#(1)) wrspi{0}_miso <-mkDWire(0);
      GenericIOType spi{0}_sclk_io = GenericIOType{{outputval:wrspi{0}_sclk,
                output_en:1, input_en:0, pullup_en:0, pulldown_en:0,
                pushpull_en:0, drivestrength:0, opendrain_en:0}};
      GenericIOType spi{0}_mosi_io = GenericIOType{{outputval:wrspi{0}_mosi,
                output_en:1, input_en:0, pullup_en:0, pulldown_en:0,
                pushpull_en:0, drivestrength:0, opendrain_en:0}};
      GenericIOType spi{0}_ss_io = GenericIOType{{outputval:wrspi{0}_ss,
                output_en:1, input_en:0, pullup_en:0, pulldown_en:0,
                pushpull_en:0, drivestrength:0, opendrain_en:0}};
      GenericIOType spi{0}_miso_io = GenericIOType{{outputval:0, output_en:0,
                input_en:1, pullup_en:0, pulldown_en:0, pushpull_en:0,
                drivestrength:0, opendrain_en:0}};

'''
twiwires = '''
      Wire#(Bit#(1)) wrtwi{0}_sda_out<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi{0}_sda_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi{0}_sda_in<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi{0}_scl_out<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi{0}_scl_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi{0}_scl_in<-mkDWire(0);
      GenericIOType  twi{0}_sda_io = GenericIOType{{outputval:wrtwi{0}_sda_out,
                output_en:wrtwi{0}_sda_outen, input_en:~wrtwi{0}_sda_outen,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
      GenericIOType  twi{0}_scl_io = GenericIOType{{outputval:wrtwi{0}_scl_out,
                output_en:wrtwi{0}_scl_outen, input_en:~wrtwi{0}_scl_outen,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
'''

sdwires = '''
      Wire#(Bit#(1)) wrsd{0}_clk <-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_cmd <-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d0_out<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d0_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d0_in<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d1_out<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d1_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d1_in<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d2_out<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d2_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d2_in<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d3_out<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d3_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrsd{0}_d3_in<-mkDWire(0);
      GenericIOType  sd{0}_clk_io = GenericIOType{{outputval:wrsd{0}_clk,
                output_en:1, input_en:0,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
      GenericIOType  sd{0}_cmd_io = GenericIOType{{outputval:wrsd{0}_cmd,
                output_en:1, input_en:0,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
      GenericIOType  sd{0}_d0_io = GenericIOType{{outputval:wrsd{0}_d0_out,
                output_en:wrsd{0}_d0_outen, input_en:~wrsd{0}_d0_outen,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
      GenericIOType  sd{0}_d1_io = GenericIOType{{outputval:wrsd{0}_d1_out,
                output_en:wrsd{0}_d1_outen, input_en:~wrsd{0}_d1_outen,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
      GenericIOType  sd{0}_d2_io = GenericIOType{{outputval:wrsd{0}_d2_out,
                output_en:wrsd{0}_d2_outen, input_en:~wrsd{0}_d2_outen,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
      GenericIOType  sd{0}_d3_io = GenericIOType{{outputval:wrsd{0}_d3_out,
                output_en:wrsd{0}_d3_outen, input_en:~wrsd{0}_d3_outen,
                pullup_en:0, pulldown_en:0, pushpull_en:0, drivestrength:0,
                opendrain_en:0}};
'''

jtagwires = '''
      Wire#(Bit#(1)) wrjtag{0}_tdi<-mkDWire(0);
      Wire#(Bit#(1)) wrjtag{0}_tms<-mkDWire(0);
      Wire#(Bit#(1)) wrjtag{0}_tclk<-mkDWire(0);
      Wire#(Bit#(1)) wrjtag{0}_trst<-mkDWire(0);
      Wire#(Bit#(1)) wrjtag{0}_tdo<-mkDWire(0);
      GenericIOType jtag{0}_tdi_io=GenericIOType{{outputval:0, output_en:0,
                input_en:1, pullup_en:0, pulldown_en:0, pushpull_en:0,
                drivestrength:0, opendrain_en:0}};
      GenericIOType jtag{0}_tdo_io=GenericIOType{{outputval:wrjtag{0}_tdo,
                output_en:1, input_en:0, pullup_en:0, pulldown_en:0,
                pushpull_en:0, drivestrength:0, opendrain_en:0}};
      GenericIOType jtag{0}_tms_io=GenericIOType{{outputval:0, output_en:0,
                input_en:1, pullup_en:0, pulldown_en:0, pushpull_en:0,
                drivestrength:0, opendrain_en:0}};
      GenericIOType jtag{0}_trst_io=GenericIOType{{outputval:0, output_en:0,
                input_en:1, pullup_en:0, pulldown_en:0, pushpull_en:0,
                drivestrength:0, opendrain_en:0}};
      GenericIOType jtag{0}_tclk_io=GenericIOType{{outputval:0, output_en:0,
                input_en:1, pullup_en:0, pulldown_en:0, pushpull_en:0,
                drivestrength:0, opendrain_en:0}};
'''

pwmwires = '''
      Wire#(Bit#(1)) wrpwm{0} <-mkDWire(0);
      GenericIOType pwm{0}_io=GenericIOType{{outputval:wrpwm{0},
                output_en:1, input_en:0, pullup_en:0, pulldown_en:0,
                pushpull_en:0, drivestrength:0, opendrain_en:0}};
'''
# =================================== #
