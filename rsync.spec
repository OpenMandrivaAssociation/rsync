%bcond_without	uclibc

Summary:	A program for synchronizing files over a network
Name:		rsync
%define	overs	3.1.1
Version: 	3.1.1
#% define	prerel	pre1
Release:	%{?prerel:0.%{prerel}.}1
License:	GPLv3+
Group:		Networking/File transfer
Url:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}%{?prerel}.tar.gz
Source1:	http://rsync.samba.org/ftp/rsync/rsync.html
Source2:	http://rsync.samba.org/ftp/rsync/rsyncd.conf.html
#Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz.asc
Source5:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{overs}.tar.gz
Source6:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{overs}.tar.gz.asc
Source12:	rsyncd.socket
Source13:	rsyncd.service
Source14:	rsyncd.conf
Source15:	rsyncd.sysconfig
Source16:	rsyncd@.service

Patch1:		rsync-man.patch
Patch2:		rsync-3.1.0-fwhole-program.patch

BuildRequires:	acl-devel
BuildRequires:	acl
Buildrequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(popt)
BuildRequires:	yodl

%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

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

%package -n	uclibc-%{name}
Summary:	A program for synchronizing files over a network (uClibc build)
Group:		Networking/File transfer
Requires:	%{name} = %{EVRD}

%description -n	uclibc-%{name}
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files). Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.  A technical report which describes the rsync algorithm
is included in this package.

Install rsync if you need a powerful mirroring program.

%prep 
%setup -q -n %{name}-%{version}%{?prerel} -b5
%patch1 -p1 -b .man~
%patch2 -p1 -b .whole_program~
%if %{with patches}
%{patch -F2 -p1 -P patches/backup-dir-dels.diff -b .dir_dels~}
%{patch -p1 -P patches/acls.diff -b .acls~}

#Enable --copy-devices parameter
%{patch -p1 -P patches/copy-devices.diff -b .copy_devs~}

%endif

autoreconf -fi

%build
%serverbuild

export CONFIGURE_TOP="$PWD"
export CC=gcc

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
cp -f ../configure.sh .
%uclibc_configure	--enable-acl-support \
			--with-nobody-group=nogroup \
			--without-included-zlib \
			--enable-wholeprogram
%make proto
%make

popd
%endif

mkdir -p glibc
pushd glibc
cp -f ../configure.sh .
%configure2_5x	--enable-acl-support \
		--with-nobody-group=nogroup \
		--without-included-zlib \
		--enable-wholeprogram

%make proto
%make
popd

%check
%make -C glibc test

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
%endif
%makeinstall_std -C glibc

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

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_bindir}/rsync
%endif
