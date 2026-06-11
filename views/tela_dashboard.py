from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from controllers.dashboard_controller import DashboardController
from views.widgets import BarChartWidget, DonutChartWidget, Panel, StatCard, StatusBadge


class DashboardView(QWidget):
    def __init__(self, controller: DashboardController | None = None, parent=None):
        super().__init__(parent)
        self.controller = controller or DashboardController()
        self.dados = self.controller.obter_resumo()
        self._build_ui()

    def _build_ui(self):
        self.setObjectName("pageBackground")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root.addWidget(scroll)

        page = QWidget()
        page.setObjectName("pageBackground")
        page_layout = QHBoxLayout(page)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(18)
        scroll.setWidget(page)

        main_column = QVBoxLayout()
        main_column.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Resumo geral das atividades")
        subtitle.setObjectName("mutedText")
        main_column.addWidget(title)
        main_column.addWidget(subtitle)

        cards = QGridLayout()
        cards.setHorizontalSpacing(14)
        cards.setVerticalSpacing(14)
        for index, card in enumerate(self.dados["cards"]):
            cards.addWidget(
                StatCard(
                    card["title"],
                    card["value"],
                    card["subtitle"],
                    card["color"],
                ),
                0,
                index,
            )
        main_column.addLayout(cards)

        main_column.addWidget(self._recent_activities_panel())

        chart_row = QHBoxLayout()
        chart_row.setSpacing(18)
        chart_row.addWidget(self._status_chart_panel(), 1)
        chart_row.addWidget(self._service_chart_panel(), 1)
        main_column.addLayout(chart_row)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(18)
        sidebar.addWidget(self._pending_panel())
        sidebar.addWidget(self._deadlines_panel())
        sidebar.addWidget(self._quick_actions_panel())
        sidebar.addStretch()

        sidebar_box = QWidget()
        sidebar_box.setFixedWidth(300)
        sidebar_box.setLayout(sidebar)

        page_layout.addLayout(main_column, 1)
        page_layout.addWidget(sidebar_box)

    def _recent_activities_panel(self) -> Panel:
        panel = Panel("Ultimas atividades registradas")
        activities = self.dados["recent_activities"]
        table = QTableWidget(len(activities), 6)
        table.setHorizontalHeaderLabels(
            ["Data", "Aprendiz", "Atividade", "Tipo de servico", "Situacao", "Prazo"]
        )
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(False)
        table.setMinimumHeight(260)

        for row_index, row_data in enumerate(activities):
            for column, value in enumerate(row_data):
                if column == 4:
                    table.setCellWidget(row_index, column, StatusBadge(value))
                else:
                    item = QTableWidgetItem(value)
                    if column in (0, 5):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row_index, column, item)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        panel.layout.addWidget(table)
        if not activities:
            empty = QLabel("Nenhuma atividade registrada ainda.")
            empty.setObjectName("mutedText")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            panel.layout.addWidget(empty)
        return panel

    def _status_chart_panel(self) -> Panel:
        panel = Panel("Atividades por situacao")
        row = QHBoxLayout()
        row.setSpacing(18)
        chart_data = self.dados["status_chart"]
        total = sum(item[1] for item in chart_data)
        row.addWidget(DonutChartWidget(chart_data))

        legend = QVBoxLayout()
        legend.setSpacing(8)
        for label, value, color in chart_data:
            legend.addWidget(self._legend_item(label, value, color))
        if total == 0:
            empty = QLabel("Aguardando registros reais.")
            empty.setObjectName("mutedText")
            legend.addWidget(empty)
        legend.addStretch()
        row.addLayout(legend)
        panel.layout.addLayout(row)
        return panel

    def _service_chart_panel(self) -> Panel:
        panel = Panel("Atividades por tipo de servico")
        panel.layout.addWidget(BarChartWidget(self.dados["service_chart"]))
        return panel

    def _pending_panel(self) -> Panel:
        panel = Panel("Pendencias")
        for label, value, color in self.dados["pending"]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            row.addStretch()
            number = QLabel(value)
            number.setStyleSheet(f"color: {color}; font-weight: 800; font-size: 16px;")
            row.addWidget(number)
            panel.layout.addLayout(row)
        return panel

    def _deadlines_panel(self) -> Panel:
        panel = Panel("Proximos prazos")
        deadlines = self.dados["deadlines"]
        for name, activity, deadline, urgent in deadlines:
            item = QFrame()
            item.setStyleSheet("border-bottom: 1px solid #E6ECF4;")
            layout = QVBoxLayout(item)
            layout.setContentsMargins(0, 0, 0, 10)
            layout.setSpacing(2)

            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: 800;")
            activity_label = QLabel(activity)
            deadline_label = QLabel(deadline)
            deadline_label.setStyleSheet(
                "font-weight: 700; color: #DC2626;" if urgent else "font-weight: 700;"
            )

            layout.addWidget(name_label)
            layout.addWidget(activity_label)
            layout.addWidget(deadline_label)
            panel.layout.addWidget(item)

        if not deadlines:
            empty = QLabel("Nenhum prazo registrado ainda.")
            empty.setObjectName("mutedText")
            empty.setWordWrap(True)
            panel.layout.addWidget(empty)
        return panel

    def _quick_actions_panel(self) -> Panel:
        panel = Panel("Acoes rapidas")
        actions = [
            "Cadastrar novo aprendiz",
            "Registrar nova atividade",
            "Gerar relatorio mensal",
            "Fazer backup dos dados",
        ]
        for label in actions:
            button = QPushButton(label)
            button.setObjectName("secondaryButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            panel.layout.addWidget(button)
        return panel

    def _legend_item(self, label: str, value: int, color: str) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        square = QLabel()
        square.setFixedSize(10, 10)
        square.setStyleSheet(f"background: {color}; border-radius: 2px;")

        label_widget = QLabel(label)
        value_widget = QLabel(str(value))
        value_widget.setStyleSheet("font-weight: 700;")

        layout.addWidget(square)
        layout.addWidget(label_widget)
        layout.addStretch()
        layout.addWidget(value_widget)
        return widget
