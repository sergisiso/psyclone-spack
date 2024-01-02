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

Now, applications/libraries listed on Spack can be installed with:
`spack install <application>`

However, in our case we are not trying to install the final applications
themself, but all of their dependencies, so that we can run their build
system manually (using psyclone):

For this we will use "spack environments", which are like bundles of
packages (e.g. all the dependencies needed to build an application) 

```bash
# Create lfric environment
spack env create lfric-gnu environments/lfric.yaml
spack env activate

# Install necessary packages
spack install
```

## Usage

List available environments
spack env list

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
