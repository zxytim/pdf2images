"""
Detect if system packages are installed and give
friendly installation instruction if not.
"""

import platform
import distro
import subprocess
from loguru import logger

from plumbum import RETCODE


def assert_is_linux():
    if platform.system() != "Linux":
        raise OSError("This package only works on linux")


def check_system_package_exists_archlinux(package: str):
    from plumbum.cmd import pacman

    retcode = pacman["-Q", package] & RETCODE
    return retcode == 0


def check_system_package_exists_debian(package: str):
    from plumbum.cmd import dpkg

    retcode = dpkg["-s", package] & RETCODE
    return retcode == 0


def get_configurations():
    arch_conf = {
        "packages": ["qpdf", "xpdf", "perl-image-exiftool"],
        "check_system_package_exists": check_system_package_exists_archlinux,
        "install_instruction": "sudo pacman -Sy && sudo pacman -S --noconfirm qpdf xpdf perl-image-exiftool",
    }

    debian_conf = {
        "packages": ["qpdf", "xpdf", "libimage-exiftool-perl"],
        "check_system_package_exists": check_system_package_exists_debian,
        "install_instruction": "sudo apt update && sudo apt install -y qpdf xpdf libimage-exiftool-perl",
    }

    return {"arch": arch_conf, "debian": debian_conf, "ubuntu": debian_conf}


def check_system_packages():
    assert_is_linux()

    dist = distro.linux_distribution(full_distribution_name=False)[0]

    confs = get_configurations()
    if dist not in confs:
        logger.info(
            "Unknown linux distribution `{}`. Skip system package check".format(dist)
        )
        return

    conf = confs[dist]

    for pack in conf["packages"]:
        if not conf["check_system_package_exists"](pack):
            raise RuntimeError(
                "System package `{}` not installed. Please install using the following instruction to ensure all system depencies are installed: \n"
                "    {}".format(pack, conf["install_instruction"])
            )
