from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget

from UI.ui_dialogpopup import Ui_DialogPopup


class DialogPopup(QWidget):
    def __init__(
            self, title: str = "", body: str = "",
            auto_close_delay: int = 0, parent=None
            ):
        super().__init__(parent)
        self.ui = Ui_DialogPopup()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        if bool(title.strip()):
            self.ui.lblTitle.setVisible(True)
            self.ui.lblTitle.setText(title)
        else:
            self.ui.lblTitle.setVisible(False)

        if bool(body.strip()):
            self.ui.lblBody.setVisible(True)
            self.ui.lblBody.setText(body)
            # self.ui.lblBody.setWordWrap(True)
        else:
            self.ui.lblBody.setVisible(False)

        self.adjustSize()

        if parent:
            parent_geometry = parent.geometry()
            self.move(
                    parent_geometry.x() + (parent_geometry.width() - self.width()) // 2,
                    parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
                    )

        if auto_close_delay > 0:
            QTimer.singleShot(auto_close_delay, self.close)

        self.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress:
            key_event = event  # type: QKeyEvent
            if key_event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape):
                self.close()
                return True
        return super().eventFilter(watched, event)
