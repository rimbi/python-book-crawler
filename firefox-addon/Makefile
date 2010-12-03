.PHONY: clean all

DIRECTORY = KitapSever
ZIP = $(shell which zip)

all: kitapsever.xpi

kitapsever.xpi:
	cd $(DIRECTORY); \
	$(ZIP) -r ../$@ *

clean:
	-rm *.xpi