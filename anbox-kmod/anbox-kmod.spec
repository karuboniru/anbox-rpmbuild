%global buildforkernels akmod
%global debug_package %{nil}

%global forgeurl        https://github.com/anbox/anbox-modules
%global commit          98f0f3b3b1eeb5a6954ca15ec43e150b76369086
%forgemeta

Name:           anbox-kmod
Summary:        Kernel module (kmod) for Anbox
Version:        0
Release:        0.3%{?dist}

# https://github.com/anbox/anbox-modules/issues/27
License:        GPLv2+
URL:            %{forgeurl}
Source:         %{forgesource}

BuildRequires:  kmodtool
BuildRequires:  elfutils-libelf-devel
BuildRequires:  buildsys-build-rpmfusion
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the kernel modules necessary to run the Anbox Android
container runtime. They're split out of the original Anbox repository to make
packaging in various Linux distributions easier.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%forgeautosetup -c -T -a 0

for kernel_version  in %{?kernel_versions} ; do
  cp -a anbox-modules-%{commit} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*}/ashmem modules
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*}/binder modules
done


%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 -t %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ $(find _kmod_build_${kernel_version%%___*}/ -name '*.ko')
 chmod u+x %{buildroot}%{_prefix}/lib/modules/*/extra/*/*
done
%{?akmod_install}


%changelog
* Sat May 30 2020 Qiyu Yan <yanqiyu01@gmail.com> - 0-0.3.20191205gite0a237e
- rebuilt

* Thu Dec 05 2019 Qiyu Yan <3437889+karuboniru@users.noreply.github.com> - 0-0.2.20191205gite0a237e
- rebuilt

* Sun Jul 21 15:47:39 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.1.20190721git816dd4d
- Initial package
