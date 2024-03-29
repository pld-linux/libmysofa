#
# Conditional build:
%bcond_without	tests		# build tests

Summary:	Library to read AES SOFA files
Summary(pl.UTF-8):	Biblioteka do odczytu plików AES SOFA
Name:		libmysofa
Version:	1.3.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/hoene/libmysofa/releases
Source0:	https://github.com/hoene/libmysofa/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	483878b0ed4dc177a64bdec3c3fe6f1e
URL:		https://github.com/hoene/libmysofa
%{?with_tests:BuildRequires:	CUnit}
BuildRequires:	cmake >= 2.8.12
%{?with_tests:BuildRequires:	pkgconfig}
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a simple set of C functions to read AES SOFA files, if they
contain HRTFs stored according to the AES69-2015 standard
<http://www.aes.org/publications/standards/search.cfm?docID=99>.

%description -l pl.UTF-8
Prosty zbiór funkcji C do odczytu plików AES SOFA, zawierających dane
HRTF zapisane zgodnie ze standardem AES69-2015
<http://www.aes.org/publications/standards/search.cfm?docID=99>.

%package devel
Summary:	Header files for libmysofa library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmysofa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
Header files for libmysofa library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmysofa.

%package static
Summary:	Static libmysofa library
Summary(pl.UTF-8):	Statyczna biblioteka libmysofa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmysofa library.

%description static -l pl.UTF-8
Statyczna biblioteka libmysofa.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{cmake_on_off tests BUILD_TESTS} \
	-DCODE_COVERAGE:BOOL=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{?with_tests:%attr(755,root,root) %{_bindir}/mysofa2json}
%attr(755,root,root) %{_libdir}/libmysofa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmysofa.so.1
%{_datadir}/libmysofa

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmysofa.so
%{_includedir}/mysofa.h
%{_pkgconfigdir}/libmysofa.pc
%{_libdir}/cmake/mysofa

%files static
%defattr(644,root,root,755)
%{_libdir}/libmysofa.a
