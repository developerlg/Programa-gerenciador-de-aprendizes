from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Panel(QFrame):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("sectionTitle")
            self.layout.addWidget(title_label)


class StatCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setMinimumHeight(104)

        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        icon_box = QLabel(" ")
        icon_box.setFixedSize(52, 52)
        icon_box.setStyleSheet(
            f"background: {color}; border-radius: 10px; color: white; font-weight: 800;"
        )
        root.addWidget(icon_box)

        texts = QVBoxLayout()
        texts.setSpacing(2)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 30px; font-weight: 800;")
        title_label = QLabel(title)
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"color: {color}; font-weight: 700;")

        texts.addWidget(value_label)
        texts.addWidget(title_label)
        texts.addWidget(subtitle_label)
        root.addLayout(texts)
        root.addStretch()


class StatusBadge(QLabel):
    COLORS = {
        "Ativo": ("#DCFCE7", "#15803D", "#BBF7D0"),
        "Inativo": ("#E5E7EB", "#4B5563", "#D1D5DB"),
        "Em andamento": ("#EAF3FF", "#0057C2", "#8BBDF8"),
        "Concluido": ("#DCFCE7", "#15803D", "#86EFAC"),
        "Concluida": ("#DCFCE7", "#15803D", "#86EFAC"),
        "Concluída": ("#DCFCE7", "#15803D", "#86EFAC"),
        "Atrasado": ("#FEE2E2", "#DC2626", "#FCA5A5"),
        "Atrasada": ("#FEE2E2", "#DC2626", "#FCA5A5"),
        "Pausado": ("#FFEDD5", "#C2410C", "#FDBA74"),
        "Pausada": ("#FFEDD5", "#C2410C", "#FDBA74"),
    }

    def __init__(self, status: str, parent=None):
        super().__init__(status, parent)
        bg, fg, border = self.COLORS.get(status, ("#E5E7EB", "#374151", "#D1D5DB"))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            f"""
            QLabel {{
                background: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 3px 10px;
                font-weight: 700;
            }}
            """
        )


class PlaceholderView(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("pageBackground")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")

        panel = Panel()
        panel.layout.addStretch()
        message = QLabel("Tela em desenvolvimento")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("font-size: 22px; font-weight: 700; color: #667085;")
        panel.layout.addWidget(message)
        panel.layout.addStretch()

        layout.addWidget(title_label)
        layout.addWidget(panel, 1)


class DonutChartWidget(QWidget):
    def __init__(self, items: list[tuple[str, int, str]], parent=None):
        super().__init__(parent)
        self.items = items
        self.setMinimumSize(220, 190)

    def paintEvent(self, event):
        super().paintEvent(event)
        total = sum(item[1] for item in self.items)
        divisor = total if total > 0 else 1
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height()) - 52
        rect = QRectF(
            (self.width() - size) / 2,
            (self.height() - size) / 2,
            size,
            size,
        )

        start_angle = 90 * 16
        if total == 0:
            pen = QPen(QColor("#D7DEE8"), 26)
            pen.setCapStyle(Qt.PenCapStyle.FlatCap)
            painter.setPen(pen)
            painter.drawArc(rect, 0, 360 * 16)
        else:
            for _, value, color in self.items:
                span_angle = int(-(value / divisor) * 360 * 16)
                pen = QPen(QColor(color), 26)
                pen.setCapStyle(Qt.PenCapStyle.FlatCap)
                painter.setPen(pen)
                painter.drawArc(rect, start_angle, span_angle)
                start_angle += span_angle

        painter.setPen(QColor("#0F172A"))
        font = QFont("Segoe UI", 19, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(total))

        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor("#475467"))
        painter.drawText(
            rect.adjusted(0, 32, 0, 32),
            Qt.AlignmentFlag.AlignCenter,
            "Total",
        )


class BarChartWidget(QWidget):
    def __init__(self, items: list[tuple[str, int, str]], parent=None):
        super().__init__(parent)
        self.items = items
        self.setMinimumHeight(210)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        left = 158
        right = 22
        top = 18
        row_height = 33
        max_value = max((item[1] for item in self.items), default=1)
        chart_width = max(1, self.width() - left - right)

        painter.setPen(QColor("#E1E8F0"))
        for i in range(6):
            x = left + int(chart_width * i / 5)
            painter.drawLine(x, top, x, top + row_height * len(self.items))

        for index, (label, value, color) in enumerate(self.items):
            y = top + index * row_height
            painter.setPen(QColor("#0F172A"))
            painter.drawText(0, y + 22, left - 10, 20, Qt.AlignmentFlag.AlignRight, label)

            width = int(chart_width * value / max_value)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(color))
            painter.drawRoundedRect(left, y + 6, width, 18, 3, 3)

            painter.setPen(QColor("#0F172A"))
            painter.drawText(left + width + 8, y + 21, str(value))
