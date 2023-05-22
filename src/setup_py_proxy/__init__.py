"""Inspired by hatch's setup.py migration hack."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def setup(**kwargs) -> None:
    print(json.dumps(kwargs), file=sys.stderr)


def run() -> None:
    cwd = Path.cwd()
    with TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp) / "tmp"
        shutil.copytree(
            cwd,
            tmp_dir,
            ignore=shutil.ignore_patterns(".git", ".tox", ".venv"),
            copy_function=shutil.copy,
        )
        shutil.copy(Path(__file__), Path(tmp_dir) / "setuptools.py")
        os.chdir(tmp_dir)
        env = dict(os.environ)
        env["PYTHONPATH"] = str(tmp_dir)
        subprocess.check_call(
            [sys.executable, str(tmp_dir / "setup.py")], env=env
        )
        os.chdir(cwd)


if __name__ == "setuptools":
    _setup_proxy_module = sys.modules.pop("setuptools")
    _setup_proxy_cwd = sys.path.pop(0)

    import setuptools as __setuptools

    sys.path.insert(0, _setup_proxy_cwd)
    sys.modules["setuptools"] = _setup_proxy_module

    def __getattr__(name):
        return getattr(__setuptools, name)

    del _setup_proxy_module
    del _setup_proxy_cwd
