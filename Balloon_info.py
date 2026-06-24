"""
Tooltip widget - PyQt6 version
"""
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        """Display text in tooltip window."""
        self.text = text
        if self.tipwindow or not self.text:
            return
        
        try:
            if hasattr(self.widget, 'geometry'):
                geom = self.widget.geometry()
                x = geom.x() + 27
                y = geom.y() + geom.height() + 27
            else:
                pos = self.widget.mapToGlobal(self.widget.rect().bottomRight())
                x = pos.x() + 27
                y = pos.y() + 27
        except (AttributeError, TypeError):
            x = y = 0

        self.tipwindow = tw = QWidget()
        tw.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        tw.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        tw.setGeometry(x, y, 200, 50)
        
        label = QLabel(self.text, tw)
        label.setFont(QFont("tahoma", 8))
        label.setStyleSheet("background-color: #ffffe0; border: 1px solid black; padding: 2px;")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setGeometry(0, 0, 200, 50)
        
        tw.show()

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.deleteLater()

    @staticmethod
    def createToolTip(widget, text):
        toolTip = ToolTip(widget)

        def enter(event):
            toolTip.showtip(text)

        def leave(event):
            toolTip.hidetip()

        widget.enterEvent = enter
        widget.leaveEvent = leave
