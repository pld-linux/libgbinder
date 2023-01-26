Summary:	Android binder client library
Summary(pl.UTF-8):	Biblioteka kliencka Android binder
Name:		libgbinder
Version:	1.1.30
Release:	0.1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/mer-hybris/libgbinder/tags
Source0:	https://github.com/mer-hybris/libgbinder/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ab55fd8341f8e36367299fc39810df4c
Patch0:		install.patch
URL:		https://github.com/mer-hybris/libgbinder
BuildRequires:	libglibutil-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C interfaces for Android binder.

%description -l pl.UTF-8
Biblioteka kliencka Android binder.

%package devel
Summary:	Header files for gbinder library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gbinder
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for gbinder library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gbinder.

%package tools
Summary:	Android binder tools
Summary(pl.UTF-8):	Narzędzia Android binder
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description tools
Android binder command line utilities.

%description tools -l pl.UTF-8
Narzędzia Android binder działające z linii poleceń.

%prep
%setup -q
%patch0 -p1

%build
%{__make} LIBDIR=%{_libdir} KEEP_SYMBOLS=1 release pkgconfig

for util in test/binder-bridge test/binder-list test/binder-ping test/binder-call; do
	%{__make} -C ${util} KEEP_SYMBOLS=1 release
done

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-dev \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

for util in test/binder-bridge test/binder-list test/binder-ping test/binder-call; do
	%{__make} -C ${util} DESTDIR=$RPM_BUILD_ROOT install
done


%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libgbinder.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgbinder.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbinder.so
%{_includedir}/gbinder
%{_pkgconfigdir}/libgbinder.pc

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/binder-bridge
%attr(755,root,root) %{_bindir}/binder-list
%attr(755,root,root) %{_bindir}/binder-ping
%attr(755,root,root) %{_bindir}/binder-call
