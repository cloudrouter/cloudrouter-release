VERSION=$(shell awk '/Version/ { print $$2 }' cloudrouter-release.spec)

CVSROOT = $(shell cat CVS/Root 2>/dev/null || :)

CVSTAG = V$(subst .,-,$(VERSION))

all:

BASE_VERSION = 20

all: hardcode-version

tag-archive:
	@cvs -Q tag -F $(CVSTAG)

create-archive:
	@rm -rf /tmp/fedora-release
	@cd /tmp ; cvs -Q -d $(CVSROOT) export -r$(CVSTAG) cloudrouter-release || echo "Um... export aborted."
	@mv /tmp/cloudrouter-release /tmp/cloudrouter-release-$(VERSION)
	@cd /tmp ; tar -czSpf cloudrouter-release-$(VERSION).tar.gz cloudrouter-release-$(VERSION)
	@rm -rf /tmp/cloudrouter-release-$(VERSION)
	@cp /tmp/cloudrouter-release-$(VERSION).tar.gz .
	@rm -f /tmp/cloudrouter-release-$(VERSION).tar.gz
	@echo ""
	@echo "The final archive is in cloudrouter-release-$(VERSION).tar.gz"

archive: tag-archive create-archive

hardcode-version:
	perl -pi -e 's/$$releasever/$(BASE_VERSION)/' fedora*repo
