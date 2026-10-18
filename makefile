SHELL := /bin/bash
EXECUTABLE := morfeo
MORFEO := $(shell which ${EXECUTABLE})

test: clean
	@python3 opener.py
	@cd ./Run1; ${MORFEO} input.dat
	#@cd ./Run2; ${MORFEO} input.dat

clean:
	@rm -rf Run* Material*
	$(info Done cleaning)
