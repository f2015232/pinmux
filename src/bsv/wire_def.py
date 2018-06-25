# == Intermediate wire definitions, special cases ==#
muxwire = '''
      Wire#({1}) wrcell{0}_mux<-mkDWire(0);'''
generic_io = '''
      Wire#(Bit#(1)) cell{0}_mux_out<-mkDWire(0);
      Wire#(Bit#(1)) cell{0}_mux_outen<-mkDWire(0);
      Wire#(Bit#(1)) cell{0}_mux_in<-mkDWire(0);
'''
