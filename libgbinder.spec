Summary:	Android binder client library
Summary(pl.UTF-8):	Biblioteka kliencka Android binder
Name:		libgbinder
Version:	1.1.32
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/mer-hybris/libgbinder/tags
Source0:	https://github.com/mer-hybris/libgbinder/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	65557e5ce0339aedf2c22a7c0ac1b58d
Patch0:		install.patch
URL:		https://github.com/mer-hybris/libgbinder
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libglibutil-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C interfaces for Android binder.

Binder is Android-specific RPC mechanism, available in binder_linux
module.

%description -l pl.UTF-8
Biblioteka kliencka Android binder.

Binder to specyficzny dla Androida mechanizm IPC, dostępny w module
binder_linux.

%package devel
Summary:	Header files for gbinder library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gbinder
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	libglibutil-devel

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
%patch -P0 -p1

%build
%{__make} release pkgconfig \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	KEEP_SYMBOLS=1

for util in test/binder-bridge test/binder-list test/binder-ping test/binder-call; do
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	%{__make} -C ${util} release \
		CC="%{__cc}" \
		KEEP_SYMBOLS=1
done

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-dev \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

for util in test/binder-bridge test/binder-list test/binder-ping test/binder-call; do
	%{__make} -C ${util} install \
		DESTDIR=$RPM_BUILD_ROOT
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README debian/changelog
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
