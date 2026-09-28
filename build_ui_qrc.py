import sys
import subprocess

from pathlib import Path

# پوشه‌ای که Python در حال اجرا در آن قرار دارد
PYTHON_DIR = Path(sys.executable).resolve().parent

UIC = PYTHON_DIR / "pyside6-uic.exe"
RCC = PYTHON_DIR / "pyside6-rcc.exe"

# مسیر پوشه UI نسبت به محل همین فایل
BASE_DIR = Path(__file__).resolve().parent

# ui_dir = "."  # مسیر جاری یا همان روت پروژه
UI_DIR = BASE_DIR / "UI"

QRC_PATH = BASE_DIR / "RC" / "rc.qrc"


def _check_pyside6_tools():
    """بررسی می‌کند که ابزارهای pyside6-uic و pyside6-rcc وجود داشته باشند."""

    missing_tools = []

    if not UIC.is_file():
        missing_tools.append(f"pyside6-uic not found: {UIC}")

    if not RCC.is_file():
        missing_tools.append(f"pyside6-rcc not found: {RCC}")

    if missing_tools:
        message = (
                "Required PySide6 tools were not found:\n"
                + "\n".join(missing_tools)
                + "\n\n"
                  "Make sure PySide6 is installed in the active Python environment."
        )

        raise FileNotFoundError(message)


def convert_ui_files_to_python():
    """تبدیل فایل‌های .ui به فایل‌های ui_*.py."""

    _check_pyside6_tools()

    ui_directories = [
        UI_DIR,
        ]

    for ui_dir in ui_directories:
        if not ui_dir.is_dir():
            print(f"UI directory not found: {ui_dir}")
            continue

        for ui_path in ui_dir.glob("*.ui"):
            out_name = f"ui_{ui_path.stem}.py"
            out_path = ui_dir / out_name

            if (
                    not out_path.exists()
                    or ui_path.stat().st_mtime > out_path.stat().st_mtime
            ):
                print(
                        f"Converting: "
                        f"{ui_path.relative_to(BASE_DIR)} -> "
                        f"{out_path.relative_to(BASE_DIR)}"
                        )

                subprocess.run(
                        [
                            str(UIC),
                            str(ui_path),
                            "-o",
                            str(out_path),
                            ],
                        check=True,
                        )


def convert_qrc_file_to_python():
    _check_pyside6_tools()

    output_path = BASE_DIR / "rc_rc.py"

    if (
            not output_path.exists()
            or QRC_PATH.stat().st_mtime > output_path.stat().st_mtime
    ):
        print(f"Converting: {QRC_PATH.name} -> {output_path.name}")

        subprocess.run(
                [
                    str(RCC),
                    str(QRC_PATH),
                    "-o",
                    str(output_path),
                    ],
                check=True,
                )


if __name__ == "__main__":
    convert_ui_files_to_python()
    convert_qrc_file_to_python()
