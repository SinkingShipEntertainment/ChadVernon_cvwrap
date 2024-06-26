name = "cvwrap"

authors = [
    "Chad Vernon"
]

# This repo has submodules. If you are cloning it for the first time, remember to run:
# git submodule init
# git submodule update

# NOTE: version = <cvwrap_version>.sse.<sse_version>
version = "1.0.0.sse.1.1.1"

description = \
    """
    A Maya wrap deformer that is faster than Maya's wrap deformer,
    can be rebounded, has a GPU implementation, and supports inverted
    front of chain blend shapes.
    """

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

requires = [
]

private_build_requires = [
]

variants = [
    ["maya-2024", "python-3.9", "maya_devkit-2024"],
    ["maya-2024", "python-3.10", "maya_devkit-2024"],
]

uuid = "repository.ChadVernon_cvwrap"

def pre_build_commands():

    info = {}
    with open("/etc/os-release", 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line_info = line.replace('\n', '').split('=')
            if len(line_info) != 2:
                continue
            info[line_info[0]] = line_info[1].replace('"', '')
    linux_distro = info.get("NAME", "centos")
    print("Using Linux distro: " + linux_distro)

    if linux_distro.lower().startswith("centos"):
        command("source /opt/rh/devtoolset-6/enable")
    elif linux_distro.lower().startswith("rocky"):
        pass

def commands():
    # NOTE: REZ package versions can have ".sse." to separate the external
    # version from the internal modification version.
    split_versions = str(version).split(".sse.")
    external_version = split_versions[0]
    internal_version = None
    if len(split_versions) == 2:
        internal_version = split_versions[1]

    env.CVWRAP_VERSION = external_version
    env.CVWRAP_PACKAGE_VERSION = external_version
    if internal_version:
        env.CVWRAP_PACKAGE_VERSION = internal_version

    env.CVWRAP_ROOT.append("{root}")
    env.CVWRAP_LOCATION.append("{root}")

    env.LD_LIBRARY_PATH.append("{root}/cvwrap/plug-ins")
    env.PYTHONPATH.append("{root}/cvwrap/scripts")

    # For Maya to locate the .mod file to setup env variables for plugins and libraries
    env.MAYA_MODULE_PATH.append("{root}/cvwrap")