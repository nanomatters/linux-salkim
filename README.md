# Linux Salkim

Linux kernel packages with Salkim's AMDGPU and ntsync IOCP changes.

## CachyOS / Arch Linux

From the repository root, build and install with:

```sh
cd linux-salkim-7.3
makepkg -si
```

Use `linux-salkim-7.4` for the 7.4 release-candidate packages.

## Fedora

Install prebuilt packages from [COPR](https://copr.fedorainfracloud.org/coprs/darginmahkum/salkim_kernel/):

```sh
sudo dnf copr enable darginmahkum/salkim_kernel
sudo dnf install kernel-salkim
```

Alternatively, build RPMs from the [7.3 spec](linux-salkim-7.3/kernel-salkim.spec)
or the [7.4 spec](linux-salkim-7.4/kernel-salkim.spec).
The matching configuration and local patches are in the same directory.

Install `kernel-salkim-devel-matched` if you need to build external kernel modules.
Secure Boot requires signing the kernel with a trusted key.

After installation, reboot into the Salkim kernel. Keep your existing kernel
installed as a fallback.
