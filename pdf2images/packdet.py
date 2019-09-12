"""
Detect if system packages are installed and give
friendly installation instruction if not.
"""

import platform
import distro
import subprocess

from plumbum import RETCODE


def assert_is_linux():
    if platform.system() != 'Linux':
        raise OSError('This package only works on linux')


def check_system_package_exists_archlinux(package: str):
    from plumbum.cmd import pacman
    retcode = pacman['-Q', package] & RETCODE
    return retcode == 0


def check_system_package_exists_debian(package: str):
    raise NotImplementedError()


def check_system_packages():
    assert_is_linux()

    dist = distro.linux_distribution(full_distribution_name=False)[0]
    packages = {
        'arch': ['qpdf', 'xpdf', 'perl-image-exiftool'],
        'debian': ['qpdf', 'xpdf', 'libimage-exiftool-perl'],
        'ubuntu': ['qpdf', 'xpdf', 'libimage-exiftool-perl'],
    }[dist]
    
    check_system_package_exists = {
        'arch': check_system_package_exists_archlinux,
        'debian': check_system_package_exists_debian,
        'ubuntu': check_system_package_exists_debian,
    }[dist]

    install_instruction = {
        'arch': 'sudo pacman -S --noconfirm qpdf xpdf perl-image-exiftool',
        'debian': 'sudo apt install -y qpdf xpdf libimage-exiftool-perl',
        'ubuntu': 'sudo apt install -y qpdf xpdf libimage-exiftool-perl',
    }[dist]


    for pack in packages:
        if not check_system_package_exists(pack):
            raise RuntimeError('System package not installed. Please install using the following instruction: \n'
                        '    {}'.format(install_instruction))


