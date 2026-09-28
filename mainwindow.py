from __future__ import annotations

import subprocess
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMainWindow

from UI.ui_mainwindow import Ui_MainWindow

from utility import measure_time, Utility

GIT_PROCESS_FLAGS = (
    subprocess.CREATE_NO_WINDOW
    if hasattr(subprocess, "CREATE_NO_WINDOW")
    else 0
)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setAcceptDrops(True)
        # ...
        self.readSettings()
        self.connect_signals_to_slots()

    def connect_signals_to_slots(self):
        pass
        # self.ui.actQuit.triggered.connect(self.on_actQuit_triggered)
        # self.ui.actAbout.triggered.connect(self.on_actAbout_triggered)

    def readSettings(self):
        settings = QSettings()
        settings.beginGroup("MainWindow")
        geometry = settings.value("Geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        state = settings.value("State")
        if state is not None:
            self.restoreState(state)
        settings.endGroup()

    def writeSettings(self):
        settings = QSettings()
        settings.beginGroup("MainWindow")
        settings.setValue("Geometry", self.saveGeometry())
        settings.setValue("State", self.saveState())
        settings.endGroup()

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def dragEnterEvent(self, event) -> None:  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:  # noqa: N802
        paths = [
            Path(url.toLocalFile())
            for url in event.mimeData().urls()
            if url.isLocalFile()
            ]

        files = [path for path in paths if path.is_file()]

        if not files:
            self.ui.label.setText("فایل معتبری دریافت نشد.")
            event.ignore()
            return

        success_count = 0
        errors: list[str] = []

        for source_path in files:
            try:
                destination_path = self._create_diff_file(source_path)
                success_count += 1
                print(f"Created: {destination_path}")
            except Exception as exc:
                errors.append(f"{source_path.name}: {exc}")
                print(f"Error: {source_path} -> {exc}")

        if errors:
            self.ui.label.setText(
                    f"انجام شد: {success_count} فایل\n"
                    f"خطا: {len(errors)} فایل\n\n"
                    + "\n".join(errors)
                    )
        else:
            self.ui.label.setText(
                    f"با موفقیت انجام شد.\n\n"
                    f"{success_count} فایل در Desktop ساخته شد."
                    )

        event.acceptProposedAction()

    @staticmethod
    def run_git(args: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
                ["git", *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                creationflags=GIT_PROCESS_FLAGS,
                )

    def _create_diff_file(self, source_path: Path) -> Path:
        """خروجی git diff فایل را در Desktop ذخیره می‌کند."""
        repo_root = self._find_git_root(source_path.parent)

        relative_path = source_path.relative_to(repo_root)
        destination_path = (
                Path.home()
                / "Desktop"
                / f"diff-{source_path.name}.txt"
        )

        result = self.run_git(
                [
                    "-C",
                    str(repo_root),
                    "diff",
                    "--",
                    str(relative_path),
                    ]
                )

        if result.returncode != 0:
            stderr = result.stderr.strip() or "git diff failed"
            raise RuntimeError(stderr)

        destination_path.write_text(
                result.stdout,
                encoding="utf-8",
                newline="",
                )

        return destination_path

    @staticmethod
    def _find_git_root(start_path: Path) -> Path:
        """نزدیک‌ترین Git repository را از مسیر فایل پیدا می‌کند."""
        result = MainWindow.run_git(
                [
                    "-C",
                    str(start_path),
                    "rev-parse",
                    "--show-toplevel",
                    ]
                )

        if result.returncode != 0:
            stderr = result.stderr.strip()

            if stderr:
                raise RuntimeError(
                        f"فایل داخل یک Git repository نیست.\n{stderr}"
                        )

            raise RuntimeError(
                    "فایل داخل یک Git repository نیست."
                    )

        return Path(result.stdout.strip()).resolve()
