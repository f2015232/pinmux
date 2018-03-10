from params import *
#== Actual pinmuxing ==# TODO: Need to get this as a templete
pinmux='''
		/*=============== THIS IS WHERE ACTUAL MUXING HAPPENS ==========*/
		cell0_out=wrmux0==0?uart0_rx_io:uart1_rx_io;
		rule get_input_for_rx;
			if(wrmux0==0)
				wruart0_rx<=cell0_in;
			else
				wruart1_rx<=cell0_in;
		endrule
		cell1_out=wrmux1==0?uart0_tx_io:uart1_tx_io;
		/*==============================================================*/
'''
########################################################################


