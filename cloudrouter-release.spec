%define release_name CloudRouter
%define dist_version 1

Summary:	CloudRouter release files
Name:		cloudrouter-release
Version:	1
Release:	6
License:	AGPLv3
Group:		System Environment/Base
Source:		%{name}-%{version}.tar.gz
Obsoletes:	redhat-release
Provides:	redhat-release
Provides:	system-release
Provides:	system-release(release)
BuildArch:	noarch
Conflicts:	fedora-release

%description
CloudRouter release files such as yum configs and various /etc/ files that
define the release. 

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes

%description notes
CloudRouter release notes package. 


%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "CloudRouter release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/cloudrouter-release
echo "cpe:/o:cloudrouter:cloudrouter:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/cloudrouter-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s cloudrouter-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s cloudrouter-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=CloudRouter
VERSION="%{version} (%{release_name})"
ID=cloudrouter
VERSION_ID=%{version}
PRETTY_NAME="CloudRouter %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:cloudrouter:cloudrouter:%{version}"
HOME_URL="http://cloudrouter.org/"
BUG_REPORT_URL="http://cloudtouer.org/"
EOF

# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg

install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
# says "fedora-19-primary: i386 x86_64",
# RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
 key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
 arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
 || echo "WARNING: no archmap entry for $key"
 for arch in $arches; do
 # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
 ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
 done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-cloudrouter-%{dist_version}-primary RPM-GPG-KEY-%{dist_version}-cloudrouter
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in cloudrouter*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%cloudrouter		%{dist_version}
%%dist		.cr%{dist_version}
%%cr%{dist_version}		1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL GNU-AGPL-3.0.txt
%config %attr(0644,root,root) /etc/os-release
%config %attr(0644,root,root) /etc/cloudrouter-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/cloudrouter.repo
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing.repo
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files notes
%defattr(-,root,root,-)
%doc README.CloudRouter-Release-Notes

%changelog
* Mon Apr 13 2015 David Jorm <djorm@iix.net> - 1-6
- increment release to facilitate rebuild

* Sat Apr 04 2015 Paul Gampe <pgampe@iix.net> - 1-5
- include fedora repos

* Sat Apr 04 2015 Paul Gampe <pgampe@iix.net> - 1-4
- follow generic-release format

* Tue Mar 31 2015 David Jorm - 1-3
- Update repo URL

* Mon Mar 02 2015 David Jorm - 1-2
- Remove update of issue file, this is now handled by the CloudRouter image build script

* Tue Jan 20 2015 David Jorm - 1-1
- Update issue file

* Fri Jan 16 2015 David Jorm - 1-0
- Initial package
