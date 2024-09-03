import os
from spack.package import *


class NemoBuildEnvironment(BundlePackage):
    """
    NemoBuildEnvironment contains everything needed to build NEMO.
    """

    version("2024.04")
    variant("xios", default=True, description="Enable XIOS support")

    depends_on("perl", type="run")
    depends_on("perl-uri")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi")
    depends_on("mpi")

    # depends_on("xios@2.5", when="+xios")  # Using same than LFRic

    def setup_run_environment(self, env):
        """ Set-up the environment variables that the arch files use. """
        env.set('FC', self.compiler.fc)
        env.set('CC', self.compiler.cc)
        env.set('CXX', self.compiler.cxx)
        env.set('MPIFC', self.spec["mpi"].mpifc)

        env.set("HDF5_HOME", self.spec["hdf5"].prefix)
        env.set("NCDF_F_HOME", self.spec["netcdf-fortran"].prefix)
        env.set("NCDF_C_HOME", self.spec["netcdf-c"].prefix)
        env.append_path("LD_LIBRARY_PATH", self.spec["netcdf-fortran"].prefix.lib)
        env.append_path("LD_LIBRARY_PATH", self.spec["netcdf-c"].prefix.lib)
        env.append_path("PERL5LIB", self.spec["perl-uri"].prefix.lib + "/perl5")
        if "xios" in self.spec:
            env.set("XIOS_HOME", self.spec["xios"].prefix)
