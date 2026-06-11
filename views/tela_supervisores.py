from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from controllers.supervisor_controller import SupervisorController
from services.aprendiz_service import ValidationError
from views.widgets import Panel, StatusBadge


class CadastroSupervisoresView(QWidget):
    def __init__(self, controller: SupervisorController | None = None, parent=None):
        super().__init__(parent)
        self.controller = controller or SupervisorController()
        self.supervisor_em_edicao: int | None = None
        self._build_ui()
        self._carregar_tabela()

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

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Cadastro de Supervisores")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Cadastre os servidores que supervisionam os jovens aprendizes.")
        subtitle.setObjectName("mutedText")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        self.novo_button = QPushButton("+  Novo Supervisor")
        self.novo_button.setObjectName("secondaryButton")
        self.novo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.novo_button.clicked.connect(self._limpar_formulario)

        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(self.novo_button)
        page_layout.addLayout(header)

        page_layout.addWidget(self._form_panel())
        page_layout.addWidget(self._table_panel())

    def _form_panel(self) -> Panel:
        panel = Panel("Dados do Supervisor")

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Digite o nome do servidor")

        self.funcao_input = QLineEdit()
        self.funcao_input.setPlaceholderText("Digite a funcao")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Ativo", "Inativo"])

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(12)
        self._add_labeled_widget(grid, 0, 0, "Nome *", self.nome_input)
        self._add_labeled_widget(grid, 0, 1, "Funcao *", self.funcao_input)
        self._add_labeled_widget(grid, 1, 0, "Status", self.status_combo)
        panel.layout.addLayout(grid)

        actions = QHBoxLayout()
        actions.addStretch()

        clear_button = QPushButton("Limpar")
        clear_button.setObjectName("secondaryButton")
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_button.clicked.connect(self._limpar_formulario)

        self.save_button = QPushButton("Salvar")
        self.save_button.setObjectName("primaryButton")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self._salvar_supervisor)

        actions.addWidget(clear_button)
        actions.addWidget(self.save_button)
        panel.layout.addLayout(actions)
        return panel

    def _table_panel(self) -> Panel:
        panel = Panel()
        header = QHBoxLayout()

        title = QLabel("Supervisores cadastrados")
        title.setObjectName("sectionTitle")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar supervisor...")
        self.search_input.setFixedWidth(280)
        self.search_input.textChanged.connect(self._carregar_tabela)

        refresh_button = QPushButton("Atualizar")
        refresh_button.setObjectName("secondaryButton")
        refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_button.clicked.connect(self._carregar_tabela)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search_input)
        header.addWidget(refresh_button)
        panel.layout.addLayout(header)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Funcao", "Status", "Acoes"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(260)
        self.table.doubleClicked.connect(self._editar_linha_selecionada)

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        panel.layout.addWidget(self.table)
        self.counter_label = QLabel()
        self.counter_label.setObjectName("mutedText")
        panel.layout.addWidget(self.counter_label)
        return panel

    def _add_labeled_widget(self, grid: QGridLayout, row: int, column: int, label: str, widget):
        box = QVBoxLayout()
        text = QLabel(label)
        text.setStyleSheet("font-weight: 700;")
        box.addWidget(text)
        box.addWidget(widget)
        grid.addLayout(box, row, column)

    def _carregar_tabela(self, *_):
        termo = self.search_input.text() if hasattr(self, "search_input") else ""
        supervisores = self.controller.listar_supervisores(termo)
        self.table.setRowCount(len(supervisores))

        for row_index, supervisor in enumerate(supervisores):
            self._set_text(row_index, 0, str(supervisor["id"]), center=True)
            self._set_text(row_index, 1, supervisor["nome"])
            self._set_text(row_index, 2, supervisor["funcao"])
            self.table.setCellWidget(row_index, 3, StatusBadge(supervisor["status"]))
            self.table.setCellWidget(row_index, 4, self._action_buttons(supervisor))

        self.counter_label.setText(f"Mostrando {len(supervisores)} registro(s)")

    def _set_text(self, row: int, column: int, text: str, center: bool = False):
        item = QTableWidgetItem(text)
        if center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, column, item)

    def _action_buttons(self, supervisor: dict) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        edit_button = QPushButton("Editar")
        edit_button.setObjectName("iconButton")
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_button.clicked.connect(
            lambda checked=False, supervisor_id=supervisor["id"]: self._carregar_para_edicao(supervisor_id)
        )

        inactive_button = QPushButton("Inativar")
        inactive_button.setObjectName("dangerButton")
        inactive_button.setCursor(Qt.CursorShape.PointingHandCursor)
        inactive_button.setEnabled(supervisor["status"] != "Inativo")
        inactive_button.clicked.connect(
            lambda checked=False, supervisor_id=supervisor["id"]: self._inativar_supervisor(supervisor_id)
        )

        layout.addWidget(edit_button)
        layout.addWidget(inactive_button)
        return widget

    def _coletar_dados(self) -> dict:
        return {
            "nome": self.nome_input.text(),
            "funcao": self.funcao_input.text(),
            "ativo": self.status_combo.currentText() == "Ativo",
        }

    def _salvar_supervisor(self):
        try:
            self.controller.salvar_supervisor(
                self._coletar_dados(),
                self.supervisor_em_edicao,
            )
        except ValidationError as exc:
            QMessageBox.warning(self, "Verifique os dados", str(exc))
            return
        except Exception as exc:
            QMessageBox.critical(self, "Erro ao salvar", str(exc))
            return

        QMessageBox.information(self, "Cadastro salvo", "Supervisor salvo com sucesso.")
        self._limpar_formulario()
        self._carregar_tabela()

    def _carregar_para_edicao(self, supervisor_id: int):
        supervisor = self.controller.obter_supervisor(supervisor_id)
        if not supervisor:
            QMessageBox.warning(self, "Nao encontrado", "Supervisor nao encontrado.")
            return

        self.supervisor_em_edicao = supervisor_id
        self.nome_input.setText(supervisor["nome"])
        self.funcao_input.setText(supervisor["funcao"])
        self.status_combo.setCurrentText(supervisor["status"])
        self.save_button.setText("Salvar alteracoes")

    def _editar_linha_selecionada(self):
        row = self.table.currentRow()
        if row < 0:
            return
        item = self.table.item(row, 0)
        if item:
            self._carregar_para_edicao(int(item.text()))

    def _inativar_supervisor(self, supervisor_id: int):
        resposta = QMessageBox.question(
            self,
            "Inativar supervisor",
            "Deseja inativar este supervisor? O registro sera mantido no banco.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.inativar_supervisor(supervisor_id)
        except Exception as exc:
            QMessageBox.critical(self, "Erro ao inativar", str(exc))
            return

        self._carregar_tabela()

    def _limpar_formulario(self):
        self.supervisor_em_edicao = None
        self.nome_input.clear()
        self.funcao_input.clear()
        self.status_combo.setCurrentText("Ativo")
        self.save_button.setText("Salvar")
        self.nome_input.setFocus()
