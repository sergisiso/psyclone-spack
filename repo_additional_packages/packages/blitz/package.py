# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.blitz import Blitz as BaseBlitz


class Blitz(BaseBlitz):

    """N-dimensional arrays for C++"""

    version(
        "1.0.1",
        sha256="b62fc3f07b64b264307b01fec5e4f2793e09a68dcb5378984aedbc2e4b3adcef",
    )
    version(
        "1.0.0",
        sha256="79c06ea9a0585ba0e290c8140300e3ad19491c45c1d90feb52819abc3b58a0c1",
    )

    depends_on("python@:2.7", type="build", when="@:1.0.1")
    depends_on("python@3:", type="build", when="@1.0.2:")

    # FIXME: Check whether this is required on non-ARM platforms
    depends_on("autoconf", type="build", when="@1.0.2 build_system=autotools")
    depends_on("automake", type="build", when="@1.0.2 build_system=autotools")
    depends_on("libtool", type="build", when="@1.0.2 build_system=autotools")

    force_autoreconf = True

    @run_before("autoreconf")
    def e_autogen(self):

        """Fix autotools problems.

        Removing these files fixes a problem with missing commands
        when autoreconf runs.  A re-run is required to fix a hardwired
        dependency on the tools used to bootstrap the distribution and
        to fix the compiler problem patched below.
        """

        remove("m4/lt~obsolete.m4")
        remove("m4/ltoptions.m4")
        remove("m4/ltsugar.m4")
        remove("m4/ltversion.m4")
        remove("m4/libtool.m4")


    def patch(self):

        """Fix compiler vendor detection macros.

        Compiler vendor detection is broken on the Cray EX.  This adds
        a default to the m4 definition to target llvm when using a
        recent version of cce.
        """

        if "%cce" in self.spec and self.compiler.version >= ver(15):
            # Add a default compiler vendor and set it to llvm if
            # using a recent Cray compiler
            filter_file("^\)", "[COMPILER_VENDOR=\"llvm\"]\n)",
                        "m4/ac_compiler_specific_header.m4")
