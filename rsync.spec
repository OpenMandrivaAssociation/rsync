Summary:	A program for synchronizing files over a network
Name:		rsync
Version: 	3.1.0
Release:	2
License:	GPLv3+
Group:		Networking/File transfer
URL:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz
Source1:	http://rsync.samba.org/ftp/rsync/rsync.html
Source2:	http://rsync.samba.org/ftp/rsync/rsyncd.conf.html
Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz.asc
Source5:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{version}.tar.gz
Source6:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{version}.tar.gz.asc
Source12:	rsyncd.socket
Source13:	rsyncd.service
Source14:	rsyncd.conf
Source15:	rsyncd.sysconfig
Patch0:		rrsync-bug-3.0.0.patch
BuildRequires:	popt-devel
BuildRequires:	acl-devel
Buildrequires:	zlib-devel

%bcond_without	patches

%description
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files). Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.  A technical report which describes the rsync algorithm
is included in this package.

Install rsync if you need a powerful mirroring program.
%if %{with patches}
This rpm has these patches applied from rsync tree:
  - acl: allow to mirror acl

Rebuild the source rpm with `bcond_with patches'
if you don't  want these patches
%endif

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .rrsync
%if %{with patches}
%setup -q -D -b 5 -n %{name}-%{version}
%__patch -p1 -b -z .dir-del < patches/backup-dir-dels.diff
%__patch -p1 -b -z .acl < patches/acls.diff
%endif

%build
%__autoconf
%__autoheader
%serverbuild
rm -f config.h

%configure2_5x \
    --enable-acl-support \
    --with-nobody-group=nogroup \
    --without-included-zlib

%make proto
%make

%check
make test

%install
%makeinstall_std

install -m644 %{SOURCE1} %{SOURCE2} .

install -D -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/rsyncd.socket
install -D -m644 %{SOURCE13} $RPM_BUILD_ROOT/%{_unitdir}/rsyncd.service
install -D -m644 %{SOURCE14} $RPM_BUILD_ROOT/%{_sysconfdir}/rsyncd.conf
install -D -m644 %{SOURCE15} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/rsyncd

%files
%doc tech_report.tex README *html NEWS OLDNEWS
%doc support/rrsync
%{_bindir}/rsync
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*
%config(noreplace) %{_sysconfdir}/rsyncd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_unitdir}/rsyncd.socket
%{_unitdir}/rsyncd.service
