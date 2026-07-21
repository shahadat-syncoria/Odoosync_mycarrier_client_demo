import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import os
import sys

base_path = os.path.dirname(__file__)
py_version = f"{sys.version_info.major}_{sys.version_info.minor}"
strip_python = py_version.replace('_', '')

package_imports = [
]
pyc_files = [
    'delivery',
    'omni_account_delivery',
]

class _VersionedPycFinder(importlib.abc.MetaPathFinder):
    def __init__(self, package_name, package_path):
        self.package_name = package_name
        self.package_path = package_path

    def find_spec(self, fullname, path=None, target=None):
        prefix = f"{self.package_name}."
        if not fullname.startswith(prefix):
            return None
        child_name = fullname[len(prefix):]
        if "." in child_name:
            return None
        if os.path.isdir(os.path.join(self.package_path, child_name)):
            return None
        file_path = os.path.join(
            self.package_path,
            '__pycache__',
            f"{child_name}.cpython-{strip_python}.pyc",
        )
        if not os.path.exists(file_path):
            return None
        loader = importlib.machinery.SourcelessFileLoader(fullname, file_path)
        return importlib.util.spec_from_file_location(fullname, file_path, loader=loader)

def _install_versioned_pyc_finder():
    for finder in sys.meta_path:
        if (
            getattr(finder, 'package_name', None) == __name__
            and getattr(finder, 'package_path', None) == base_path
        ):
            return
    sys.meta_path.insert(0, _VersionedPycFinder(__name__, base_path))

_install_versioned_pyc_finder()

for package_name in package_imports:
    importlib.import_module(f"{__name__}.{package_name}")

for file_name in pyc_files:
    importlib.import_module(f"{__name__}.{file_name}")
