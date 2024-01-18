from spack.package import *


class Fcm(Package):
    """
    FCM is a build system for Fortran programs
    """

    homepage = "https://github.com/metomi/fcm"
    url = "https://github.com/metomi/fcm/archive/refs/tags/2021.05.0.tar.gz"

    maintainers = ["scottwales"]

    version(
        "2021.05.0",
        sha256="b4178b488470aa391f29b46d19bd6395ace42ea06cb9678cabbd4604b46f56cd",
    )

    depends_on("perl")
    depends_on("perl-alien-svn")
    depends_on("perl-config-inifiles")
    depends_on("perl-dbd-sqlite")
    depends_on("perl-digest-md5")
    depends_on("perl-time-piece")
    depends_on("perl-tk")
    depends_on("perl-xml-parser")
    depends_on("rsync")
    depends_on("subversion")

    def install(self, spec, prefix):
        install_tree(".", prefix)
