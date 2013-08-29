# $Id$

PREFIX := $(HOME)/tools
SCRIPTS := $(wildcard *.py *.sh)

all:
	for script in $(SCRIPTS); do \
	    install -D $$script $(PREFIX)/bin/$${script%.*}; \
	done
	# restore-tags runs backup-tags in restore mode.
	ln -f $(PREFIX)/bin/backup-tags $(PREFIX)/bin/restore-tags
	install -D abcde.conf $(HOME)/.abcde.conf
