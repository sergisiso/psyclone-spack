# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.xios import Xios as BaseXios


class Xios(BaseXios):

    """Extension of builtin XIOS package."""

    # LFRic requires the following:
    # http://forge.ipsl.jussieu.fr/ioserver/svan/XIOS/trunk revision=2252
    # https://forge.ipsl.jussieu.fr/ioserver/browser/XIOS2

    version("develop", svn="http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS2/trunk")
    version("2.5.2252", revision=2252,  svn="http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS2/trunk")

    depends_on("blitz")
    depends_on("subversion", type="build")


    def patch(self):

        """Patch GCC 12 header problems.

        With GCC 12, some lesser-used C++ header files are no longer
        included by default.  This causes XIOS to fail to build and
        the following patches the missing array header files back in.
        """

        if self.spec.satisfies("%gcc@12:"):
            # Note that the replacements are not r-strings because they
            # need to contain newlines
            filter_file(r"^(#include\s*<vector>\s*)$",
                        "#include <array>\n\\1",
                        "src/xios_spl.hpp",
                        backup=True)

            filter_file(r"^(#include\s*<list>\s*)$",
                        "#include <array>\n\\1",
                        "extern/remap/src/elt.hpp",
                        backup=True)

        return

    def xios_fcm(self):

        """Create an fcm configuration for the current system.

        Override the method in the base package to create a modified
        fcm configuration for the latest releases of XIOS.  Fixes
        include the addition of the -lstdc++ flag and a flag to
        support long source lines in gfortran.
        """

        file = join_path("arch", "arch-SPACK.fcm")
        spec = self.spec
        param = dict()
        param["MPICXX"] = spec["mpi"].mpicxx
        param["MPIFC"] = spec["mpi"].mpifc
        param["CC"] = self.compiler.cc
        param["FC"] = self.compiler.fc
        param["BOOST_INC_DIR"] = spec["boost"].prefix.include
        param["BOOST_LIB_DIR"] = spec["boost"].prefix.lib
        param["BLITZ_INC_DIR"] = spec["blitz"].prefix.include
        param["BLITZ_LIB_DIR"] = spec["blitz"].prefix.lib
        if spec.satisfies("%apple-clang"):
            param["LIBCXX"] = "-lc++"
        else:
            param["LIBCXX"] = "-lstdc++"

        if spec.satisfies("%gcc"):
            # Allow long lines in gfortran
            param["FFLAGS"] = "-ffree-line-length-none"
        else:
            param["FFLAGS"] = ""

        # Note: removed "%intel", "%apple-clang", "%clang", "%fj" from
        # the list on the assumption that the flags will need changing
        # to work with these compilers
        if any(map(spec.satisfies, ("%gcc",  "%cce"))):
            text = r"""
%CCOMPILER      {MPICXX}
%FCOMPILER      {MPIFC}
%LINKER         {MPIFC}

%BASE_CFLAGS    -ansi -w -D_GLIBCXX_USE_CXX11_ABI=0 \
                -I{BOOST_INC_DIR} -std=c++11
%PROD_CFLAGS    -O3 -DBOOST_DISABLE_ASSERTS
%DEV_CFLAGS     -g -O2
%DEBUG_CFLAGS   -g

%BASE_FFLAGS    -D__NONE__ {FFLAGS}
%PROD_FFLAGS    -O3
%DEV_FFLAGS     -g -O2
%DEBUG_FFLAGS   -g

%BASE_INC       -D__NONE__
%BASE_LD        -L{BOOST_LIB_DIR} {LIBCXX}

%CPP            {CC} -E
%FPP            {CC} -E -P -x c
%MAKE           gmake
""".format(
                **param
            )

        else:
            raise InstallError("Unsupported compiler.")

        with open(file, "w") as f:
            f.write(text)
