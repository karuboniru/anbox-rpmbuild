%global forgeurl        https://github.com/anbox/anbox-modules
%global commit          98f0f3b3b1eeb5a6954ca15ec43e150b76369086
%forgemeta

Name:           anbox-common
Summary:        Common package for Anbox Kernel module
Version:        0
Release:        0.3%{?dist}

# https://github.com/anbox/anbox-modules/issues/27
License:        GPLv2+
URL:            %{forgeurl}
Source:         %{forgesource}

Provides:       anbox-kmod-common = %{version}
Requires:       anbox-kmod >= %{version}
BuildRequires:  systemd-rpm-macros
BuildArch:      noarch

%description
This package contains tho udev rules necessary to use the Anbox kernel modules.

%prep
%forgeautosetup

%build
# Nothing to do

%install
install -m 0755 -vd %{buildroot}%{_sysconfdir}/modules-load.d/
install -m 0644 -vp anbox.conf %{buildroot}%{_sysconfdir}/modules-load.d/
install -m 0755 -vd %{buildroot}%{_udevrulesdir}/
install -m 0644 -vp 99-anbox.rules %{buildroot}%{_udevrulesdir}/

%files
%doc README.md
%{_sysconfdir}/modules-load.d/anbox.conf
%{_udevrulesdir}/99-anbox.rules

%changelog
* Thu Dec 05 2019 Qiyu Yan <3437889+karuboniru@users.noreply.github.com> - 0-0.2.20190721git816dd4d
- rebuilt

* Sun Jul 21 15:47:39 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.1.20190721git816dd4d
- Initial package
