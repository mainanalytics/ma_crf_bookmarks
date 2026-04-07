from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


def scale_icon(parent_widget: QWidget) -> QPainter:
    if parent_widget.pixmap.isNull():
        return

    painter = QPainter(parent_widget)

    # Scale relative to window width
    target_width = int(parent_widget.width() * parent_widget.scale_ratio)

    scaled = parent_widget.pixmap.scaledToWidth(target_width, Qt.SmoothTransformation)

    # Keep inside window if too tall
    if scaled.height() > parent_widget.height() - parent_widget.margin * 2:
        scaled = parent_widget.pixmap.scaledToHeight(
            parent_widget.height() - parent_widget.margin * 2, Qt.SmoothTransformation
        )

    # Bottom-right position
    x = parent_widget.width() - scaled.width() - parent_widget.margin
    y = parent_widget.height() - scaled.height() - parent_widget.margin - 20

    painter.drawPixmap(x, y, scaled)
