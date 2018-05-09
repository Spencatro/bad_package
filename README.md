# Bad Package

Bad Package is a set of tools to help identify pypi indexes and python environments that are using bad packages.

This work inspired by [ssh-decorate-gate 2k18](https://securityaffairs.co/wordpress/72298/malware/ssh-decorator-backdoor.html)

## Usage:

```bash
$ pip install bad_package
test_env -e path/to/virtualenv -p requests  # look for any modules that end up installing requests
test_env -e path/to/virtualenv -p requests -v 2.18.4  # look for any modules that end up installing requests==2.18.4
test_env -e path/to/virtualenv -p ssh-decorate -v0 0.27 -v1 0.31  # look for any modules that install ssh-decorate between 0.27 and 0.31
```