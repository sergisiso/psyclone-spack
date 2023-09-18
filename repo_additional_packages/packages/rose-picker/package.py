from spack.package import *


class RosePicker(Package):
    """
    LFRic RosePicker
    """

    homepage = ""
    url = "file:////home/sergi/workspace/psyclone/run_lfric/opt/rose-picker.v2.tar.gz"


    version(
        "2",
        sha256="asdf1234",
    )

    depends_on("python@3:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
