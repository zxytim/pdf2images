"""
Detect if system packages are installed and give
friendly installation instruction if not.
"""

import platform
import distro
import subprocess
from loguru import logger
import os
import json

from plumbum import RETCODE


def assert_system_supported():
    p = platform.system()
    if p not in {"Linux", "Darwin"}:
        raise OSError("This package only works on Linux and macOS: `{}`".format(p))


def check_system_package_exists_archlinux(package: str):
    from plumbum.cmd import pacman

    retcode = pacman["-Q", package] & RETCODE
    return retcode == 0


def check_system_package_exists_debian(package: str):
    from plumbum.cmd import dpkg

    retcode = dpkg["-s", package] & RETCODE
    return retcode == 0


def check_system_package_exists_darwin(package: str):
    from plumbum.cmd import brew

    retcode = brew["list", package] & RETCODE
    return retcode == 0


def get_configurations():
    arch_packages = ["qpdf", "xpdf", "perl-image-exiftool"]
    arch_conf = {
        "packages": arch_packages,
        "check_system_package_exists": check_system_package_exists_archlinux,
        "install_instruction": "sudo pacman -Sy && sudo pacman -S --noconfirm {}".format(
            " ".join(arch_packages)
        ),
    }

    debian_packages = ["qpdf", "xpdf", "libimage-exiftool-perl"]
    debian_conf = {
        "packages": debian_packages,
        "check_system_package_exists": check_system_package_exists_debian,
        "install_instruction": "sudo apt update && sudo apt install -y {}".format(
            " ".join(debian_packages)
        ),
    }

    # a.k.a, macOS
    darwin_packages = [
        "freetype",
        "imagemagick",
        "qpdf",
        "xpdf",
        "exiftool",
        "libmagic",
        "ghostscript",
    ]
    darwin_conf = {
        "packages": darwin_packages,
        "check_system_package_exists": check_system_package_exists_darwin,
        "install_instruction": "brew install {}".format(" ".join(darwin_packages)),
    }

    return {
        "arch": arch_conf,
        "debian": debian_conf,
        "ubuntu": debian_conf,
        "darwin": darwin_conf,
    }


CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "pdf2images")
CACHE_PATH = os.path.join(CACHE_DIR, "package_check.json")


def check_system_packages_exist_from_cache(dist: str):
    try:
        if not os.path.exists(CACHE_PATH):
            return False

        with open(CACHE_PATH) as f:
            cache = json.load(f)

        if cache.get(dist, {}).get("ok", False):
            return True
        return False
    except Exception:
        import traceback

        traceback.print_exc()
        logger.info("Check system packages exist from cache failed.")
        return False


def store_system_package_exists_cache(dist: str):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)

    with open(CACHE_PATH, "w") as f:
        json.dump({dist: {"ok": True}}, f)


def check_system_packages():
    assert_system_supported()

    dist = distro.linux_distribution(full_distribution_name=False)[0]
    logger.info("check 1")
    if check_system_packages_exist_from_cache(dist):
        return True
    logger.info("check 2")

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

    store_system_package_exists_cache(dist)
