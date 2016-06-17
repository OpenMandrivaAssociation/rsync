%bcond_without	patches

Summary:	A program for synchronizing files over a network
Name:		rsync
%define	overs	3.1.2
Version: 	3.1.2
#% define	prerel	pre1
Release:	0.1
License:	GPLv3+
Group:		Networking/File transfer
Url:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}%{?prerel}.tar.gz
Source1:	http://rsync.samba.org/ftp/rsync/rsync.html
Source2:	http://rsync.samba.org/ftp/rsync/rsyncd.conf.html
Source3:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{overs}.tar.gz
Source12:	rsyncd.socket
Source13:	rsyncd.service
Source14:	rsyncd.conf
Source15:	rsyncd.sysconfig
Source16:	rsyncd@.service
Source100:	rsync.rpmlintrc
Patch0:		rsync-man.patch
Patch1:		detect-renamed-rediff.patch

BuildRequires:	acl-devel
BuildRequires:	acl
Buildrequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(popt)
BuildRequires:	yodl

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
%apply_patches

%if %{with patches}
%{patch -p1 -P patches/backup-dir-dels.diff -b .dir_dels~ -F2}
%{patch -p1 -P patches/acls.diff -b .acls~}
%{patch -p1 -P patches/xattrs.diff -b .xattrs~}

# enable --copy-devices parameter
%{patch -p1 -P patches/copy-devices.diff -b .copy_devs~}
# enable --atimes parameter
%{patch -p1 -P patches/atimes.diff -b .atimes~}
# enable --direct-io parameter
%{patch -p1 -P patches/direct-io.diff -b .directio~}
# enable --detect-renamed parameter
%{patch -p1 -P patches/detect-renamed.diff -b .detect_renamed~ -F2}
# enable --date-only parameter
%{patch -p1 -P patches/date-only.diff -b .date_only~}
# enable --sumfiles parameter
#{patch -p1 -P patches/checksum-reading.diff -b .chksum_read~}
#{patch -p1 -P patches/checksum-updating.diff -b .chksum_update~}
# enable --downdate parameter
%{patch -p1 -P patches/downdate.diff -b .downdate~ -F2}
# enable --fileflags parameter
#{patch -p1 -P patches/fileflags.diff -b .fileflags~ -F2}
# enable --fsync parameter
#{patch -p1 -P patches/fsync.diff -b .fsync~ -F2}
# disabled due to breakage of test suite..
# enable --ignore-case
#{patch -p1 -P patches/ignore-case.diff -b .ignore_case~}
# enable --link-by-hash
#{patch -p1 -P patches/link-by-hash.diff -b .link_by_hash~ -F2}
#{patch -p1 -P patches/netgroup-auth.diff -b .netgroup~}
# enable --omit-dir-changes
#{patch -p1 -P patches/omit-dir-changes.diff -b .omit_dir_chgs~ -F2}
# enable  --slow-down
%{patch -p1 -P patches/slow-down.diff -b .slowdown~}

#patch4 -p1 -b .fix_defs~
%endif

autoreconf -fi
touch configure.sh

%build
%serverbuild
rm -f config.h

%configure2_5x \
	--enable-acl-support \
	--with-nobody-group=nogroup \
	--without-included-popt \
	--without-included-zlib


%make proto
%make

%check
make test

%install
%makeinstall_std

install -m644 %{SOURCE1} %{SOURCE2} .

install -m644 %{SOURCE12} -D %{buildroot}%{_unitdir}/rsyncd.socket
install -m644 %{SOURCE13} -D %{buildroot}%{_unitdir}/rsyncd.service
install -m644 %{SOURCE14} -D %{buildroot}%{_sysconfdir}/rsyncd.conf
install -m644 %{SOURCE15} -D %{buildroot}%{_sysconfdir}/sysconfig/rsyncd
install -m644 %{SOURCE16} -D %{buildroot}%{_unitdir}/rsyncd@.service

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
%{_unitdir}/rsyncd@.service
