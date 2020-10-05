
import os
import sys
import shutil


url_prefix = "https://github.com/MoonShineVFX/avalon-core/archive"


def build(source_path, build_path, install_path, targets=None):
    from rezutil import lib

    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)

    filename = "%s.zip" % os.environ["REZ_BUILD_PROJECT_VERSION"]

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    # Deploy
    # (we cannot use setup.py to install avalon, there are additional files
    # currently not being installed by it)
    lib.copy_dir(source_root, dst)

    # Additional
    dst_root = os.path.dirname(dst)
    for dir_name in ["apps", "bin", "config", "template"]:
        dst_dir = os.path.join(dst_root, dir_name)
        lib.copy_dir(os.path.join(source_path, dir_name), dst_dir)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
