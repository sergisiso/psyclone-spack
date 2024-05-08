# PSyclone Spack Software Stack

This repository contains the Spack packages necessary to build all applications
targeted by PSyclone, such as: LFRic, NEMO, PSycloneBench, CROCO, NUMA3d, ...
in addition to the reframe performance testing framework and some additional
benchmarks.

## Initial set up

Install the latest version of Spack:
```bash
git clone -c feature.manyFiles=true https://github.com/spack/spack.git ~/.spack
```

Configure system packages and global settings:
```
cat <<EOF > ~/.spack/packages.yaml
packages:
    openssl:
        externals:
        - spec: openssl@`openssl version | awk '{print $2}'`
          prefix: /usr
        buildable: False
    subversion:
        externals:
        - spec: subversion@1.14
          prefix: /usr
        buildable: False
    all:
        variants: cuda_arch=70
EOF
```

Install the compilers (alternatively point to locally installed compilers):
```
spack install gcc@11+nvptx
spack install intel-oneapi-compilers
spack install nvhpc
spack install aocc
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


Not all necessary software is available on the Spack upstream, and some which are
available need patches. Add the additional packages by doing (order is important):
```bash
git clone git@github.com:MetOffice/simit-spack.git
spack repo add simit-spack/repos/metoffice
spack repo add repo_additional_packages
```

## Spack Usage

Applications/libraries listed on Spack (`spack list`) can be installed with:
```bash
spack install <application>
```

Before installing, use the commands:
- `spack info <application>` to see the available versions and variants
- `spack spec <application>` to see which dependencies will be installed

It is sometimes useful to use the `-U` (`--fresh`) option to concretize the
dependencies without using the already installed packages, so that all dependencies
use the chosen compiler. For example:

```bash
spack install -U lfric-buildenv %aocc +xios
```

Once installed, a package can be, found, loaded and its files located with:
```bash
spack find -x
spack load lfric-buildenv
spack locate -i lfric-buildenv
```

> **_NOTE:_**  Some build environments like LFRic, Nemo, PSycloneBench, ...
are created as packages (instead of Spack environments), this is because
even if no software is installed, it was easier to specify the different
compiler/variant/dependencies and the environment variables that must be
load/unloaded for each combination.

## Reframe

This repository also includes reframe python scripts to automate the testing
of multiple benchmarks and applications on multiple environments.

```bash
spack install reframe
```

All benchmarks use a Spack environment to install the application. This is
specified in the `self.build_system.specs` attribute. For example

```python
self.build_system.specs = ['babelstream%gcc+omp']
```

It also includes a `config.py` configuration file with information about the
multiple systems and job schedulers where the tests are executed. The reframe
tests can be triggered with:

```bash
reframe -C reframe/config.py -c reframe/benchmarks/babelstream.py -r --performance-report --keep-stage-files
```

If the workflow fails, it is recommended to go step by step:
1. Install the spack recipe manually (the environment will reuse the already installed one)
2. Run the staged `rfm_build.sh` (build process)
3. Run the staged `rfm_job.sh` (benchmark)

> **_NOTE:_** Reframe has been patched to ignore spack config options so that
by default it uses the same configuration/installations than the Spack packages
installed in the system.
