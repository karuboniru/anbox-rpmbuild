%global extrarel        14.10.20140730

Name:       properties-cpp
Version:    0.0.1
Release:    2.%{extrarel}%{?dist}
Summary:    Simple convenience library for handling properties and signals in C++11

License:    LGPLv3+
URL:        https://launchpad.net/properties-cpp
Source0:    https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/%{name}/%{version}+%{extrarel}-0ubuntu1/%{name}_%{version}+%{extrarel}.orig.tar.gz

BuildArch:      noarch
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz

%description
A very simple convenience library for handling properties and signals in C++11.

%package devel
Summary:        Development files for properties-cpp

%description devel
Development files for properties-cpp, a simple convenience library for handling
properties and signals in C++11.

%prep
%autosetup -p1 -n %{name}-%{version}+%{extrarel}
# Debian packaging stuff
sed -i "/include(cmake\/PrePush.cmake)/d" CMakeLists.txt
# Code coverage is not needed
sed -i "/include(cmake\/EnableCoverageReport.cmake)/d" CMakeLists.txt
# Test binaries are not needed
sed -i "/add_subdirectory(tests)/d" CMakeLists.txt

%build
mkdir build && cd build
%cmake ..
%make_build

%install
cd build
%make_install
mkdir -p %{buildroot}%{_datadir}/pkgconfig
mv %{buildroot}%{_libdir}/pkgconfig/%{name}.pc %{buildroot}%{_datadir}/pkgconfig/%{name}.pc

%files devel
%doc README.md
%license COPYING
%{_pkgdocdir}/html/
%{_includedir}/core/
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Thu Dec 05 2019 Qiyu Yan <3437889+karuboniru@users.noreply.github.com> - 0.0.1-2.14.10.20140730
- rebuilt

* Sun Jul 21 17:44:18 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.0.1-1.14.10.20140730
- Initial package