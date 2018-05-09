# Bad Package

Bad Package is a set of tools to help identify pypi indexes and python environments that are using bad packages.

This work inspired by [ssh-decorate-gate 2k18](https://securityaffairs.co/wordpress/72298/malware/ssh-decorator-backdoor.html)

## Usage:

```bash
$ python setup.py install

$ test_env -e path/to/virtualenv -p requests  # look for requests
$ test_env -e path/to/virtualenv -p requests -v 2.18.4  # look for requests==2.18.4
$ test_env -e path/to/virtualenv -p ssh-decorate -v0 0.27 -v1 0.31  # look for ssh-decorate between 0.27 and 0.31

$ test_index -i http://my-private-pypi/simple -p requests  # look for any modules that end up installing requests
$ test_index -i http://my-private-pypi/simple -p requests -v 2.18.4  # look for any modules that end up installing requests==2.18.4
$ test_index -i http://my-private-pypi/simple -p ssh-decorate -v0 0.27 -v1 0.31  # look for any modules that install ssh-decorate between 0.27 and 0.31
```

Example output:

```bash
$ test_index -i https://my.private-pypi.com/simple/ -p requests
Need to test 3 modules on https://my.private-pypi.com/simple/...
Safe! https://my.private-pypi.com/simple/safemodule does not contain requests
FAILURE: env `./bad_package_testenv_unsafe_module` contains package `requests`
Command "python setup.py egg_info" failed with error code 1 in /private/var/folders/vd/5nr1jfqd4d19p349161zlgnndmpq06/T/pip-install-sU7GdM/error_package/
WARNING: could not install `error_package` from `https://my.private-pypi.com/simple/`
FAILURE: 1 modules in this index failed!
```
