Name:           cloudrouter-release
Version:        1
Release:        3
Summary:        Extra packages for the CloudRouter Software-Defined Interconnect (SDI) platform

Group:          System Environment/Base
License:        AGPLv3

URL:            https://cloudrouter.org/
Source0:        https://cloudrouter.org/repo/RPM-GPG-KEY-CLOUDROUTER
Source1:        cloudrouter.repo
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%description
This packages the CloudRouter repository GPG key as well as configuration for yum.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CLOUDROUTER

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*

%changelog
* Tue Mar 31 2015 David Jorm - 1-3
- Update repo URL
* Mon Mar 02 2015 David Jorm - 1-2
- Remove update of issue file, this is now handled by the CloudRouter image build script
* Tue Jan 20 2015 David Jorm - 1-1
- Update issue file
* Fri Jan 16 2015 David Jorm - 1-0
- Initial package
