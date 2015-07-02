# Copyright 2015 CloudRouter Project Authors.

PKG_NAME		:= cloudrouter-release
RPM_NAME_FEDORA := $(PKG_NAME)-fedora
RPM_NAME_CENTOS := $(PKG_NAME)-centos
VERSION     	:= 2
SRC_FILE_FEDORA := $(RPM_NAME_FEDORA)-$(VERSION).tar.gz
SRC_FILE_CENTOS := $(RPM_NAME_CENTOS)-$(VERSION).tar.gz

# mksrc RPM_NAME SRC_FILE dist
mksrc = rm -rf $(1)-$(VERSION); \
	mkdir -p $(1)-$(VERSION); \
	find $(PKG_NAME) -maxdepth 1 -type f -exec cp {} $(1)-$(VERSION)/. \;; \
	find $(PKG_NAME)/$(3) -maxdepth 1 -type f -exec cp {} $(1)-$(VERSION)/. \;; \
	cp LICENSE README.md $(1)-$(VERSION)/.; \
	tar cvf $(2) $(1)-$(VERSION)

rpmbuild = rpmbuild --define "_topdir %(pwd)/rpm-build" \
	    --define "_builddir %{_topdir}" \
	    --define "_rpmdir %{_topdir}" \
	    --define "_srcrpmdir %{_topdir}" \
	    --define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
	    --define "_specdir %{_topdir}" \
	    --define "_sourcedir  %{_topdir}" \
	    --define "distribution  $(1)" \
	    -ba cloudrouter-release.spec

all: rpm

$(SRC_FILE_FEDORA):
	$(call mksrc,$(RPM_NAME_FEDORA),$(SRC_FILE_FEDORA),fedora)

$(SRC_FILE_CENTOS):
	$(call mksrc,$(RPM_NAME_CENTOS),$(SRC_FILE_CENTOS),centos)

# Phony targets for cleanup and similar uses
#
 .PHONY: clean

source: $(SRC_FILE_CENTOS) $(SRC_FILE_FEDORA)

fedora: $(SRC_FILE_FEDORA)
	mkdir -p rpm-build
	cp $(SRC_FILE_FEDORA) rpm-build
	$(call rpmbuild,Fedora)

centos: $(SRC_FILE_CENTOS)
	mkdir -p rpm-build
	cp $(SRC_FILE_CENTOS) rpm-build
	$(call rpmbuild,CentOS)

rpm: fedora centos

clean:
	rm -f $(SRC_FILE_FEDORA) $(SRC_FILE_CENTOS)
	rm -rf $(RPM_NAME_FEDORA)-$(VERSION) $(RPM_NAME_CENTOS)-$(VERSION)
	rm -rf rpm-build
