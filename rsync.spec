# %%define pre pre10

%bcond_without	uclibc

Summary:	A program for synchronizing files over a network
Name:		rsync
Version: 	3.0.9
Release:	3.1
Group:		Networking/File transfer
License:	GPLv3+
URL:		http://rsync.samba.org/
Source0:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz
Source1:	rsync.html
Source2:	rsyncd.conf.html
Source3:	rsync.xinetd
Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz.asc
Source5:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{version}.tar.gz
Source6:	http://rsync.samba.org/ftp/rsync/%{name}-patches-%{version}.tar.gz.asc
Patch0:		rrsync-bug-3.0.0.patch
Patch1:		rsync-aarch64.patch
BuildRequires:	popt-devel
BuildRequires:	acl-devel
BuildRequires:	acl
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

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

Rebuild the source rpm with `--without patches' if you don't  want 
these patches
%endif

%package -n	uclibc-%{name}
Summary:	A program for synchronizing files over a network (uClibc build)
Group:		Networking/File transfer

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
%setup -q
%patch0 -p0 -b .rrsync

%if %apply_patches
%setup -q -D -b 5 -n %{name}-%{version}
%__patch -p1 -b -z .dir-del < patches/backup-dir-dels.diff
%__patch -p1 -b -z .acl < patches/acls.diff
%endif
%patch1 -p1 -b .aarch64

autoreconf -fi

%build
%serverbuild

export CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
    --enable-acl-support \
    --with-acl-support \
    --with-nobody-group=nogroup
# kernel or glibc sucks
perl -pi -e 's:^#define HAVE_LUTIMES 1$:/* #undef HAVE_LUTIMES */:' config.h

%make proto
%make
popd
%endif

mkdir -p glibc
pushd glibc
#ln -s ../rsync.1 ../rsyncd.conf.5
%configure2_5x \
    --enable-acl-support \
    --with-acl-support \
    --with-nobody-group=nogroup

# kernel or glibc sucks
perl -pi -e 's:^#define HAVE_LUTIMES 1$:/* #undef HAVE_LUTIMES */:' config.h

%make proto
%make
popd

%check
# Test failed on the cluster because there are 2 svn group
[ `hostname | grep mandriva.com` ] && exit 0
make -C glibc test

%install
install -d %{buildroot}{%{_bindir},%{_mandir}/{man1,man5}}

%if %{with uclibc}
%makeinstall_std -C uclibc
%endif
%makeinstall_std -C glibc

install -m644 %{SOURCE1} %{SOURCE2} .
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/xinetd.d/rsync
install -m644 rsync.1 %{buildroot}%{_mandir}/man1/rsync.1*
install -m644 rsyncd.conf.5 %{buildroot}%{_mandir}/man5/rsyncd.conf.5*

%files
%doc tech_report.tex README *html NEWS OLDNEWS
%doc support/rrsync
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%{_bindir}/rsync
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_bindir}/rsync
%endif

%changelog
* Sun Oct 16 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.9-1mdv2012.0
+ Revision: 704846
- 3.0.9

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.8-2
+ Revision: 669453
- mass rebuild

* Mon Mar 28 2011 Funda Wang <fwang@mandriva.org> 3.0.8-1
+ Revision: 648660
- update to new version 3.0.8

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.7-2mdv2011.0
+ Revision: 607379
- rebuild

  + Michael Scherer <misc@mandriva.org>
    - fix License

* Fri Jan 01 2010 Funda Wang <fwang@mandriva.org> 3.0.7-1mdv2010.1
+ Revision: 484808
- new version 3.0.7

* Tue May 12 2009 Frederik Himpe <fhimpe@mandriva.org> 3.0.6-1mdv2010.0
+ Revision: 374977
- update to new version 3.0.6

* Sat Jan 03 2009 Olivier Thauvin <nanardon@mandriva.org> 3.0.5-1mdv2009.1
+ Revision: 323612
- 3.0.5

* Mon Dec 01 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.4-2mdv2009.1
+ Revision: 308829
- provide rrsync in %%doc
- Patch0: new options not handle by the rrsync script

* Sun Sep 07 2008 Frederik Himpe <fhimpe@mandriva.org> 3.0.4-1mdv2009.0
+ Revision: 282417
- Update to new version 3.0.4

  + Olivier Thauvin <nanardon@mandriva.org>
    - add NEWS, OLDNEWS as doc files

* Mon Jun 30 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.3-1mdv2009.0
+ Revision: 230334
- 3.0.3

* Sat Apr 12 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.2-1mdv2009.0
+ Revision: 192620
- 3.0.2 (security fix)

* Wed Mar 19 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-4mdv2008.1
+ Revision: 189063
- revert last change, broken patch, and anyway there's nothing to avoid issue w/o breaking rsync, -e is not used on server side anyway

* Wed Mar 19 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-3mdv2008.1
+ Revision: 188985
- avoid -e call on server because some ssh can have restriction on it (ask by blino)

* Mon Mar 10 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-2mdv2008.1
+ Revision: 183191
- fix segfault (#38730)

* Sun Mar 02 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-1mdv2008.1
+ Revision: 177527
- 3.0.0 final

* Wed Feb 20 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre10.1mdv2008.1
+ Revision: 173168
- 3.0.0 pre10
- update html page

* Mon Feb 11 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre9.1mdv2008.1
+ Revision: 165088
- 3.0.0 pre9

* Wed Feb 06 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre8.2mdv2008.1
+ Revision: 163178
- put back dir-del patch
- kill the log_on_failure USERID making xinetd performing a useless ident request

* Sat Jan 12 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre8.1mdv2008.1
+ Revision: 150064
- 3.0.0 pre8

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 17 2007 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre7.1mdv2008.1
+ Revision: 121645
- 3.0.0pre7

* Wed Nov 28 2007 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre6.0.1mdv2008.1
+ Revision: 113711
- 3.0.0 pre6

* Sat Nov 10 2007 Olivier Thauvin <nanardon@mandriva.org> 3.0.0-0.pre5.1mdv2008.1
+ Revision: 107440
- 3.0.0 pre5
- prepare work for pre release

* Sun Aug 26 2007 Olivier Thauvin <nanardon@mandriva.org> 2.6.9-5mdv2008.0
+ Revision: 71493
- fix #32654, eg disable lutimes()

* Sun Aug 19 2007 Olivier Thauvin <nanardon@mandriva.org> 2.6.9-4mdv2008.0
+ Revision: 66537
- CVE-2007-4091

* Wed Aug 15 2007 Olivier Thauvin <nanardon@mandriva.org> 2.6.9-3mdv2008.0
+ Revision: 63600
- fix --acls + --delete (#32411)

* Thu Jun 28 2007 Andreas Hasenack <andreas@mandriva.com> 2.6.9-2mdv2008.0
+ Revision: 45571
- rebuild with new serverbuild macro (-fstack-protector-all)


* Tue Nov 07 2006 Olivier Thauvin <nanardon@mandriva.org> 2.6.9-1mdv2007.0
+ Revision: 77064
- 2.6.9
- kill draksync patch (still need ?)
- disable dir-del patch, conflict with the acl one

* Sun Aug 06 2006 Olivier Thauvin <nanardon@mandriva.org> 2.6.8-3mdv2007.0
+ Revision: 53196
- ensure rsync is build with acl
- don't perform test on the cluster (see comment)
- remove changelog
- add patch to force nobody's group (#21340)
- inital rsync import

* Sun Jun 18 2006 Olivier Thauvin <nanardon@mandriva.org> 2.6.8-2mdv2007.0
- add patch to force nobody's group (#21340)

* Sun Apr 23 2006 Olivier Thauvin <nanardon@mandriva.org> 2.6.8-1mdk
- 2.6.8

* Fri Mar 17 2006 Olivier Thauvin <nanardon@mandriva.org> 2.6.7-2mdk
- path1: fix exclude with relative path (patch from rsync author)

* Sat Mar 11 2006 Olivier Thauvin <nanardon@mandriva.org> 2.6.7-1mdk
- 2.6.7

* Fri Jul 29 2005 Olivier Thauvin <nanardon@mandriva.org> 2.6.6-1mdk
- 2.6.6
- remove patch1, no longer need
- add --with --w/o patches options
- don't apply patches, test failed with acl patches (reported on the ML)

* Fri Jun 10 2005 Frederic Lepied <flepied@mandriva.com> 2.6.5-2mdk
- removed patch2 (not needed)

* Fri Jun 10 2005 Frederic Lepied <flepied@mandriva.com> 2.6.5-1mdk
- rediff patch2
- new release

* Thu Jun 09 2005 Olivier Thauvin <nanardon@mandriva.org> 2.6.4-2mdk
- apply 2 patches provide by rsync
- so fix #13854

* Thu May 05 2005 Olivier Thauvin <nanardon@mandriva.org> 2.6.4-1mdk
- 2.6.4
- make test in %%check

* Wed Nov 17 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.6.3-1mdk
- 2.6.3 final

* Thu Aug 19 2004 Warly <warly@mandrakesoft.com> 2.6.3-0.pre1.1mdk
- new version to fix security issue

* Mon Jun 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.6.2-2mdk
- security fix for CAN-2004-0426 (patch3) (Stew Benedict)
- misc spec file fixes

* Sun May 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.6.2-1mdk
- 2.6.2
- P2 from fedora:
	o Backport fix for crasher when passing multiple directories of the same
	  length (bug #123708)
- spec cosmetics

* Thu Jan 08 2004 Warly <warly@mandrakesoft.com> 2.6.0-1mdk
- new version

* Thu Dec 04 2003 Warly <warly@mandrakesoft.com> 2.5.7-1mdk
- new version (security fix)

