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
Release:        8%{?dist}
Summary:        Linux kernel with Salkim AMDGPU and ntsync IOCP improvements
License:        GPL-2.0-only
URL:            https://github.com/nanomatters/linux-cachyos
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

Source0:        https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-%{version}.tar.xz
Source1:        config

# Match linux-salkim/PKGBUILD's GCC path (without dkms-clang.patch).
Patch001:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/5d4a24ec3ba553bf577ea4d74804dee99a7df910.patch
Patch002:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/f64ad63b551bfef7f20b16ea8cfa030b3b4a9bad.patch
Patch003:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/22763a52e0894f7e31b8acc7047e0cb3f70d9eba.patch
Patch004:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/39e5b1e4f4b3e623d398299f4429756e4935a3f6.patch
Patch005:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/831fac2ac5edce9f829db0d74d852409c8ab16a0.patch
Patch006:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/871467ce5bce5c7af5d278ffa0442c49dddb82b6.patch
Patch007:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/74a61f46f3e1ec4cc6c0044358746ce573fc175b.patch
Patch008:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/063eec35f42d216daee7383e9f2bcc314f45a27a.patch
Patch009:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/25c4e6feb856075e7bcc37f03b28936a9aa954fb.patch
Patch010:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/2770817a7dd90bb80d9147123dd2d2fcb5ccf258.patch
Patch011:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/2a03ddb7740478287721feb469e359b5961e3e6e.patch
Patch012:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/81d84cb547a26df07cfb40932e66a27fccc6b9c1.patch
Patch013:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/af21fb73ee028ca95222005904de7c653a0f7371.patch
Patch014:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/44d0d3031e47973ed65fd327669d5e2eaaf6c565.patch
Patch015:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/955418796b2933be41c197b8b210da9191da29f7.patch
Patch016:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/030d47cc6720e0f07b502876cdbd266e309f9461.patch
Patch017:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/bebad45050945a3d668d6701fb77ae2571c5d44b.patch
Patch018:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/6675c4642b9aa7c44ac29e46ed83bbd830a379dd.patch
Patch019:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/1f47aaf3ff0d86365fab6f5bf6ec5f3ec1427655.patch
Patch020:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/fa3389c71379998525aaef4c04c30de9db81a52c.patch
Patch021:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/8b607d6f54b0049923369abecc9133b3c9fe10ca.patch
Patch022:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/640fd039dc8bd88d5edc98b2d55aaa6f677adf39.patch
Patch023:       https://gitlab.freedesktop.org/agd5f/linux/-/commit/dd601ed4ce28efe8b1452b9323a2c5499060d71b.patch
Patch024:       https://gitlab.freedesktop.org/drm/amdgpu/kernel/-/commit/5fd3b60d9b80bfe8b880336b5486309c69cf3865.patch
Patch025:       https://github.com/CachyOS/linux/commit/6f11071b4a1a305d42e61fb7d943c703cbdbd6fb.patch
Patch026:       https://github.com/CachyOS/linux/commit/5a42488d82a8df3e22507259babfc45fd88d820a.patch
Patch027:       https://github.com/CachyOS/linux/commit/96f023bb8c13bbe6662f28da97cf5b5787e58fe1.patch
Patch028:       https://gitlab.freedesktop.org/drm/misc/kernel/-/commit/3be436cbd3d265fe4fcfbb5b650edad7b2108443.patch
Patch029:       https://gitlab.freedesktop.org/drm/misc/kernel/-/commit/cb104d395da48d965665fefe8502f71b6e7e3733.patch
Patch030:       https://gitlab.freedesktop.org/drm/misc/kernel/-/commit/fd485d47437ba1700dd47205a63b9f389a00aa36.patch
Patch031:       https://gitlab.freedesktop.org/drm/misc/kernel/-/commit/b537d87d2632c9a72afa08755b2de89a5b3ab70f.patch
Patch032:       https://gitlab.freedesktop.org/drm/misc/kernel/-/commit/1ba6405638439a4214783965538b0196c8de8a5b.patch
Patch033:       local-0001-amdgpu-separate-tlb-invalidation-fences.patch
Patch034:       local-0002-ntsync-add-iocp-support.patch
Patch035:       local-0003a-amdgpu-fix-dependency-fence-references.patch
Patch036:       local-0003b-amdgpu-preserve-sdma-rollover-jobs.patch
Patch037:       local-0003c-amdgpu-retain-failed-vm-clears.patch
Patch038:       local-0003d-amdgpu-complete-failed-vm-updates.patch
Patch039:       local-0003e-amdgpu-factor-vm-update-helpers.patch
Patch040:       local-0003f-amdgpu-batch-bo-mapping-updates.patch
Patch041:       local-0003g-amdgpu-batch-freed-range-updates.patch
Patch042:       local-0004-amdgpu-send-hdmi-vrr-metadata-in-vtem-slot.patch
Patch043:       local-0005-amdgpu-batch-sparse-va-operations.patch
Patch044:       local-0006-amdgpu-share-sparse-bo-update-batches.patch
Patch045:       local-0007-amdgpu-share-prt-update-batches.patch
Patch046:       local-0008-amdgpu-grow-sdma-update-buffers.patch
Patch047:       local-0009-amdgpu-scope-batch-retirements.patch
Patch048:       local-0010-amdgpu-honor-completed-sparse-dependencies.patch
Patch049:       local-0011-amdgpu-honor-passive-vrr-in-vtem.patch
Patch050:       local-0012-amdgpu-fallback-to-cea-vrr-ranges.patch
Patch051:       local-0013-amdgpu-enable-hdmi-vrr-on-pcon.patch
Patch052:       local-0014-amdgpu-complete-allm-mode-signalling.patch
Patch053:       local-0015-drm-parse-amd-freesync-ranges.patch
Patch054:       local-0016-amdgpu-use-common-freesync-parser.patch

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
%setup -q -n linux-%{version}
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
