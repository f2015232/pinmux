from params import *
#=== templates for interface definitions ======#
mux_interface_def='''
		method Action cell{0}_mux (Bit#('''+str(N_MUX)+''') in );
			wrmux{0}<=in;
		endmethod
'''
io_interface_def='''
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
uartinterface_def='''
		method rx_{0}=wruart{0}_rx;
		method Action tx_{0}(Bit#(1) in);
			wruart{0}_tx<=in;
		endmethod
'''
spiinterface_def='''
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
#==============================================#


