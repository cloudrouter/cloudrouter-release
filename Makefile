# Copyright 2015 CloudRouter Project Authors.

RPM_NAME    = cloudrouter-release
VERSION     = 1
FEDORA_BASE = 20
SRC_FILE    = $(RPM_NAME)-$(VERSION).tar.gz

all: rpm

$(SRC_FILE):
	cp -a $(RPM_NAME) $(RPM_NAME)-$(VERSION)
	tar cvf $(SRC_FILE) $(RPM_NAME)-$(VERSION)
	mkdir -p rpm-build
	cp $(SRC_FILE) rpm-build

# Phony targets for cleanup and similar uses
#
# .PHONY: clean

rpm: $(SRC_FILE)
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	    --define "_builddir %{_topdir}" \
	    --define "_rpmdir %{_topdir}" \
	    --define "_srcrpmdir %{_topdir}" \
	    --define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
	    --define "_specdir %{_topdir}" \
	    --define "_sourcedir  %{_topdir}" \
	    -ba cloudrouter-release.spec

clean:
	rm -f $(SRC_FILE)
	rm -rf $(RPM_NAME)-$(VERSION)
	rm -rf rpm-build
