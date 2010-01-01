%define version 3.0.7
# %%define pre pre10
%define rel 1
%define release %mkrel %{?pre:0.%{pre}.%{rel}}%{?!pre:%{rel}}

Summary:	A program for synchronizing files over a network
Name:		rsync
Version: 	%version
Release:	%release
Group:		Networking/File transfer
URL:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}%{?pre}.tar.gz
Source1:	rsync.html
Source2:	rsyncd.conf.html
Source3:	rsync.xinetd
Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}%{?pre}.tar.gz.asc
Source5:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{version}%{?pre}.tar.gz
Source6:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{version}%{?pre}.tar.gz.asc
Patch0:     rrsync-bug-3.0.0.patch
License:	GPL
BuildRequires:	popt-devel
BuildRequires:  libacl-devel
BuildRequires:  acl
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define apply_patches 1

%{?_with_patches:%define apply_patches 1}
%{?_without_patches:%define apply_patches 0}

%description
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files). Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.  A technical report which describes the rsync algorithm
is included in this package.

Install rsync if you need a powerful mirroring program.
%if %apply_patches
This rpm has these patches applied from rsync tree:
  - acl: allow to mirror acl

Rebuild the source rpm with `--without patches' if you don't  want these patches
%endif

%prep
%setup -q -n %{name}-%{version}%{?pre}
%patch0 -p0 -b .rrsync
%if %apply_patches
%setup -q -D -b 5 -n %{name}-%{version}%{?pre}
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
    --with-acl-support \
    --with-nobody-group=nogroup

# kernel or glibc sucks
perl -pi -e 's:^#define HAVE_LUTIMES 1$:/* #undef HAVE_LUTIMES */:' config.h

%make proto
%make

%check
# Test failed on the cluster because there are 2 svn group
[ `hostname | grep mandriva.com` ] && exit 0
make test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}{%{_bindir},%{_mandir}/{man1,man5}}

%makeinstall

install -m644 %{SOURCE1} %{SOURCE2} .
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/xinetd.d/rsync

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc tech_report.tex README *html NEWS OLDNEWS
%doc support/rrsync
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%{_bindir}/rsync
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*
