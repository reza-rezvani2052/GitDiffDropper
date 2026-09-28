from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


# ----------------------------------------------------------------------------------------

# region REGION_UI_AND_QRC_BUILD
def convert_qrc_and_ui_files_to_python():
    from build_ui_qrc import (
        convert_qrc_file_to_python,
        convert_ui_files_to_python,
        )

    convert_qrc_file_to_python()
    convert_ui_files_to_python()


# پای اینستالر هنگام اجرای فایل اجرایی، معمولا ویژگی sys.frozen را True میکند
# این روش استاندارد و قابل اتکا برای تشخیص حالت اجرای فریزشده است
# هنگام اجرای مستقیم تابع build_ui_and_convert_qrc_to_py اجرا میشود
# هنگام اجرای فایل اجرایی ساخته شده توسط پای اینستالر، این تابع اجرا نمیشود
if not getattr(sys, 'frozen', False):
    convert_qrc_and_ui_files_to_python()

# خط زیر باید بعد از ساخت فایلهای ریسورس باشد
import rc_rc  # ریسورس ها و تصویر اسپلش اسکرین
from utility import Utility  # این باید بعد از ساخت ریسورس ها باشد

from mainwindow import MainWindow
from definitions import AppInfo, CompanyInfo


# endregion

# ----------------------------------------------------------------------------------------

def main() -> int:
    app = QApplication(sys.argv)

    app.setLayoutDirection(Qt.RightToLeft)
    app.setApplicationName(AppInfo.ApplicationName_EN)
    app.setOrganizationName(CompanyInfo.OrganizationName)
    app.setOrganizationDomain(CompanyInfo.OrganizationDomain)

    # ...

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
