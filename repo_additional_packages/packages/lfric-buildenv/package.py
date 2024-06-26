import os
from spack.package import *


class LfricBuildenv(BundlePackage):
    """
    LFRicBuildEnv contains everything needed to build LFRic
    """
    version("2024.01")

    variant("xios", default=True, description="Enable XIOS support")

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("yaxt@0.9.0 idxtype=long")
    depends_on("pfunit max_array_rank=6 +mpi +openmp")
    depends_on("fcm")
    depends_on("rose-picker", type="run")
    depends_on("py-jinja2", type="run")

    # XIOS can be disabled with -xios
    depends_on("xios@2.5.2252", when="+xios")

    def setup_run_environment(self, env):
        env.set('FC', "gfortran")
        env.set('CC', "gcc")
        env.set('CXX', "g++")
        env.set('FPP', "cpp -traditional-cpp")
        env.set('LDMPI', "mpif90")

        env.append_flags("FFLAGS", self.spec["mpi"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["mpi"].headers.include_flags + "/../lib")
        env.append_flags("FFLAGS", self.spec["netcdf-fortran"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["yaxt"].headers.include_flags)

        env.append_flags("LDFLAGS", self.spec["mpi"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["netcdf-fortran"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["netcdf-c"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["hdf5"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["yaxt"].libs.ld_flags)

        env.append_flags("LD_LIBRARY_PATH", self.spec["mpi"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["netcdf-fortran"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["netcdf-c"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["hdf5"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["yaxt"].prefix.lib, sep=":")

        if "xios" in self.spec:
            env.append_flags("FFLAGS", self.spec["xios"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["xios"].libs.ld_flags)
            env.append_flags("LD_LIBRARY_PATH", self.spec["xios"].prefix.lib, sep=":")
