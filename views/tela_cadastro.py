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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from controllers.aprendiz_controller import AprendizController
from data.opcoes import SETORES_APRENDIZES
from services.aprendiz_service import ValidationError
from views.widgets import Panel, StatusBadge


class CadastroAprendizesView(QWidget):
    def __init__(self, controller: AprendizController | None = None, parent=None):
        super().__init__(parent)
        self.controller = controller or AprendizController()
        self.aprendiz_em_edicao: int | None = None
        self._build_ui()
        self._carregar_supervisores()
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
        title = QLabel("Cadastro de Aprendizes")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Cadastre os jovens e vincule cada um ao supervisor responsavel.")
        subtitle.setObjectName("mutedText")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        self.novo_button = QPushButton("+  Novo Aprendiz")
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
        panel = Panel("Dados do Aprendiz")

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Digite o nome do jovem")

        self.cpf_input = QLineEdit()
        self.cpf_input.setPlaceholderText("000.000.000-00")
        self.cpf_input.setInputMask("000.000.000-00;_")

        self.setor_combo = QComboBox()
        self.setor_combo.addItem("Selecione o setor", "")
        self.setor_combo.addItems(SETORES_APRENDIZES)

        self.supervisor_combo = QComboBox()

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Ativo", "Inativo"])

        self.observacao_input = QTextEdit()
        self.observacao_input.setPlaceholderText("Observação opcional")
        self.observacao_input.setFixedHeight(88)

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(12)

        self._add_labeled_widget(grid, 0, 0, "Nome *", self.nome_input)
        self._add_labeled_widget(grid, 0, 1, "CPF *", self.cpf_input)
        self._add_labeled_widget(grid, 1, 0, "Setor *", self.setor_combo)
        self._add_labeled_widget(grid, 1, 1, "Supervisor *", self.supervisor_combo)
        self._add_labeled_widget(grid, 2, 0, "Status", self.status_combo)
        self._add_labeled_widget(grid, 2, 1, "Observação", self.observacao_input)

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
        self.save_button.clicked.connect(self._salvar_aprendiz)

        actions.addWidget(clear_button)
        actions.addWidget(self.save_button)
        panel.layout.addLayout(actions)
        return panel

    def _table_panel(self) -> Panel:
        panel = Panel()
        header = QHBoxLayout()

        title = QLabel("Aprendizes cadastrados")
        title.setObjectName("sectionTitle")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome, CPF, setor ou supervisor...")
        self.search_input.setFixedWidth(340)
        self.search_input.textChanged.connect(self._carregar_tabela)

        refresh_button = QPushButton("Atualizar")
        refresh_button.setObjectName("secondaryButton")
        refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_button.clicked.connect(self._atualizar_tela)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search_input)
        header.addWidget(refresh_button)
        panel.layout.addLayout(header)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nome", "CPF", "Setor", "Supervisor", "Status", "Ações"]
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(270)
        self.table.doubleClicked.connect(self._editar_linha_selecionada)

        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

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

    def _carregar_supervisores(self):
        atual = self.supervisor_combo.currentData()
        self.supervisor_combo.clear()
        self.supervisor_combo.addItem("Selecione o supervisor", "")
        supervisores = self.controller.listar_supervisores_ativos()

        for supervisor in supervisores:
            self.supervisor_combo.addItem(supervisor["nome"], supervisor["id"])

        if atual:
            index = self.supervisor_combo.findData(atual)
            if index >= 0:
                self.supervisor_combo.setCurrentIndex(index)

    def _carregar_tabela(self, *_):
        termo = self.search_input.text() if hasattr(self, "search_input") else ""
        aprendizes = self.controller.listar_aprendizes(termo)
        self.table.setRowCount(len(aprendizes))

        for row_index, aprendiz in enumerate(aprendizes):
            self._set_text(row_index, 0, str(aprendiz["id"]), center=True)
            self._set_text(row_index, 1, aprendiz["nome"])
            self._set_text(row_index, 2, aprendiz["cpf"], center=True)
            self._set_text(row_index, 3, aprendiz["setor"])
            self._set_text(row_index, 4, aprendiz["supervisor_nome"])
            self.table.setCellWidget(row_index, 5, StatusBadge(aprendiz["status"]))
            self.table.setCellWidget(row_index, 6, self._action_buttons(aprendiz))

        self.counter_label.setText(f"Mostrando {len(aprendizes)} registro(s)")

    def _set_text(self, row: int, column: int, text: str, center: bool = False):
        item = QTableWidgetItem(text)
        if center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, column, item)

    def _action_buttons(self, aprendiz: dict) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        edit_button = QPushButton("Editar")
        edit_button.setObjectName("iconButton")
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_button.clicked.connect(
            lambda checked=False, aprendiz_id=aprendiz["id"]: self._carregar_para_edicao(aprendiz_id)
        )

        inactive_button = QPushButton("Inativar")
        inactive_button.setObjectName("dangerButton")
        inactive_button.setCursor(Qt.CursorShape.PointingHandCursor)
        inactive_button.setEnabled(aprendiz["status"] != "Inativo")
        inactive_button.clicked.connect(
            lambda checked=False, aprendiz_id=aprendiz["id"]: self._inativar_aprendiz(aprendiz_id)
        )

        layout.addWidget(edit_button)
        layout.addWidget(inactive_button)
        return widget

    def _coletar_dados(self) -> dict:
        return {
            "nome": self.nome_input.text(),
            "cpf": self.cpf_input.text(),
            "setor": self.setor_combo.currentData() or self.setor_combo.currentText(),
            "observacao": self.observacao_input.toPlainText(),
            "supervisor_id": self.supervisor_combo.currentData(),
            "ativo": self.status_combo.currentText() == "Ativo",
        }

    def _salvar_aprendiz(self):
        try:
            self.controller.salvar_aprendiz(
                self._coletar_dados(),
                self.aprendiz_em_edicao,
            )
        except ValidationError as exc:
            QMessageBox.warning(self, "Verifique os dados", str(exc))
            return
        except Exception as exc:
            QMessageBox.critical(self, "Erro ao salvar", str(exc))
            return

        QMessageBox.information(self, "Cadastro salvo", "Aprendiz salvo com sucesso.")
        self._limpar_formulario()
        self._carregar_tabela()

    def _carregar_para_edicao(self, aprendiz_id: int):
        aprendiz = self.controller.obter_aprendiz(aprendiz_id)
        if not aprendiz:
            QMessageBox.warning(self, "Não encontrado", "Aprendiz não encontrado.")
            return

        self.aprendiz_em_edicao = aprendiz_id
        self.nome_input.setText(aprendiz["nome"])
        self.cpf_input.setText(aprendiz["cpf"])
        self._selecionar_combo_por_texto(self.setor_combo, aprendiz["setor"])
        self.observacao_input.setPlainText(aprendiz["observacao"])
        self._selecionar_supervisor(aprendiz["supervisor_id"])
        self.status_combo.setCurrentText(aprendiz["status"])
        self.save_button.setText("Salvar alterações")

    def _selecionar_supervisor(self, supervisor_id: int):
        index = self.supervisor_combo.findData(supervisor_id)
        self.supervisor_combo.setCurrentIndex(index if index >= 0 else 0)

    def _selecionar_combo_por_texto(self, combo: QComboBox, texto: str):
        index = combo.findText(texto)
        if index == -1 and texto:
            combo.addItem(texto, texto)
            index = combo.findText(texto)
        combo.setCurrentIndex(index if index >= 0 else 0)

    def _editar_linha_selecionada(self):
        row = self.table.currentRow()
        if row < 0:
            return
        item = self.table.item(row, 0)
        if item:
            self._carregar_para_edicao(int(item.text()))

    def _inativar_aprendiz(self, aprendiz_id: int):
        resposta = QMessageBox.question(
            self,
            "Inativar aprendiz",
            "Deseja inativar este aprendiz? O registro sera mantido no banco.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.inativar_aprendiz(aprendiz_id)
        except Exception as exc:
            QMessageBox.critical(self, "Erro ao inativar", str(exc))
            return

        self._carregar_tabela()

    def _atualizar_tela(self):
        self._carregar_supervisores()
        self._carregar_tabela()

    def ao_exibir(self):
        self._atualizar_tela()

    def _limpar_formulario(self):
        self.aprendiz_em_edicao = None
        self.nome_input.clear()
        self.cpf_input.clear()
        self.setor_combo.setCurrentIndex(0)
        self.observacao_input.clear()
        self.supervisor_combo.setCurrentIndex(0)
        self.status_combo.setCurrentText("Ativo")
        self.save_button.setText("Salvar")
        self.nome_input.setFocus()
