### Makefile for the cclass project (test)

default: gen_pinmux gen_verilog


########## BSIM COMPILE, LINK AND SIMULATE TARGETS ##########################
.PHONY: gen_pinmux
gen_pinmux: 
	@python ./src/pinmux_generator.py -v -o test

.PHONY: gen_verilog 
gen_verilog:
	make -C test gen_verilog

#############################################################################

.PHONY: clean
clean:
	make -C test clean
	find . -name "*.pyc" | xargs rm -f
	find . -name "__pycache__" | xargs rm -fr

pep8:
	autopep8 -a -a -a --experimental -r -i src
