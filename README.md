# PSyclone Spack Software Stack

This repository contains the Spack packages necessary to build some applications
that have PSyclone as part of their build system. As such, these packages do not
install the final applications nor PSyclone itself. Instead they provide the
necessary dependencies and environment variables (FC, LD_LIBRARY_PATH, ...)
to build each application. You need your own version of PSyclone. Currently, this
repository has:

- lfric-build-environment
- nemo-build-environment

> **_NOTE:_**  Spack bundle packages were chosen over spack environments because
they have more flexibility to chose compiler/variant/dependencies when installing
them and they allow to set up environment variables when loading the package.

## Initial set up

To install them you need Spack and the MetOffice Simit repositories, for convenience
these are both submodules of this repository with the exact versions that have worked
before, but you can also use external installations. To use the submodules do:
```bash
git submodule update --init
```

Now, add Spack to your environment with:
```bash
source ${PWD}/spack-repo/share/spack/setup-env.sh
```

Then configure Spack settings, config files can be added to:
  - ${PWD}/spack-repo/etc/spack/ to affect only this spack instance but for all users.
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
Choose the right "cuda_arch" by using: https://developer.nvidia.com/cuda-gpus

If your system needs specific installations e.g. cuda for WSL or MPI with
specific system configurations, also add them here:
```
    # Modify spack-repo/var/spack/repos/builtin/packages/cuda/package.py:
    # find_libraries("libcudart" -> find_libraries("libcuda"
    cuda:
        buildable: false
        externals:
        - spec: cuda@12.5
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

Set up the Spack compilers configuration (N.B. you may need to e.g. `spack load nvhpc`
before spack will find the new compilers):
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

The reason to provide packages that overlap with the ones in Spack and Simit are:

- Blitz: Simit is out-of-date with its base version which uses cmake, this repo
has a copy of the base version.
- XIOS: this repo adds fixes for gcc>12 and nvhpc. Note that it needs to be
installed specifying the same compiler for the mpi. For instance:
`spack install xios%nvhpc ^openmpi%nvhpc`
- rose_picker: The repository is password-protected, this repo distributes the
source in a tar file.
- fcm: Skips one perl dependency that can't be compiled with latest gcc.

## Spack Usage

Applications/libraries listed on Spack (`spack list`) can be installed with:
```bash
spack install <application>
```

Before installing, use the commands:
- `spack info <application>` to see the available versions and variants
- `spack spec <application>` to see which dependencies will be installed

It is sometimes useful to use the `-U` (`--fresh`) option to concretize the
dependencies without preferring the already installed packages:

```bash
spack install lfric-buildenv%nvhpc ^openmpi%nvhpc
```

Once installed, a package can be, found, loaded and its files located with:
```bash
spack find -x
spack load lfric-buildenv%nvhpc
spack location -i lfric-buildenv
```
