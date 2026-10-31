# Fedora packaging adapted from CachyOS/copr-linux-cachyos:
# sources/kernel-cachyos/kernel-cachyos-server.spec

# Kernel modules are stripped before signing by modules_install.
# RPM's generic post-install processing must not alter them afterwards.
%global debug_package %{nil}
%global __spec_install_post %{nil}
%global _build_id_links none
%global _default_patch_fuzz 0
%global _disable_source_fetch 0
%undefine _auto_set_build_flags
%undefine _include_frame_pointers

Name:           kernel-salkim
Version:        7.3
Release:        9%{?dist}
Summary:        Linux kernel with Salkim AMDGPU and ntsync IOCP improvements
License:        GPL-2.0-only
URL:            https://github.com/nanomatters/kernel-salkim
ExclusiveArch:  x86_64
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-modules = %{version}-%{release}
Provides:       installonlypkg(kernel)

BuildRequires:  bc
BuildRequires:  binutils
BuildRequires:  bison
BuildRequires:  bindgen-cli >= 0.71.1
# Rust's bindgen uses libclang even when C code is built with GCC.
BuildRequires:  clang-libs
BuildRequires:  dwarves
BuildRequires:  elfutils-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  kmod
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  perl-interpreter
BuildRequires:  python3
BuildRequires:  rsync
BuildRequires:  rust >= 1.85.0
BuildRequires:  rust-src
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  zstd

# Final x.y releases use x.y.0 in the kernel release string.
%global kernel_version %{lua: local v = rpm.expand("%{version}"); print(v:match("^%d+%.%d+$") and v .. ".0" or v)}
%global kver %{kernel_version}-%{release}.%{_arch}
%global kernel_dir /usr/lib/modules/%{kver}
%global devel_dir /usr/src/kernels/%{kver}

%global kernel_branch salkim-7.3

Source0:        %{url}/archive/refs/heads/%{kernel_branch}.tar.gz
Source1:        config

# Match PKGBUILD's GCC path. Driver and IOCP changes are already in the branch.
Patch001:       https://github.com/CachyOS/linux/commit/96f023bb8c13bbe6662f28da97cf5b5787e58fe1.patch
Patch002:       local-0018-amdgpu-preserve-dp-vrr-range-extension.patch

%description
Salkim's Linux kernel with AMDGPU sparse-mapping optimisations, HDMI/VRR
fixes and ntsync IOCP support. This package installs the matching kernel
image and modules.

%package core
Summary:        Kernel image for %{name}
AutoReq:        no
Provides:       kernel = %{version}-%{release}
Provides:       kernel-uname-r = %{kver}
Provides:       kernel-core-uname-r = %{kver}
Provides:       installonlypkg(kernel)
Requires:       kernel-modules-uname-r = %{kver}
Requires:       dracut
Requires(posttrans): /usr/bin/kernel-install
Requires(posttrans): /usr/sbin/depmod
Requires(preun): /usr/bin/kernel-install
Recommends:     linux-firmware

%description core
The Salkim kernel image, configuration and symbol map.

%package modules
Summary:        Kernel modules for %{name}
Provides:       kernel-modules = %{version}-%{release}
Provides:       kernel-modules-core = %{version}-%{release}
Provides:       kernel-modules-extra = %{version}-%{release}
Provides:       kernel-modules-uname-r = %{kver}
Provides:       kernel-modules-core-uname-r = %{kver}
Provides:       kernel-modules-extra-uname-r = %{kver}
Provides:       installonlypkg(kernel-module)
Requires:       kernel-uname-r = %{kver}

%description modules
All in-tree modules for the matching Salkim kernel.

%package devel
Summary:        Development files for building modules against %{name}
AutoReqProv:    no
Provides:       kernel-devel = %{version}-%{release}
Provides:       kernel-devel-uname-r = %{kver}
Provides:       installonlypkg(kernel)
Requires:       bc
Requires:       binutils
Requires:       dwarves
Requires:       elfutils-libelf-devel
Requires:       findutils
Requires:       gcc
Requires:       make
Requires:       openssl-devel
Requires:       perl-interpreter
Requires:       python3
Requires:       rust
Requires:       rust-src

%description devel
Headers, generated build files and tools for building external modules
against the matching Salkim kernel.

%package devel-matched
Summary:        Matching Salkim kernel and development files
Provides:       kernel-devel-matched = %{version}-%{release}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description devel-matched
Installs matching Salkim kernel and development packages.

%prep
%setup -q -n kernel-salkim-%{kernel_branch}
%autopatch -p1
cp %{SOURCE1} .config

# COPR builds must run on other machines and retain Fedora's SELinux policy.
scripts/config -d X86_NATIVE_CPU -d LOCALVERSION_AUTO \
    --set-str LOCALVERSION "" --set-str DEFAULT_HOSTNAME "(none)" \
    -e SECURITY_SELINUX \
    --set-str LSM "landlock,lockdown,yama,integrity,selinux,bpf"

# Use GCC without LTO; retain the other default Salkim build options.
scripts/config -d LTO_CLANG_FULL -d LTO_CLANG_THIN -d LTO_CLANG_THIN_DIST -e LTO_NONE \
    -d HZ_300 -e HZ_1000 --set-val HZ 1000 \
    -d HZ_PERIODIC -d NO_HZ_IDLE -e NO_HZ_FULL \
    -e PREEMPT -d PREEMPT_LAZY \
    -d TRANSPARENT_HUGEPAGE_MADVISE -e TRANSPARENT_HUGEPAGE_ALWAYS
printf '%s\n' '-%{release}.%{_arch}' > localversion.salkim
%make_build CC=gcc HOSTCC=gcc olddefconfig
test "$(make -s CC=gcc HOSTCC=gcc kernelrelease)" = "%{kver}"

%build
export KBUILD_BUILD_USER=salkim
export KBUILD_BUILD_HOST=copr
%make_build CC=gcc HOSTCC=gcc all

%install
install -Dm644 "$(make -s CC=gcc HOSTCC=gcc image_name)" \
    %{buildroot}%{kernel_dir}/vmlinuz
install -m644 .config %{buildroot}%{kernel_dir}/config
install -m644 System.map %{buildroot}%{kernel_dir}/System.map
zstd -q -19 -c Module.symvers > %{buildroot}%{kernel_dir}/symvers.zst
ZSTD_CLEVEL=9 %make_build CC=gcc HOSTCC=gcc INSTALL_MOD_PATH=%{buildroot}/usr \
    INSTALL_MOD_STRIP=1 DEPMOD=true modules_install

# Use the kernel's maintained external-module build tree installer.
%make_build CC=gcc HOSTCC=gcc run-command \
    KBUILD_RUN_COMMAND='./scripts/package/install-extmod-build %{buildroot}%{devel_dir}'
install -m644 .config System.map %{buildroot}%{devel_dir}/
if grep -q '^CONFIG_DEBUG_INFO_BTF_MODULES=y' .config; then
    objcopy --only-section=.BTF --set-section-flags .BTF=alloc,readonly \
        --strip-all vmlinux %{buildroot}%{devel_dir}/vmlinux
fi
if grep -q '^CONFIG_RUST=y' .config; then
    install -d %{buildroot}%{devel_dir}/rust
    find rust -maxdepth 1 -type f \( -name '*.rmeta' -o -name '*.so' \) \
        -exec cp -t %{buildroot}%{devel_dir}/rust {} +
    find rust -type f -name 'generated_*.rs' \
        -exec cp --parents -t %{buildroot}%{devel_dir} {} +
fi
rm -f %{buildroot}%{kernel_dir}/build
ln -s %{devel_dir} %{buildroot}%{kernel_dir}/build
ln -s %{devel_dir} %{buildroot}%{kernel_dir}/source

# Track files that depmod creates after installation.
{
    echo '%dir %{kernel_dir}'
    echo '%{kernel_dir}/kernel'
    find %{buildroot}%{kernel_dir} -maxdepth 1 -type f -name 'modules.*' \
        -printf '%{kernel_dir}/%f\n'
    for suffix in alias alias.bin builtin.alias.bin builtin.bin dep dep.bin \
                  devname softdep symbols symbols.bin weakdep; do
        printf '%s\n' "%%ghost %{kernel_dir}/modules.$suffix"
    done
} > modules.list

%posttrans core
/usr/sbin/depmod -a %{kver} || exit $?
# Booted ostree systems and container image builds manage boot entries separately.
if [ ! -e /run/ostree-booted ] && [ -d /run/systemd/system ]; then
    /usr/bin/kernel-install add %{kver} %{kernel_dir}/vmlinuz || exit $?
fi

%preun core
if [ ! -e /run/ostree-booted ] && [ -d /run/systemd/system ]; then
    /usr/bin/kernel-install remove %{kver} || exit $?
fi

%files

%files core
%license COPYING
%{kernel_dir}/vmlinuz
%{kernel_dir}/config
%{kernel_dir}/System.map
%{kernel_dir}/symvers.zst
%ghost /boot/initramfs-%{kver}.img
%ghost /boot/vmlinuz-%{kver}

%files modules -f modules.list

%files devel
%license COPYING
%{devel_dir}
%{kernel_dir}/build
%{kernel_dir}/source

%files devel-matched
