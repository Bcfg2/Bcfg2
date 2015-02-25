"""This provides Bcfg2 support for Blastwave."""

import tempfile
import Bcfg2.Client.Tools.SYSV


class Blast(Bcfg2.Client.Tools.SYSV.SYSV):
    """Support for Blastwave packages."""
    pkgtype = 'blast'
    pkgtool = ("/opt/csw/bin/pkg-get install %s", ("%s", ["bname"]))
    name = 'Blast'
    __execs__ = ['/opt/csw/bin/pkg-get', "/usr/bin/pkginfo"]
    __handles__ = [('Package', 'blast')]
    __req__ = {'Package': ['name', 'version', 'bname']}

    def __init__(self, config):  # pylint: disable=super-init-not-called
        # dont use the sysv constructor
        # pylint: disable=non-parent-init-called
        Bcfg2.Client.Tools.PkgTool.__init__(self, config)
        # pylint: enable=non-parent-init-called
        noaskfile = tempfile.NamedTemporaryFile()
        self.noaskname = noaskfile.name
        try:
            noaskfile.write(Bcfg2.Client.Tools.SYSV.noask)
        except:  # pylint: disable=bare-except
            pass

    # VerifyPackage comes from Bcfg2.Client.Tools.SYSV
    # Install comes from Bcfg2.Client.Tools.PkgTool
    # Extra comes from Bcfg2.Client.Tools.Tool
    # Remove comes from Bcfg2.Client.Tools.SYSV
    def FindExtra(self):
        """Pass through to null FindExtra call."""
        return []
