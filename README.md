# PSyclone Spack Software Stack

## Introduction

This repository contains the Spack packages and recipes to build the software
stacks necessary to build PSyclone applications: LFRic, NEMO, NUMA3d, ...

## Initial set up

To install the latest version of Spack with:
`git clone -c feature.manyFiles=true https://github.com/spack/spack.git spack-repo`

Install the compilers (alternatively point to locally installed compilers):
```
spack install gcc+nvptx ^cuda@10
spack install intel-oneapi-compilers
spack install nvhpc
spack install aocc
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



