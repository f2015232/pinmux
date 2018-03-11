from params import *
from string import digits


## dictionary of properties of signals that are supported.
dictionary={
	"uart_rx":"input",
	"uart_tx":"output",
	"spi_sclk":"output",
	"spi_mosi":"output",
	"spi_ss": "output",
	"spi_miso":"input"
}
	

########### common bsv templates ############
assign_cell='''cell{0}_out=wrmux{0}=={1}?'''
# first argument is the io-cell number being assigned. 
# second argument is the mux value. 
# Third argument is the signal from the pinmap file
input_wire='''		
		rule assign_input_for_{2}(wrmux{0}=={1});
			wr{2}<=cell{0}_in;
		endrule
'''
#########################################
pinmux=''' '''
pinmap_file=open("./pinmap.txt","r")
for lineno,line in enumerate(pinmap_file):
	line1=line.split()
	if(lineno>0):
		if(lineno>N_IO):
			print"ERROR: Parameter N_IO("+str(N_IO)+") is less than the pin number in line: "+str(lineno)+" of pinmap.txt"
			exit(1)
		######## Mux each generic IO cell with the mapping######
		# provided in the pinmap file
		pinmux=pinmux+"		cell"+str(line1[0])+"_out="
		i=0
		while(i<len(line1)-1):
			pinmux=pinmux+"wrmux"+str(line1[0])+"=="+str(i)+"?"+line1[i+1]+"_io:"
			if(i+2==len(line1)-1):
				pinmux=pinmux+line1[i+2]+"_io"
				i=i+2
			else:
				i=i+1
		pinmux=pinmux+";\n"
		########################################################

		###### check each cell if "peripheral input/inout" then assign its wire ########
		## Here we check the direction of each signal in the dictionary. 
		## We choose to keep the dictionary within the code and not user-input 
		## since the interfaces are always standard and cannot change from user-to-user
		## plus reduces human-error as well :)
		for i in range(0,len(line1)-1):
			temp=line1[i+1].translate(None,digits)
			x=dictionary.get(temp);
			if(x==None):
				print "Error: The signal : "+str(line1[i+1])+" in lineno: "+str(lineno)+"of pinmap.txt is not present in the current dictionary.\nSoln: Either update the dictionary or fix typo."
				exit(1)
			if(x=="input"):
				pinmux=pinmux+input_wire.format(line1[0],i,line1[i+1])+"\n"
		################################################################################
###########################################

