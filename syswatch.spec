Name: syswatch
Version: 7.4.0
Release: 1%{dist}
Summary: Network and system monitor module
License: GPL
Group: System Environment/Daemons
Source: %{name}-%{version}.tar.gz
Vendor: ClearFoundation
Packager: ClearFoundation
Requires: perl
Requires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
BuildArch: noarch
BuildRoot: %_tmppath/%name-%version-buildroot

%description
Network and system monitor module

%prep
%setup
%build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


mkdir -p -m 755 $RPM_BUILD_ROOT%{_unitdir}
mkdir -p -m 755 $RPM_BUILD_ROOT%{_tmpfilesdir}
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p -m 755 $RPM_BUILD_ROOT/usr/sbin
mkdir -p -m 755 $RPM_BUILD_ROOT/var/lib/syswatch
mkdir -p -m 755 $RPM_BUILD_ROOT/var/run/syswatch

install -m 644 syswatch.conf $RPM_BUILD_ROOT/etc/syswatch
install -m 644 syswatch.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/syswatch
install -m 755 syswatch $RPM_BUILD_ROOT/usr/sbin/
install -m 644 syswatch.service %{buildroot}%{_unitdir}/syswatch.service
install -m 644 syswatch-tmpfiles.conf %{buildroot}/%{_tmpfilesdir}/syswatch.conf

%post
%systemd_post syswatch.service

systemctl enable syswatch.service >/dev/null 2>&1

exit 0

%preun
%systemd_preun syswatch.service

exit 0

%postun
%systemd_postun_with_restart syswatch.service

exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) /etc/syswatch
%{_unitdir}/syswatch.service
%{_tmpfilesdir}/syswatch.conf
/etc/logrotate.d/syswatch
/usr/sbin/syswatch
/var/lib/syswatch
/var/run/syswatch
