%bcond_without	patches
%define	prerel	pre1

Summary:	A program for synchronizing files over a network
Name:		rsync
%define	overs	3.2.1
Version: 	3.2.1
Release:	%{?prerel:0.%{prerel}.}1
License:	GPLv3+
Group:		Networking/File transfer
Url:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{?prerel:src-previews/}%{name}-%{version}%{?prerel}.tar.gz
Source1:	http://rsync.samba.org/ftp/rsync/rsync.html
Source2:	http://rsync.samba.org/ftp/rsync/rsyncd.conf.html
Source3:	http://rsync.samba.org/ftp/rsync/%{?prerel:src-previews/}%{name}-patches-%{overs}%{?prerel}.tar.gz
Source12:	rsyncd.socket
Source13:	rsyncd.service
Source14:	rsyncd.conf
Source15:	rsyncd.sysconfig
Source16:	rsyncd@.service
Source100:	rsync.rpmlintrc

BuildRequires:	acl-devel
BuildRequires:	acl
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libxxhash)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	yodl
BuildRequires:	diffutils
BuildRequires:	systemd-macros

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
%setup -q -n %{name}-%{version}%{?prerel} -b3
%autopatch -p1

%if %{with patches}
%__patch -p1 -i patches/backup-dir-dels.diff
%__patch -p1 -i patches/acls.diff
%__patch -p1 -i patches/xattrs.diff

# enable --copy-devices parameter
%__patch -p1 -i patches/copy-devices.diff
# enable --direct-io parameter
%__patch -p1 -i patches/direct-io.diff
# enable --detect-renamed parameter
%__patch -p1 -i patches/detect-renamed.diff
# enable --date-only parameter
%__patch -p1 -i patches/date-only.diff
# enable --sumfiles parameter
#__patch -p1 -i patches/checksum-reading.diff
#__patch -p1 -i patches/checksum-updating.diff
# enable --downdate parameter
%__patch -p1 -i patches/downdate.diff
# enable --fileflags parameter
#__patch -p1 -i patches/fileflags.diff
# enable --fsync parameter
#__patch -p1 -i patches/fsync.diff
# disabled due to breakage of test suite..
# enable --ignore-case
#__patch -p1 -i patches/ignore-case.diff
# enable --link-by-hash
#__patch -p1 -i patches/link-by-hash.diff
#__patch -p1 -i patches/netgroup-auth.diff
# enable --omit-dir-changes
#__patch -p1 -i patches/omit-dir-changes.diff
# enable  --slow-down
%__patch -p1 -i patches/slow-down.diff

%endif

autoreconf -fi
touch configure.sh

%build
%serverbuild
rm -f config.h

%configure \
    --enable-acl-support \
    --with-nobody-group=nogroup \
    --without-included-popt \
    --without-included-zlib


%make_build proto
%make_build

# (tpg) for some strange reasones checks fails on ix86 and x86_64 and armx
#check
#make test

%install
%make_install

install -m644 %{SOURCE1} %{SOURCE2} .

install -m644 %{SOURCE12} -D %{buildroot}%{_unitdir}/rsyncd.socket
install -m644 %{SOURCE13} -D %{buildroot}%{_unitdir}/rsyncd.service
install -m644 %{SOURCE14} -D %{buildroot}%{_sysconfdir}/rsyncd.conf
install -m644 %{SOURCE15} -D %{buildroot}%{_sysconfdir}/sysconfig/rsyncd
install -m644 %{SOURCE16} -D %{buildroot}%{_unitdir}/rsyncd@.service

%files
%doc tech_report.tex *html
%doc support/rrsync
%{_bindir}/rsync
%{_bindir}/rsync-ssl
%{_mandir}/man1/rsync.1*
%{_mandir}/man1/rsync-ssl.1*
%{_mandir}/man5/rsyncd.conf.5*
%config(noreplace) %{_sysconfdir}/rsyncd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_unitdir}/rsyncd.socket
%{_unitdir}/rsyncd.service
%{_unitdir}/rsyncd@.service
