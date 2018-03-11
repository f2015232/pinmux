from params import *
#== Intermediate wire definitions ==#
muxwire='''
		Wire#(Bit#('''+str(N_MUX)+'''))	wrmux{0} <-mkDWire(0);'''
generic_io='''
		GenericIOType cell{0}_out=unpack(0);
		Wire#(Bit#(1)) cell{0}_in <-mkDWire(0);
'''
uartwires='''
		Wire#(Bit#(1)) wruart{0}_rx <-mkDWire(0);
		Wire#(Bit#(1)) wruart{0}_tx <-mkDWire(0);
		GenericIOType uart{0}_rx_io=GenericIOType{{outputval:0, output_en:0, input_en:1,
															   pullup_en:0, pulldown_en:0, pushpull_en:0,
																drivestrength:0, opendrain_en:0}};
		GenericIOType uart{0}_tx_io=GenericIOType{{outputval:wruart{0}_tx, output_en:1, input_en:0,
															   pullup_en:0, pulldown_en:0, pushpull_en:0,
																drivestrength:0, opendrain_en:0}};
'''
spiwires='''
		Wire#(Bit#(1)) wrspi{0}_sclk <-mkDWire(0);
		Wire#(Bit#(1)) wrspi{0}_mosi <-mkDWire(0);
		Wire#(Bit#(1)) wrspi{0}_ss	  <-mkDWire(0);
		Wire#(Bit#(1)) wrspi{0}_miso <-mkDWire(0);
		GenericIOType spi{0}_sclk_io = GenericIOType{{outputval:wrspi{0}_sclk, output_en:1, input_en:0,
															   pullup_en:0, pulldown_en:0, pushpull_en:0,
																drivestrength:0, opendrain_en:0}};
		GenericIOType spi{0}_mosi_io = GenericIOType{{outputval:wrspi{0}_mosi, output_en:1, input_en:0,
															   pullup_en:0, pulldown_en:0, pushpull_en:0,
																drivestrength:0, opendrain_en:0}};
		GenericIOType spi{0}_ss_io = GenericIOType{{outputval:wrspi{0}_ss, output_en:1, input_en:0,
															   pullup_en:0, pulldown_en:0, pushpull_en:0,
																drivestrength:0, opendrain_en:0}};
		GenericIOType spi{0}_miso_io = GenericIOType{{outputval:0, output_en:0, input_en:1,
															   pullup_en:0, pulldown_en:0, pushpull_en:0,
																drivestrength:0, opendrain_en:0}};
		
'''
#===================================#

