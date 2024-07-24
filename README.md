# PSyclone Spack Software Stack

This repository contains the Spack packages necessary to build all applications
targeted by PSyclone, such as: LFRic, NEMO, PSycloneBench, CROCO, NUMA3d, ...

## Initial set up

To install them you need Spack and the MetOffice Simit packages, for convenience
these are both submodules of this repository with exact versions that have worked
before, but you can only use external installations. To use the submodules do:
```bash
git submodule update --init
```

Then configure Spack settings, add your configs to:
  - spack-repo/etc/spack/ to affect only this spack instance but for all users.
  - or ~/.spack/ to affect all spack instances but only for this user.
In the one you choose add a `packages.yaml` with:
```
packages:
    openssl:
        buildable: false
        externals:
        - spec: openssl@`openssl version | awk '{print $2}'`
          prefix: /usr
        buildable: False
    subversion:
        buildable: false
        externals:
        - spec: subversion@1.14
          prefix: /usr
        buildable: False
    all:
        variants: cuda_arch=70
```
Choose the "cuda_arch" by using: https://developer.nvidia.com/cuda-gpus

If your system needs specific installations e.g. cuda for WSL or MPI with
specific system configurations, also add them here:
```
    cuda:
        buildable: false
        externals:
        - spec: cuda@12.2
          prefix: /usr/lib/wsl/
```

Install the compilers:
```
spack install gcc +nvptx
spack install intel-oneapi-compilers
spack install nvhpc
spack install aocc
spack install llvm +cuda +flang +libomptarget +libomptarget_debug +mlir
```

Set up the Spack compilers configuration:
```bash
spack compiler find
spack compilers
```
and edit the flags in `spack config edit compilers`. For example adding:
```
    flags:
      cflags: -O2 -g -fno-omit-frame-pointer
      fflags: -O2 -g -fno-omit-frame-pointer
      cxxflags: -O2 -g -fno-omit-frame-pointer
      cppflags: -O2 -g -fno-omit-frame-pointer
      ldflags: -O2 -g -fno-omit-frame-pointer
```
to add debug symbols and frame pointers to all installed packages.

Not all necessary software is available on the Spack upstream repository, and some
of the available packages need patches. Add the additional packages needed by doing
(order is important):
```bash
spack repo add simit-spack/repos/metoffice
spack repo add psyclone_additional_packages
```

After this you can list them using: `spack repo list`

## Spack Usage

Applications/libraries listed on Spack (`spack list`) can be installed with:
```bash
spack install <application>
```

Before installing, use the commands:
- `spack info <application>` to see the available versions and variants
- `spack spec <application>` to see which dependencies will be installed

It is sometimes useful to use the `-U` (`--fresh`) option to concretize the
dependencies without preferring the already installed packages. For example:

```bash
spack install -U lfric-buildenv %aocc +xios
```

Once installed, a package can be, found, loaded and its files located with:
```bash
spack find -x
spack load lfric-buildenv
spack locate -i lfric-buildenv
```

This repository provides:
- lfric-buildenv
- nemo-buildenv

> **_NOTE:_** These are provided as packages (instead of Spack environments)
because it was easier to specify the different compiler/variant/dependencies
to build and load different combinations of them, and each comes with shell
environment variables that are used during the applications building step
outside spack.
