import os
from spack.package import *


class RosePicker(Package):
    """
    LFRic RosePicker
    """

    homepage = ""
    url = "https://github.com/sergisiso/psyclone-spack/raw/master/repo_additional_packages/packages/rose-picker/rose-picker.v2.tar.gz"

    version(
        '2',
        '8459bac55ca97fca874b89f7199fdc8e551d0661402b629d7acd668b594c01b1',
        url='https://github.com/sergisiso/psyclone-spack/raw/master/repo_additional_packages/packages/rose-picker/rose-picker.v2.tar.gz'
    )

    # depends_on("python@3:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", os.path.join(self.spec.prefix, "lib", "python"))
