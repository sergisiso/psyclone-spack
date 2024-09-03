import os
from spack.package import *


class LfricBuildEnvironment(BundlePackage):
    """LFRicBuildEnvironment installs all the dependencies needed to build
    LFRic and when loaded populates the appropriate environment variables (FC,
    CC, CXX, FPP, LDMPI, FFLAGS, LDFLAGS and LD_LIBRARY_PATH).
   
    """
    version("2689")

    variant("xios", default=True, description="Enable XIOS support")

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("yaxt")
    depends_on("pfunit")
    depends_on("fcm")
    depends_on("rose-picker", type="run")
    depends_on("py-jinja2", type="run")

    # XIOS can be disabled with -xios
    # depends_on("xios@2.5.2252", when="+xios")
    depends_on("xios", when="+xios")

    def setup_run_environment(self, env):
        env.set('FC', self.compiler.fc)
        env.set('CC', self.compiler.cc)
        env.set('CXX', self.compiler.cxx)
        env.set('FPP', "cpp -traditional-cpp")
        env.set('LDMPI', self.spec["mpi"].mpifc)

        env.append_flags("FFLAGS", self.spec["mpi"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["mpi"].headers.include_flags + "/../lib")
        env.append_flags("FFLAGS", self.spec["netcdf-fortran"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["yaxt"].headers.include_flags)

        env.append_flags("LDFLAGS", self.spec["mpi"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["netcdf-fortran"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["netcdf-c"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["hdf5"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["yaxt"].libs.ld_flags)

        env.append_path("LD_LIBRARY_PATH", self.spec["mpi"].prefix.lib)
        env.append_path("LD_LIBRARY_PATH", self.spec["netcdf-fortran"].prefix.lib)
        env.append_path("LD_LIBRARY_PATH", self.spec["netcdf-c"].prefix.lib)
        env.append_path("LD_LIBRARY_PATH", self.spec["hdf5"].prefix.lib)
        env.append_path("LD_LIBRARY_PATH", self.spec["yaxt"].prefix.lib)

        if "xios" in self.spec:
            env.append_flags("FFLAGS", self.spec["xios"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["xios"].libs.ld_flags)
            env.append_path("LD_LIBRARY_PATH", self.spec["xios"].prefix.lib)
