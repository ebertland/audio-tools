PREFIX := $(HOME)/tools

all:
	install -D backup-tags.py $(PREFIX)/bin/backup-tags
	ln -f $(PREFIX)/bin/backup-tags $(PREFIX)/bin/restore-tags
	install -D copy-tags.py $(PREFIX)/bin/copy-tags
	install -D fix-mb-tags.py $(PREFIX)/bin/fix-mb-tags
	install -D replaygain-id3v2.sh $(PREFIX)/bin/replaygain-id3v2
