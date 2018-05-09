import click
import sys

from _lib import env_contains, list_modules, make_and_activate, install_package_from, _remove_env, _activate, _which_python


@click.command()
@click.option('--index_url', '-i', required=True)
@click.option('--package', '-p', required=True)
@click.option('--env_prefix', '-e', default="bad_package_testenv")
@click.option('--tmp_workdir', '-t', default=".")
@click.option('--keep_virtualenvs', default=False)
@click.option('--exact_version', '-v')
@click.option('--min_version', '-v0')
@click.option('--max_version', '-v1')
@click.pass_context
def test_index(ctx, index_url, package, env_prefix, tmp_workdir, keep_virtualenvs, exact_version, min_version, max_version):
    errcount = 0
    modules_on_index = list_modules(index_url)
    print("Need to test {} modules on {}...".format(len(modules_on_index), index_url))
    for module in modules_on_index:
        env_name = "{}/{}_{}".format(tmp_workdir, env_prefix, "".join([c for c in module if c.isalpha() or c.isdigit() or c=='_']).rstrip())
        make_and_activate(env_name)
        if not install_package_from(module, index_url):
            sys.stderr.write("WARNING: could not install `{}` from `{}`\n".format(module, index_url))
        errcount += ctx.invoke(test_env, env_path=env_name, package=package, exact_version=exact_version,
                               min_version=min_version, max_version=max_version, exit_on_failure=False,
                               env_name_override="{}{}".format(index_url, module))
        if not keep_virtualenvs:
            _remove_env(env_name)
    if errcount:
        sys.stderr.write("FAILURE: {} modules in this index failed!\n".format(errcount))
        sys.exit(1)


@click.command()
@click.option('--env_path', '-e', required=True)
@click.option('--package', '-p', required=True)
@click.option('--exact_version', '-v')
@click.option('--min_version', '-v0')
@click.option('--max_version', '-v1')
def test_env(env_path, package, exact_version, min_version, max_version, exit_on_failure=True, env_name_override=None):
    env_contains_package = env_contains(env_path, package, exact_version, min_version, max_version)
    if env_contains_package:
        errstr = "FAILURE: env `{}` contains package `{}`".format(env_path, package)
        if exact_version:
            errstr += " ({}=={})".format(*env_contains_package)
        elif min_version or max_version:
            version_parts = []
            if min_version:
                version_parts.append("min version {}".format(min_version))
            if max_version:
                version_parts.append("max version {}".format(max_version))
            version_str = " with {} ({}=={})".format(" and ".join(version_parts), *env_contains_package)
            errstr += version_str
        sys.stderr.write(errstr + "\n")
        if exit_on_failure:
            sys.exit(1)
        else:
            return 1
    else:
        safe_str = "Safe! {} does not contain {}".format(env_name_override or env_path, package)
        if exact_version:
            safe_str += " version {}".format(exact_version)
        elif min_version or max_version:
            version_parts = []
            if min_version:
                version_parts.append("min version {}".format(min_version))
            if max_version:
                version_parts.append("max version {}".format(max_version))
            version_str = " with {}".format("and".join(version_parts))
            safe_str += version_str
        print(safe_str)
        return 0
