Summary:	A program for synchronizing files over a network
Name:		rsync
Version: 	2.6.9
Release:	%mkrel 2
Group:		Networking/File transfer
URL:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz
Source1:	rsync.html
Source2:	rsyncd.conf.html
Source3:	rsync.xinetd
Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz.asc
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
  - backup-dir-dels: availlibility to store backup file in another directory

Rebuild the source rpm with `--without patches' if you don't  want these patches
%endif

%prep

%setup -q -n %{name}-%{version}
%if %apply_patches
#%%__patch -p1 -b -z .dir-del < patches/backup-dir-dels.diff
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
%doc tech_report.tex README *html
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%{_bindir}/rsync
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*


