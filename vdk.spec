%define name vdk
%define version 2.0.3
%define release %mkrel 2

%define major   2
%define libname %mklibname %name %major
%define libnamedev %mklibname %name %major -d

Summary:	C++ framework that wraps famous Gtk+ widget set library
Name:		%name
Version:	%version
Release:	%release

Source0:	%name-%version.tar.bz2
Url:		http://vdkbuilder.sourceforge.net/

License:	LGPL
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires:	gnome-libs-devel libsigc++-devel tetex gtk2-devel

%description
- signal/events dispatching strategy makes a clear distinction between 
interface   and application
- a powerful and flexible signal system 
- supports properties like moderns RAD tools do, user defined properties are
  supported as well 
- will track closely Gtk+ development and relies only on Gtk+ stable releases
- has a full documentation and soon a tutorial will be written 
- is used as base library for a RAD tool , named VDKBuilder 
- using VDK is similar to Borland (Inprise) OWL and/or VCL 

VDK distribution 

VDK is made of three separated libraries: 
- libvdk VDK core library, contains all Gtk+ wrapped widgets. 
- libvdkcompo VDK components library, contains totally new widgets and others
  interesting widgets
- libvdkgnome a gnome-aware components library (optionally build) 

%package -n %libname
Summary:        C++ framework that wraps famous Gtk+ widget set library
Group:		System/Libraries

%description -n %libname
- signal/events dispatching strategy makes a clear distinction between 
interface and application
- a powerful and flexible signal system
- supports properties like moderns RAD tools do, user defined properties are
  supported as well
- will track closely Gtk+ development and relies only on Gtk+ stable releases
- has a full documentation and soon a tutorial will be written
- is used as base library for a RAD tool , named VDKBuilder
- using VDK is similar to Borland (Inprise) OWL and/or VCL

VDK distribution

VDK is made of three separated libraries:
- libvdk VDK core library, contains all Gtk+ wrapped widgets.
- libvdkcompo VDK components library, contains totally new widgets and others
  interesting widgets
- libvdkgnome a gnome-aware components library (optionally build)

%package -n %libnamedev 
Summary:	C++ wrapper for GTK+
Group:		Development/GNOME and GTK+
Requires:	%libname = %version-%release
Provides:	libvdk-devel


%description -n %libnamedev
This package contains the headers and libraries needed to compile and link
applications using VDK.
                               

%prep

%setup -q

%build
./configure --prefix=%_prefix \
			--host=%_target_platform \
			--build=%_target_platform \
			--enable-debug=no \
			--enable-shared=yes \
			--enable-static=no \
			--enable-opt=3 \
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

rm -rf $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}

%clean
rm -fr %buildroot

%post -n %libname -p /sbin/ldconfig
 
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%doc README TODO
%_libdir/libvdk*.so.*   


%files -n %libnamedev
%defattr(-,root,root)
%doc example doc/*.txt     
%_libdir/libvdk*.so
%_libdir/libvdk*.la
%_includedir/vdk2
%_mandir/man1/*
%_bindir/*
%_datadir/aclocal/*


