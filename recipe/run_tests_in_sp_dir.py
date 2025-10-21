"""
upstream expectes the folders /tests & /test_fixtures to be relative
to the finished package, even though those folders are not packaged;
effectively, the upstream test suite can currently only be run in (their)
development mode, so patch it that we can properly test the package here.
"""

import subprocess
import sys
import site
from pathlib import Path
import shutil

SRC_DIR = Path(__file__).parent
SP_DIR = Path(site.getsitepackages()[0])
PATHS = ["tests", "test_fixtures"]


def main() -> int:
    for path in PATHS:
        shutil.copytree(SRC_DIR / path, SP_DIR / path)
    args = [sys.executable, "-m", "pytest", *sys.argv[1:]]
    print(">>>", *args)
    rc = subprocess.call(args, cwd=f"{SP_DIR / 'tests'}")
    for path in PATHS:
        shutil.rmtree(SP_DIR / path)
    return rc


if __name__ == "__main__":
    sys.exit(main())
