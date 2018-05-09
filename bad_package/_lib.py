import os
import requests
import shutil
import subprocess
from distutils.version import LooseVersion
from bs4 import BeautifulSoup


def _which_python():
    return subprocess.check_output("which python", shell=True)


def _remove_env(env_name):
    if os.path.exists(env_name):
        shutil.rmtree(env_name)


def _make_env(env_name, ok_to_delete=True):
    if os.path.exists(env_name) and ok_to_delete:
        _remove_env(env_name)
    return subprocess.check_output("python -m virtualenv {}".format(env_name), shell=True)


def _activate(env_name):
    activate_script = os.path.join(env_name, "bin", "activate_this.py")
    execfile(activate_script, dict(__file__=activate_script))


def make_and_activate(env_name, ok_to_delete=True):
    _make_env(env_name, ok_to_delete)
    _activate(env_name)


def install_package_from(package, index):
    cmd = "python -m pip install {} --index-url={} --extra-index-url=https://pypi.python.org/simple".format(package, index)
    try:
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return False



def list_env_modules(env_to_activate=None):
    """ given an env (or the current one activated), return a list of (package, version) tups installed via pip

    :param env_to_activate: str: name of env to activate
    :return: list[... list[package, version]]
    """
    if env_to_activate:
        _activate(env_to_activate)
    output = [i for i in subprocess.check_output("python -m pip freeze", shell=True).split("\n") if i]
    package_version_tups = []
    for line in output:
        v_tup = line.split("==")
        package_version_tups.append((v_tup[0], LooseVersion(v_tup[1])))
    return package_version_tups


def env_contains(env_name, package, exact_version=None, min_version=None, max_version=None):
    """ test if an env contains a package at a specific version, or between two versions

    :param env_name: str: name of env to activate & search
    :param package: str: name of package searching for
    :param min_version: str or LooseVersion: the min version to match. if no max_version, then the exact version.
    :param max_version: str or LooseVersion: the max version to match.
    :return: False if env does not contain package, (package, version) if it does
    """
    if isinstance(exact_version, basestring):
        exact_version = LooseVersion(exact_version)
    if isinstance(min_version, basestring):
        min_version = LooseVersion(min_version)
    if isinstance(max_version, basestring):
        max_version = LooseVersion(max_version)
    modules = list_env_modules(env_name)
    if exact_version:
        return (package, exact_version) if (package, exact_version) in modules else False
    elif min_version or max_version:
        for module_package in modules:
            if module_package[0] == package and \
                   (not min_version or min_version <= module_package[1]) and \
                   (not max_version or module_package[1] <= max_version):
                return module_package
        return False
    else:
        return package if package in [module[0] for module in modules] else False


def list_modules(pypi_simple_url):
    index_contents = requests.get(pypi_simple_url)
    soup = BeautifulSoup(index_contents.text, 'html.parser')
    module_names = [a.text for a in soup.find_all("a")]
    return module_names
