# TODO: * هاردکدها را بعدا مدیریت کنم، همچنین درصورت امکان لیزی لود انجام دهم

import sys
import time

from pathlib import Path
from functools import wraps

from PySide6.QtCore import QEventLoop, QTimer
from PySide6.QtWidgets import QApplication, QWidget

from definitions import DEBUG_MODE
from dialogpopup import DialogPopup


# .........................................................................................


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not DEBUG_MODE:
            return func(*args, **kwargs)

        start_time = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time
            print(
                    f"[TIMING] {func.__qualname__}: "
                    f"{elapsed_time:.3f} sec"
                    )

    return wrapper


class Utility:
    APP_DIR = (
        Path(sys.executable).resolve().parent
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent
    )

    def __init__(self):
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._loop = QEventLoop()
        self._timer.timeout.connect(self._loop.quit)

    # .................................................................................

    def delay(self, msec: int) -> None:
        self._timer.start(msec)
        self._loop.exec()

    # .................................................................................

    @staticmethod
    def create_popup_dialog(
            title: str = "",
            body: str = "",
            auto_close_delay: int = 0,
            parent: QWidget | None = None,
            ) -> DialogPopup:
        popup = DialogPopup(title=title, body=body, auto_close_delay=auto_close_delay, parent=parent)
        QApplication.beep()
        return popup

    # .................................................................................

    @staticmethod
    def asset_path(rel: str) -> str:
        return str((Utility.APP_DIR / rel).resolve())

    # .................................................................................
