"""
Build executable using PyInstaller.
"""

import sys
import time
import shutil
import subprocess

from pathlib import Path

BUILD_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD_SCRIPT_DIR.parent))

from build_ui_qrc import convert_qrc_file_to_python, convert_ui_files_to_python
from definitions import APP_DIRECTORY, AppInfo

# ...

APP_NAME = AppInfo.ApplicationName_EN
APP_VERSION = AppInfo.ApplicationVersion

DIR_ROOT = APP_DIRECTORY

ICON = DIR_ROOT / "RC" / "app-icon.ico"

ENTRY_POINT_MAIN = DIR_ROOT / "main.py"

# PYINSTALLER_MODE = "--onefile"
PYINSTALLER_MODE = "--onedir"

DIR_BUILD = DIR_ROOT / "build"
DIR_DIST = DIR_ROOT / "dist"
SPEC_FILE = DIR_ROOT / f"{APP_NAME}.spec"


def remove(path: Path) -> None:
    if not path.exists():
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def clean() -> None:
    print("Cleaning previous build...")
    # ...
    remove(DIR_BUILD)
    remove(DIR_DIST)
    remove(SPEC_FILE)


def get_version(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def show_versions() -> None:
    print(f"App Version : {APP_VERSION}")
    print(f"Python      : {sys.version.split()[0]}")
    print(
            "PyInstaller : "
            f"{get_version([sys.executable, '-m', 'PyInstaller', '--version'])}"
            )


def build() -> None:
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        PYINSTALLER_MODE,
        "--clean",
        "--noconfirm",
        "--windowed",
        # "--collect-all",
        f"--icon={ICON}",
        f"--name={APP_NAME}",
        # ...
        f"--workpath={DIR_BUILD}",
        f"--distpath={DIR_DIST}",
        f"--specpath={DIR_ROOT}",
        # ...
        ENTRY_POINT_MAIN,
        ]

    subprocess.run(command, check=True)


def validate_executables() -> None:
    app_dist_dir = DIR_DIST / APP_NAME

    required_executables = (
        app_dist_dir / f"{APP_NAME}.exe",
        )

    for executable in required_executables:
        if not executable.is_file():
            raise FileNotFoundError(
                    f"Expected executable not found: {executable}"
                    )

    print(f"Validated executable: {required_executables[0]}")
    # print(f"Validated executable: {required_executables[1]}")


def copy_runtime_files() -> None:
    pass

    # app_dist_dir = DIR_DIST / APP_NAME

    # shutil.copy2(DATABASE_FILE, app_dist_dir / DATABASE_FILE.name)
    # print(f"{DATABASE_FILE.name} file copied")


def format_elapsed_time(seconds: float) -> str:
    seconds = int(seconds)

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []

    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")

    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

    if seconds or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if len(parts) == 1:
        return parts[0]

    return ", ".join(parts[:-1]) + " and " + parts[-1]


def check_prerequisites() -> None:
    required_files = (
        ICON,
        ENTRY_POINT_MAIN,
        )

    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(f"Required file not found: {path}")


def main():
    start = time.perf_counter()

    try:
        check_prerequisites()
        show_versions()
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # ...

    try:
        print()
        clean()
        print()
        # ...
        print("Checking qrc & ui files...\n")

        # اطمینان از ساخته شدن فایلهای ریسورس و تبدیل کدهای .ui به پایتون
        convert_qrc_file_to_python()
        convert_ui_files_to_python()
        # ...
        print("\nStarting application bundle build...\n")

        build()

        validate_executables()

        copy_runtime_files()

        elapsed = time.perf_counter() - start

        print(f"\nDone in {format_elapsed_time(elapsed)}.")

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"File operation failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBuild cancelled by user.")
        sys.exit(2)


if __name__ == "__main__":
    main()
