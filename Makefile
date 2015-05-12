# Copyright 2015 CloudRouter Project Authors.

PKG_NAME		:= cloudrouter-release
RPM_NAME_FEDORA := $(PKG_NAME)-fedora
RPM_NAME_CENTOS := $(PKG_NAME)-centos
VERSION     	:= 1
SRC_FILE_FEDORA := $(RPM_NAME_FEDORA)-$(VERSION).tar.gz
SRC_FILE_CENTOS := $(RPM_NAME_CENTOS)-$(VERSION).tar.gz

all: rpm

$(SRC_FILE_FEDORA):
	rm -rf $(RPM_NAME_FEDORA)-$(VERSION)
	mkdir -p $(RPM_NAME_FEDORA)-$(VERSION)
	find $(PKG_NAME) -maxdepth 1 -type f -exec cp {} $(RPM_NAME_FEDORA)-$(VERSION)/. \;
	find $(PKG_NAME)/fedora -maxdepth 1 -type f -exec cp {} $(RPM_NAME_FEDORA)-$(VERSION)/. \;
	tar cvf $(SRC_FILE_FEDORA) $(RPM_NAME_FEDORA)-$(VERSION)
	mkdir -p rpm-build
	cp $(SRC_FILE_FEDORA) rpm-build

$(SRC_FILE_CENTOS):
	rm -rf $(RPM_NAME_CENTOS)
	mkdir -p $(RPM_NAME_CENTOS)-$(VERSION)
	find $(PKG_NAME) -maxdepth 1 -type f -exec cp {} $(RPM_NAME_CENTOS)-$(VERSION)/. \;
	find $(PKG_NAME)/centos -maxdepth 1 -type f -exec cp {} $(RPM_NAME_CENTOS)-$(VERSION)/. \;
	tar cvf $(SRC_FILE_CENTOS) $(RPM_NAME_CENTOS)-$(VERSION)
	mkdir -p rpm-build
	cp $(SRC_FILE_CENTOS) rpm-build

# Phony targets for cleanup and similar uses
#
 .PHONY: clean

source: $(SRC_FILE_FEDORA) $(SRC_FILE_CENTOS)

fedora: source
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	    --define "_builddir %{_topdir}" \
	    --define "_rpmdir %{_topdir}" \
	    --define "_srcrpmdir %{_topdir}" \
	    --define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
	    --define "_specdir %{_topdir}" \
	    --define "_sourcedir  %{_topdir}" \
	    --define "distribution  Fedora" \
	    -ba cloudrouter-release.spec

centos: source
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	    --define "_builddir %{_topdir}" \
	    --define "_rpmdir %{_topdir}" \
	    --define "_srcrpmdir %{_topdir}" \
	    --define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
	    --define "_specdir %{_topdir}" \
	    --define "_sourcedir  %{_topdir}" \
	    --define "distribution  CentOS" \
	    -ba cloudrouter-release.spec

rpm: fedora centos

clean:
	rm -f $(SRC_FILE_FEDORA) $(SRC_FILE_CENTOS)
	rm -rf $(RPM_NAME_FEDORA)-$(VERSION) $(RPM_NAME_CENTOS)-$(VERSION)
	rm -rf rpm-build
