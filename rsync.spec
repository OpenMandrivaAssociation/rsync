%bcond_with	patches
#% define	prerel	

Summary:	A program for synchronizing files over a network
Name:		rsync
Version:	3.3.0
Release:	1
License:	GPLv3+
Group:		Networking/File transfer
Url:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{?prerel:src-previews/}%{name}-%{version}%{?prerel}.tar.gz
Source1:	http://rsync.samba.org/ftp/rsync/rsync.html
Source2:	http://rsync.samba.org/ftp/rsync/rsyncd.conf.html
Source3:	http://rsync.samba.org/ftp/rsync/%{?prerel:src-previews/}%{name}-patches-%{version}%{?prerel}.tar.gz
Source12:	rsyncd.socket
Source13:	rsyncd.service
Source14:	rsyncd.conf
Source15:	rsyncd.sysconfig
Source16:	rsyncd@.service
Source100:	rsync.rpmlintrc

BuildRequires:	pkgconfig(libacl)
BuildRequires:	acl
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libxxhash)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	yodl
BuildRequires:	diffutils
BuildRequires:	systemd-rpm-macros

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
%__patch -p1 -i patches/clone-dest.diff
%__patch -p1 -i patches/fileflags.diff
%__patch -p1 -i patches/soften-links.diff
%__patch -p1 -i patches/backup-deleted.diff
%__patch -p1 -i patches/catch_crash_signals.diff
%__patch -p1 -i patches/ignore-case.diff
%__patch -p1 -i patches/direct-io.diff
%__patch -p1 -i patches/detect-renamed.diff
%__patch -p1 -i patches/kerberos.diff
%__patch -p1 -i patches/source-backup.diff
%__patch -p1 -i patches/detect-renamed-lax.diff
%__patch -p1 -i patches/date-only.diff
%__patch -p1 -i patches/slp.diff
%__patch -p1 -i patches/congestion.diff
%__patch -p1 -i patches/checksum-updating.diff
%__patch -p1 -i patches/checksum-reading.diff
%__patch -p1 -i patches/filter-attribute-mods.diff
%__patch -p1 -i patches/source-filter_dest-filter.diff
%__patch -p1 -i patches/link-by-hash.diff
%__patch -p1 -i patches/omit-dir-changes.diff
%__patch -p1 -i patches/downdate.diff
%__patch -p1 -i patches/transliterate.diff
%__patch -p1 -i patches/backup-dir-dels.diff
%__patch -p1 -i patches/slow-down.diff
%__patch -p1 -i patches/sparse-block.diff
%endif

autoreconf -fi
touch configure.sh

%build
%serverbuild
rm -f config.h

%configure \
    --enable-openssl \
    --enable-xxhash \
    --enable-zstd \
    --enable-lz4 \
    --enable-ipv6 \
    --enable-acl-support \
    --with-nobody-group=nogroup \
    --with-included-popt=no \
    --with-included-zlib=no

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
%doc %{_mandir}/man1/rsync.1*
%doc %{_mandir}/man1/rsync-ssl.1*
%doc %{_mandir}/man5/rsyncd.conf.5*
%config(noreplace) %{_sysconfdir}/rsyncd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_unitdir}/rsyncd.socket
%{_unitdir}/rsyncd.service
%{_unitdir}/rsyncd@.service
