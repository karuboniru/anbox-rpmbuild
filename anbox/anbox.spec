%global forgeurl        https://github.com/anbox/anbox
%global commit          25e288436c937e7f4da56eac50167a549ac79294
%forgemeta


Name:       anbox
Version:    0
Release:    0.5%{?dist}
Summary:    Container-based approach to boot a full Android system on a GNU/Linux system

License:    GPLv3+
URL:        %{forgeurl}
Source:     %{forgesource}
# From Debian
Source1:    anbox-container-manager.service
Source2:    anbox-session-manager.service
Source3:    anbox.1
Source4:    anbox.desktop
Source5:    README.Fedora
# Patch0:     0001-convert-script-to-python3.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  boost-devel
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  protobuf-compiler
BuildRequires:  pkgconfig(lxc)
BuildRequires:  pkgconfig(properties-cpp)
BuildRequires:  pkgconfig(libpkgconf)
BuildRequires:  binutils-devel
BuildRequires:  pkgconfig(libdw)
BuildRequires:  libdwarf-devel
BuildRequires:  glm-devel
Requires:       anbox-common
Requires:       hicolor-icon-theme

# For SELinux
BuildRequires: selinux-policy-devel
Requires(post): policycoreutils
Requires(preun): policycoreutils
Requires(postun): policycoreutils

%description
Anbox is a container-based approach to boot a full Android system on a regular
GNU/Linux system like Ubuntu. In other words: Anbox will let you run Android on
your Linux system without the slowness of virtualization. Anbox uses Linux
namespaces (user, pid, uts, net, mount, ipc) to run a full Android system in a
container and provide Android applications on any GNU/Linux-based platform.

The Android inside the container has no direct access to any hardware. All
hardware access is going through the anbox daemon on the host. We're reusing
what Android implemented within the QEMU-based emulator for OpenGL ES
accelerated rendering. The Android system inside the container uses different
pipes to communicate with the host system and sends all hardware access commands
through these.

%prep
%forgeautosetup -p1
# Gmock cmake detection is specific to Debian
sed -i "/find_package(GMock)/d" CMakeLists.txt
# As a result, disable tests
sed -i "/add_subdirectory(tests)/d" CMakeLists.txt
cp %{S:5} .

%build
%cmake    -DANBOX_VERSION=%{version}-%{release} \
          -DANBOX_VERSION_SUFFIX=Fedora
%cmake_build

%install
%cmake_install
install -Dpm 0644 snap/gui/icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/anbox.png
install -Dpm 0755 scripts/anbox-bridge.sh %{buildroot}%{_datadir}/anbox/
install -Dpm 0755 scripts/anbox-shell.sh %{buildroot}%{_datadir}/anbox/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{S:4}
install -m 0755 -vd %{buildroot}%{_mandir}/man1/
install -m 0644 -vp %{S:3} %{buildroot}%{_mandir}/man1/
install -m 0755 -vd %{buildroot}%{_unitdir}/
install -m 0644 -vp  %{S:1} %{buildroot}%{_unitdir}/
install -m 0755 -vd %{buildroot}%{_userunitdir}/
install -m 0644 -vp  %{S:2} %{buildroot}%{_userunitdir}/
# cpu_features leftover
rm -rf %{buildroot}%{_bindir}/list_cpu_features
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_prefix}/lib/backward
rm -rf %{buildroot}%{_libdir}/cmake

# SELinux
mkdir selinux
cd selinux

cat << EOF > %{name}.te
module %{name} 1.0;

require {
    type unconfined_service_t;
    class binder set_context_mgr;
    class binder { call transfer };
}

#============= unconfined_service_t ==============
allow unconfined_service_t self:binder set_context_mgr;
allow unconfined_service_t self:binder call;
allow unconfined_service_t self:binder transfer;
EOF

make -f %{_datadir}/selinux/devel/Makefile
install -m 0755 -vd %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 0644 -vp anbox.pp %{buildroot}%{_datadir}/selinux/packages/%{name}/

%post
%systemd_post anbox-container-manager.service
%systemd_user_post anbox-session-manager.service
if [ "$1" -le "1" ] ; then # First install
semodule -i %{_datadir}/selinux/packages/%{name}/%{name}.pp 2>/dev/null || :
fi

%preun
%systemd_preun anbox-container-manager.service
%systemd_user_preun anbox-session-manager.service
if [ "$1" -lt "1" ] ; then # Final removal
semodule -r %{name} 2>/dev/null || :
fi

%postun
%systemd_postun_with_restart anbox-container-manager.service
if [ "$1" -ge "1" ] ; then # Upgrade
semodule -i %{_datadir}/selinux/packages/%{name}/%{name}.pp 2>/dev/null || :
fi

%files
%license COPYING.GPL
%doc AUTHORS README.md README.Fedora docs
%{_bindir}/anbox
%{_libdir}/libcpu_features.so
%{_datadir}/anbox
%{_datadir}/applications/anbox.desktop
%{_datadir}/icons/hicolor/512x512/apps/anbox.png
%{_datadir}/selinux/packages/%{name}/%{name}.pp
%{_mandir}/man1/anbox.1*
%{_unitdir}/anbox-container-manager.service
%{_userunitdir}/anbox-session-manager.service

%changelog
* Sun Jul 21 17:22:15 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.1.20190721gitcd829e9
- Initial package
