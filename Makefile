# Makefile for darcs-hooks
#
# Copyright (C) 2007 Miklos Vajna <vmiklos@frugalware.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

VERSION = 0.1.0

INSTALL = /usr/bin/install -c
DESTDIR =
bindir = /usr/bin
sysconfdir = /etc/darcs-hooks
shareddir = /usr/share/darcs-hooks

compile:

install:
	$(INSTALL) -d $(DESTDIR)$(bindir)
	$(INSTALL) -d $(DESTDIR)$(sysconfdir)
	$(INSTALL) darcs-hooks.py $(DESTDIR)$(bindir)/darcs-hooks
	$(INSTALL) -m644 config.py $(DESTDIR)$(sysconfdir)
	for i in *; do \
		[ ! -d $$i ] && continue; \
		[ ! -e $$i/config.py ] && continue; \
		$(INSTALL) -d $(DESTDIR)$(sysconfdir)/$$i; \
		$(INSTALL) -m644 $$i/config.py $(DESTDIR)$(sysconfdir)/$$i; \
		$(INSTALL) -d $(DESTDIR)$(shareddir)/$$i; \
		$(INSTALL) -m644 $$i/$$i.py $(DESTDIR)$(shareddir)/$$i/; \
	done

clean:

dist:
	darcs changes >_darcs/pristine/Changelog
	darcs dist -d darcs-hooks-$(VERSION)
	gpg --comment "See http://ftp.frugalware.org/pub/README.GPG for info" \
		-ba -u 20F55619 darcs-hooks-$(VERSION).tar.gz
	mv darcs-hooks-$(VERSION).tar.gz{,.asc} ../
	rm _darcs/pristine/Changelog

release:
	darcs tag --checkpoint $(VERSION)
	$(MAKE) dist
