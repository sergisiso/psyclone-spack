# PSyclone Spack Software Stack

## Introduction

This repository contains the Spack packages and recipes to build the software
stacks necessary to build PSyclone applications: LFRic, NEMO, NUMA3d, ...

## Initial set up

To install the latest version of Spack with:
`git clone -c feature.manyFiles=true https://github.com/spack/spack.git spack-repo`

Install the compilers (alternatively point to locally installed compilers):
```
spack install gcc%11.2.0+nvptx
spack install intel-oneapi-compilers
spack install nvhpc
```

Set up compilers file:
```
spack compiler find
spack compilers
```

Not all necessary software is available on the upstream Spack, so we provide an
additional set of spack recipes that include all LFRic dependencies.
`spack repo add repo_additional_packages`

## Spack Usage

Now, applications/libraries listed on Spack can be installed with:
`spack install <application>`

Before installing one can use the commands:
- `spack info <application>` to see the available versions and variants
- `spack spec <application>` to see which dependencies will be installed

It is sometimes useful to use the `-U` (`--fresh`) option to concretize the
dependencies without using the already installed packages, so that all dependencies
use the chosen compiler. For example:

```bash
spack install -U lfric-buildenv %aocc +xios
```

Once installed, a package can be loaded and its files located with:
```bash
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
