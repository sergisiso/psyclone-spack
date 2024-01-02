import os
from spack.package import *


class LfricBuildenv(Package):
    """
    LFRic BuildEnvironment is everything needed to build LFRic
    """

    source_path = os.path.dirname(os.path.realpath(__file__))
    maintainers = ['']

    variant("xios", default=True, description="Enable XIOS support")
    version(
        "2024.01",
        '77518a79558d45638bf070ec6af41ea5f86096fb6d0cc90784909dc0ae6c0a95',
        expand=False,
        url="file://"+source_path+"/empty_file.py"
    )
    
    def url_for_version(self, version):
        return os.path.join("dev", "null")

    depends_on("mpich@3.2")
    depends_on("netcdf-fortran")
    depends_on("yaxt@0.9.0 idxtype=long")
    depends_on("pfunit@3 max_array_rank=6 +mpi +openmp")
    depends_on("fcm")
    depends_on("rose-picker")
    
    # XIOS is optional and has to be requested with +xios
    depends_on("xios@2.5.2252", when="+xios")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.set('FC', "gfortran")
        env.set('CC', "gcc")
        env.set('CXX', "g++")
        env.set('FPP', "cpp -traditional-cpp")
        env.set('LDMPI', "mpif90")

        env.append_flags("FFLAGS", self.spec["mpich"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["xios"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["netcdf-fortran"].headers.include_flags)
        env.append_flags("FFLAGS", self.spec["yaxt"].headers.include_flags)

        env.append_flags("LDFLAGS", self.spec["mpich"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["xios"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["netcdf-fortran"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["netcdf-c"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["hdf5"].libs.ld_flags)
        env.append_flags("LDFLAGS", self.spec["yaxt"].libs.ld_flags)

        env.append_flags("LD_LIBRARY_PATH", self.spec["mpich"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["xios"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["netcdf-fortran"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["netcdf-c"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["hdf5"].prefix.lib, sep=":")
        env.append_flags("LD_LIBRARY_PATH", self.spec["yaxt"].prefix.lib, sep=":")
