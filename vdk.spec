# underlink.patch fixes most underlinking issues but there's one weird
# one I just can't shift - AdamW 2008/09
%define _disable_ld_no_undefined	1

%define oname		vdklib

%define major		2
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	C++ framework that binds GTK+ GUI libraries
Name:		vdk
Version:	2.4.1
Release:	7
Source0:	http://downloads.sourceforge.net/%{oname}/%{name}-%{version}.tar.gz
# From Debian: fix 'extra qualification' build errors - AdamW 2008/09
Patch0:		vdk-2.4.1-debian-qualification.patch
# From Debian: fix build failures caused by missing includes - AdamW
# 2008/09
Patch1:		vdk-2.4.1-debian-cstring.patch
# Fix underlinking issues - AdamW 2008/09
Patch2:		vdk-2.4.1-underlink.patch
# From Debian: fix x86_64 build issues - AdamW 2008/09
Patch3:		vdk-2.4.1-debian-x86_64.patch
URL:		http://vdklib.sourceforge.net/
License:	LGPLv2+
Group:		System/Libraries
BuildRequires:	sigc++2.0-devel
BuildRequires:	tetex
BuildRequires:	gtk2-devel
BuildRequires:	libdmx-devel

%description
The Visual Development Kit (VDK) is a C++ library that wraps the GTK+
toolkit. The package also includes the VDK Component Library which
contains some useful new components not available in pure GTK+.

Programming in VDK is much like programming in VCL and Borland C++
Builder. 

%package -n %{libname}
Summary:        C++ framework that binds GTK+ GUI libraries
Group:		System/Libraries

%description -n %{libname}
The Visual Development Kit (VDK) is a C++ library that wraps the GTK+
toolkit. The package also includes the VDK Component Library which
contains some useful new components not available in pure GTK+.

Programming in VDK is much like programming in VCL and Borland C++
Builder.

%package -n %{develname} 
Summary:	C++ framework that binds GTK+ GUI libraries
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname vdk 2 -d}

%description -n %{develname}
This package contains the headers and libraries needed to compile and
link applications using VDK.
                               
%prep
%setup -q
%patch0 -p1 -b .qualification
%patch1 -p1 -b .cstring
%patch2 -p1 -b .underlink
%patch3 -p1 -b .x86_64

%build
%configure2_5x \
			--host=%{_target_platform} \
			--build=%{_target_platform} \
			--enable-debug=no \
			--enable-shared=yes \
			--enable-static=no \
			--enable-opt=2 \
			--enable-testvdk=yes \
			--enable-sigc=yes \
			--enable-testsigc=yes \
			--enable-gnome=yes \
			--enable-doc-html=yes \
			--enable-doc-latex=no \
			--enable-doc-man=yes

%make
make docs


%install
%makeinstall
rm -rf %{buildroot}/%{_docdir}/%{name}-devel-%{version}

%files -n %{libname}
%{_libdir}/libvdk*.so.%{major}*   

%files -n %{develname}
%doc README TODO example doc/*.txt     
%{_libdir}/libvdk*.so
%{_includedir}/vdk2
%{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/vdk-2.x.pc


%changelog
* Sun Sep 20 2009 Thierry Vignaud <tvignaud@mandriva.com> 2.4.1-5mdv2010.0
+ Revision: 445656
- rebuild

* Thu Nov 13 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.1-4mdv2009.1
+ Revision: 302649
- fix deps
- rebuilt against new libxcb

* Fri Sep 05 2008 Adam Williamson <awilliamson@mandriva.org> 2.4.1-2mdv2009.0
+ Revision: 280998
- put docs in devel package, not lib package
- protect major in file list
- s/$RPM_BUILD_ROOT/%%{buildroot}
- don't use -O3 optimizations
- use configure macro
- better description (from upstream)
- drop unnecessary old GNOME buildrequire
- new license policy
- add debian-x86_64.patch (from Debian, fix x86_64 build errors)
- add underlink.patch (fix most underlinking errors)
- add debian-cstrng.patch (from Debian, fixes build errors)
- add debian-qualification.patch (from Debian, fixes build errors)
- new version 2.4.1
- better summary
- new devel policy
- disable underlink protection (one error can't be fixed)
- drop unnecessary defines

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - fix no-buildroot-tag
    - BR gtk2-devel
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - import vdk

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers


* Wed Aug 05 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.0.3-1mdk
- 2.0.3

* Sat Mar 23 2002 David BAUDENS <baudens@mandrakesoft.com> 1.2.4-3mdk
- Allow build
- Clean spec

* Fri Dec 08 2000 David BAUDENS <baudens@mandrakesoft.com> 1.2.4-2mdk
- Allow to build: fix typos in SPEC
- Macros, BM, etc.
- Use optimizations

* Mon Oct 23 2000 Vincent Saugey <vince@mandrakesoft.com> 1.2.4-1mdk
- First mdk version
