import os
from spack.package import *


class NemoBuildenv(BundlePackage):
    """
    NemoBuildEnv contains everything needed to build NEMO.
    """

    version("2024.04")
    variant("xios", default=True, description="Enable XIOS support")

    depends_on("perl", type="run")
    depends_on("perl-uri")
    depends_on("mpi")
    depends_on("netcdf-fortran", type="link")
    depends_on("xios@2.5", when="+xios")  # Using same than LFRic

    def setup_run_environment(self, env):
        """ Set-up the environment variables that the arch files use. """
        env.append_flags("HDF5_HOME", self.spec["hdf5"].prefix)
        env.append_flags("NCDF_F_HOME", self.spec["netcdf-fortran"].prefix)
        env.append_flags("NCDF_C_HOME", self.spec["netcdf-c"].prefix)
        env.append_flags("LD_LIBRARY_PATH", self.spec["netcdf-fortran"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["netcdf-c"].prefix.lib, sep=":")
        env.append_flags("PERL5LIB", self.spec["perl-uri"].prefix.lib + "/perl5", sep=":")
        if "xios" in self.spec:
            env.append_flags("XIOS_HOME", self.spec["xios"].prefix)
