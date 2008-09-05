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
Release:	%{mkrel 1}
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libsigc++-devel
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
Provides:	%{name}-devel = %{version}-%{release}
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

%clean
rm -fr %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
 
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libvdk*.so.%{major}*   

%files -n %{develname}
%defattr(-,root,root)
%doc README TODO example doc/*.txt     
%{_libdir}/libvdk*.so
%{_libdir}/libvdk*.la
%{_includedir}/vdk2
%{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/vdk-2.x.pc
