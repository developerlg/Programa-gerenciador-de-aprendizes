from dataclasses import dataclass

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config import CURRENT_USER_NAME
from data.opcoes import SITUACOES_ATIVIDADE, TIPOS_SERVICO_ATIVIDADE
from views.widgets import Panel, StatusBadge


MAX_OBSERVACAO_CHARS = 300


@dataclass(frozen=True)
class SummaryConfig:
    key: str
    title: str
    color: str
    background: str
    border: str
    icon: QStyle.StandardPixmap


SUMMARY_ITEMS = (
    SummaryConfig(
        "Em andamento",
        "Em andamento",
        "#0B55B7",
        "#EEF6FF",
        "#CFE4FF",
        QStyle.StandardPixmap.SP_BrowserReload,
    ),
    SummaryConfig(
        "Concluída",
        "Concluídas",
        "#16A34A",
        "#EEFDF4",
        "#CBEFD8",
        QStyle.StandardPixmap.SP_DialogApplyButton,
    ),
    SummaryConfig(
        "Pausada",
        "Pausadas",
        "#F97316",
        "#FFF7ED",
        "#FED7AA",
        QStyle.StandardPixmap.SP_MediaPause,
    ),
    SummaryConfig(
        "Atrasada",
        "Atrasadas",
        "#DC2626",
        "#FEF2F2",
        "#FECACA",
        QStyle.StandardPixmap.SP_MessageBoxWarning,
    ),
    SummaryConfig(
        "total",
        "Total de atividades",
        "#0F172A",
        "#FFFFFF",
        "#DCE6F2",
        QStyle.StandardPixmap.SP_FileIcon,
    ),
)


class TelaAtividades(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.atividades: list[dict[str, str]] = []
        self.summary_values: dict[str, QLabel] = {}
        self._build_ui()
        self._carregar_tabela()
        self._atualizar_resumo()

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
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(16)
        scroll.setWidget(page)

        header = QVBoxLayout()
        header.setSpacing(4)
        title = QLabel("Registro de Atividade")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Veja as atividades cadastradas e seu status")
        subtitle.setObjectName("mutedText")
        header.addWidget(title)
        header.addWidget(subtitle)
        page_layout.addLayout(header)

        top_row = QHBoxLayout()
        top_row.setSpacing(16)
        top_row.addWidget(self._form_panel(), 1)
        top_row.addWidget(self._summary_panel())
        page_layout.addLayout(top_row)

        page_layout.addWidget(self._table_panel())
        page_layout.addStretch()

    def _form_panel(self) -> Panel:
        panel = Panel("Nova atividade")
        panel.setMinimumWidth(0)
        panel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)

        self.aprendiz_combo = QComboBox()
        self.aprendiz_combo.addItem("Selecione o aprendiz", "")

        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())

        self.atividade_input = QLineEdit()
        self.atividade_input.setPlaceholderText("Descreva a atividade realizada")

        self.tipo_servico_combo = QComboBox()
        self.tipo_servico_combo.addItem("Selecione o tipo de serviço", "")
        for tipo in TIPOS_SERVICO_ATIVIDADE:
            self.tipo_servico_combo.addItem(tipo, tipo)

        self.situacao_combo = QComboBox()
        self.situacao_combo.addItem("Selecione a situação", "")
        for situacao in SITUACOES_ATIVIDADE:
            self.situacao_combo.addItem(situacao, situacao)

        self.prazo_input = QDateEdit()
        self.prazo_input.setDisplayFormat("dd/MM/yyyy")
        self.prazo_input.setCalendarPopup(True)
        self.prazo_input.setMinimumDate(QDate(1900, 1, 1))
        self.prazo_input.setSpecialValueText("dd/mm/aaaa")
        self.prazo_input.setDate(self.prazo_input.minimumDate())

        self.responsavel_combo = QComboBox()
        self.responsavel_combo.addItem(CURRENT_USER_NAME, CURRENT_USER_NAME)

        self.observacao_input = QTextEdit()
        self.observacao_input.setPlaceholderText("Informações adicionais (opcional)")
        self.observacao_input.setFixedHeight(64)
        self.observacao_input.textChanged.connect(self._atualizar_contador_observacao)

        self.observacao_counter = QLabel(f"0 / {MAX_OBSERVACAO_CHARS}")
        self.observacao_counter.setObjectName("mutedText")
        self.observacao_counter.setAlignment(Qt.AlignmentFlag.AlignRight)

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self._add_labeled_widget(grid, 0, 0, "Aprendiz *", self.aprendiz_combo)
        self._add_labeled_widget(grid, 0, 1, "Data *", self.data_input)
        self._add_labeled_widget(grid, 1, 0, "Atividade executada *", self.atividade_input, 1, 2)
        self._add_labeled_widget(grid, 2, 0, "Tipo de serviço *", self.tipo_servico_combo)
        self._add_labeled_widget(grid, 2, 1, "Situação *", self.situacao_combo)
        self._add_labeled_widget(grid, 3, 0, "Prazo", self.prazo_input)
        self._add_labeled_widget(grid, 3, 1, "Responsável pelo registro *", self.responsavel_combo)
        self._add_labeled_widget(grid, 4, 0, "Observação", self.observacao_input, 1, 2)
        grid.addWidget(self.observacao_counter, 5, 0, 1, 2)
        panel.layout.addLayout(grid)

        actions = QHBoxLayout()
        actions.addStretch()

        clear_button = QPushButton("Limpar")
        clear_button.setObjectName("secondaryButton")
        clear_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton))
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_button.clicked.connect(self._limpar_formulario)

        save_button = QPushButton("Salvar atividade")
        save_button.setObjectName("primaryButton")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self._salvar_atividade)

        actions.addWidget(clear_button)
        actions.addWidget(save_button)
        panel.layout.addLayout(actions)
        return panel

    def _summary_panel(self) -> Panel:
        panel = Panel("Resumo das atividades")
        panel.setFixedWidth(280)

        for item in SUMMARY_ITEMS:
            panel.layout.addWidget(self._summary_card(item))

        panel.layout.addStretch()
        return panel

    def _summary_card(self, item: SummaryConfig) -> QFrame:
        card = QFrame()
        card.setObjectName("activitySummaryCard")
        card.setMinimumHeight(50)
        card.setStyleSheet(
            f"""
            QFrame#activitySummaryCard {{
                background: {item.background};
                border: 1px solid {item.border};
                border-radius: 7px;
            }}
            QFrame#activitySummaryCard QLabel {{
                border: none;
                background: transparent;
            }}
            """
        )

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        icon = QLabel()
        icon.setFixedSize(24, 24)
        icon.setPixmap(self.style().standardIcon(item.icon).pixmap(20, 20))

        title = QLabel(item.title)
        title.setStyleSheet(f"color: {item.color}; font-weight: 800;")

        value = QLabel("0")
        value.setStyleSheet(f"color: {item.color}; font-size: 16px; font-weight: 900;")
        value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.summary_values[item.key] = value

        layout.addWidget(icon)
        layout.addWidget(title, 1)
        layout.addWidget(value)
        return card

    def _table_panel(self) -> Panel:
        panel = Panel()
        panel.setMinimumWidth(0)
        panel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)

        header = QHBoxLayout()
        title = QLabel("Atividades registradas")
        title.setObjectName("sectionTitle")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar atividade...")
        self.search_input.setFixedWidth(280)
        self.search_input.textChanged.connect(self._carregar_tabela)

        filter_button = QPushButton("Filtrar")
        filter_button.setObjectName("secondaryButton")
        filter_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        filter_button.setCursor(Qt.CursorShape.PointingHandCursor)
        filter_button.clicked.connect(self._carregar_tabela)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search_input)
        header.addWidget(filter_button)
        panel.layout.addLayout(header)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            [
                "Data",
                "Aprendiz",
                "Atividade",
                "Tipo de serviço",
                "Situação",
                "Prazo",
                "Responsável",
                "Ações",
            ]
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(230)
        self.table.setMinimumWidth(0)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.table.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        panel.layout.addWidget(self.table)

        self.empty_label = QLabel("Nenhuma atividade registrada ainda.")
        self.empty_label.setObjectName("mutedText")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel.layout.addWidget(self.empty_label)

        footer = QHBoxLayout()
        self.counter_label = QLabel()
        self.counter_label.setObjectName("mutedText")
        footer.addWidget(self.counter_label)
        footer.addStretch()
        footer.addWidget(self._pagination_button("<", enabled=False))
        footer.addWidget(self._pagination_button("1", active=True, enabled=False))
        footer.addWidget(self._pagination_button(">", enabled=False))
        panel.layout.addLayout(footer)
        return panel

    def _pagination_button(self, text: str, active: bool = False, enabled: bool = True) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("primaryButton" if active else "secondaryButton")
        button.setFixedSize(38, 34)
        button.setEnabled(enabled)
        return button

    def _add_labeled_widget(
        self,
        grid: QGridLayout,
        row: int,
        column: int,
        label: str,
        widget,
        row_span: int = 1,
        column_span: int = 1,
    ):
        box = QVBoxLayout()
        box.setSpacing(5)
        text = QLabel(label)
        text.setStyleSheet("font-weight: 700;")
        widget.setMinimumWidth(0)
        policy = widget.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        widget.setSizePolicy(policy)
        if isinstance(widget, QComboBox):
            widget.setMinimumContentsLength(12)
            widget.setSizeAdjustPolicy(
                QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
            )
        box.addWidget(text)
        box.addWidget(widget)
        grid.addLayout(box, row, column, row_span, column_span)

    def _carregar_tabela(self, *_):
        termo = self.search_input.text().strip().lower() if hasattr(self, "search_input") else ""
        atividades = self._filtrar_atividades(termo)
        self.table.setRowCount(len(atividades))

        for row_index, atividade in enumerate(atividades):
            valores = [
                atividade.get("data", ""),
                atividade.get("aprendiz", ""),
                atividade.get("atividade", ""),
                atividade.get("tipo_servico", ""),
                atividade.get("situacao", ""),
                atividade.get("prazo", ""),
                atividade.get("responsavel", ""),
            ]
            for column, value in enumerate(valores):
                if column == 4 and value:
                    self.table.setCellWidget(row_index, column, StatusBadge(value))
                    continue
                self._set_text(row_index, column, value, center=column in (0, 4, 5))
            self.table.setCellWidget(row_index, 7, self._action_buttons())

        self.empty_label.setVisible(len(atividades) == 0)
        self.counter_label.setText(
            f"Mostrando {len(atividades)} de {len(self.atividades)} atividades"
        )

    def _filtrar_atividades(self, termo: str) -> list[dict[str, str]]:
        if not termo:
            return self.atividades

        return [
            atividade
            for atividade in self.atividades
            if termo
            in " ".join(str(valor).lower() for valor in atividade.values())
        ]

    def _set_text(self, row: int, column: int, text: str, center: bool = False):
        item = QTableWidgetItem(text)
        if center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, column, item)

    def _action_buttons(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        edit_button = QPushButton()
        edit_button.setObjectName("iconButton")
        edit_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        edit_button.setToolTip("Editar")
        edit_button.setEnabled(False)

        delete_button = QPushButton()
        delete_button.setObjectName("dangerButton")
        delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        delete_button.setToolTip("Excluir")
        delete_button.setEnabled(False)

        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        return widget

    def _atualizar_resumo(self):
        total = len(self.atividades)
        for item in SUMMARY_ITEMS:
            if item.key == "total":
                valor = total
            else:
                valor = sum(1 for atividade in self.atividades if atividade.get("situacao") == item.key)
            self.summary_values[item.key].setText(str(valor))

    def _atualizar_contador_observacao(self):
        texto = self.observacao_input.toPlainText()
        if len(texto) > MAX_OBSERVACAO_CHARS:
            cursor = self.observacao_input.textCursor()
            position = min(cursor.position(), MAX_OBSERVACAO_CHARS)
            self.observacao_input.blockSignals(True)
            self.observacao_input.setPlainText(texto[:MAX_OBSERVACAO_CHARS])
            cursor = self.observacao_input.textCursor()
            cursor.setPosition(position)
            self.observacao_input.setTextCursor(cursor)
            self.observacao_input.blockSignals(False)
            texto = self.observacao_input.toPlainText()

        self.observacao_counter.setText(f"{len(texto)} / {MAX_OBSERVACAO_CHARS}")

    def _salvar_atividade(self):
        erros = self._validar_formulario()
        if erros:
            QMessageBox.warning(self, "Verifique os dados", "\n".join(erros))
            return

        QMessageBox.information(
            self,
            "Registro preparado",
            "A tela já está pronta. A gravação das atividades será conectada em uma próxima etapa.",
        )

    def _validar_formulario(self) -> list[str]:
        erros = []
        if not self.aprendiz_combo.currentData():
            erros.append("Selecione o aprendiz.")
        if not self.atividade_input.text().strip():
            erros.append("Informe a atividade executada.")
        if not self.tipo_servico_combo.currentData():
            erros.append("Selecione o tipo de serviço.")
        if not self.situacao_combo.currentData():
            erros.append("Selecione a situação.")
        if not self.responsavel_combo.currentData():
            erros.append("Selecione o responsável pelo registro.")
        return erros

    def _limpar_formulario(self):
        self.aprendiz_combo.setCurrentIndex(0)
        self.data_input.setDate(QDate.currentDate())
        self.atividade_input.clear()
        self.tipo_servico_combo.setCurrentIndex(0)
        self.situacao_combo.setCurrentIndex(0)
        self.prazo_input.setDate(self.prazo_input.minimumDate())
        self.responsavel_combo.setCurrentIndex(0)
        self.observacao_input.clear()
        self._atualizar_contador_observacao()
        self.aprendiz_combo.setFocus()

    def ao_exibir(self):
        self._carregar_tabela()
        self._atualizar_resumo()
