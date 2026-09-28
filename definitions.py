import sys

from dataclasses import dataclass
from pathlib import Path

# ...

# تشخیص حالت اجرای برنامه
IS_FROZEN = getattr(sys, "frozen", False)  # PyInstaller
DEBUG_MODE = not IS_FROZEN
# print(f"{DEBUG_MODE=}")


# Keep application data beside the script/executable. The current working
# directory may be different when a Windows shortcut launches the program.
APP_DIRECTORY = (
    Path(sys.executable).resolve().parent
    if IS_FROZEN else Path(__file__).resolve().parent
)


# ----------------------------------------------------------------------------------------


@dataclass(frozen=True)
class CompanyInformation:
    OrganizationName: str = "RezvanSoft"
    OrganizationDomain: str = "https://codexlab.ir/"


@dataclass(frozen=True)
class AppInformation:
    ApplicationName_EN: str = "GitDiffDropper"
    ApplicationName_FA: str = "دیف ساز"
    ApplicationVersion: str = "1.0.0"
    SupportMail: str = "reza.rezvani2052@gmail.com"


# Shared application metadata and runtime state.
CompanyInfo = CompanyInformation()
AppInfo = AppInformation()
