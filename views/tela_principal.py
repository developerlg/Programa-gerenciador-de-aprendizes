from datetime import datetime

from PySide6.QtCore import QEvent, QTimer, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from config import APP_TITLE, APP_VERSION, CURRENT_USER_NAME, CURRENT_USER_ROLE, DATABASE_PATH
from views.styles import APP_STYLESHEET
from views.tela_atividades import TelaAtividades
from views.tela_avaliacao import TelaAvaliacao
from views.tela_cadastro import CadastroAprendizesView
from views.tela_configuracoes import TelaConfiguracoes
from views.tela_consulta import TelaConsulta
from views.tela_dashboard import DashboardView
from views.tela_historico import TelaHistorico
from views.tela_relatorios import TelaRelatorios


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(1180, 720)
        self.resize(1366, 820)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(APP_STYLESHEET)
        self._drag_position = None
        self.menu_buttons: list[QPushButton] = []

        self._build_ui()
        self._setup_clock()
        self._set_page(0)

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("appRoot")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(root)

        self.top_bar = self._top_bar()
        self.top_bar.installEventFilter(self)
        root_layout.addWidget(self.top_bar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        body.addWidget(self._sidebar())

        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardView())
        self.stack.addWidget(CadastroAprendizesView())
        self.stack.addWidget(TelaAtividades())
        self.stack.addWidget(TelaConsulta())
        self.stack.addWidget(TelaHistorico())
        self.stack.addWidget(TelaAvaliacao())
        self.stack.addWidget(TelaRelatorios())
        self.stack.addWidget(TelaConfiguracoes())
        body.addWidget(self.stack, 1)

        root_layout.addLayout(body, 1)
        root_layout.addWidget(self._footer())

    def _top_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("topBar")
        bar.setFixedHeight(58)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(18, 0, 14, 0)
        layout.setSpacing(12)

        logo = QLabel("■")
        logo.setStyleSheet("color: #0B55B7; font-size: 20px; font-weight: 800;")
        title = QLabel(APP_TITLE)
        title.setObjectName("appTitle")

        user_icon = QLabel("●")
        user_icon.setStyleSheet("color: #0B55B7; font-size: 22px;")
        user_box = QVBoxLayout()
        user_box.setSpacing(0)
        name = QLabel(CURRENT_USER_NAME)
        name.setStyleSheet("font-weight: 800;")
        role = QLabel(CURRENT_USER_ROLE)
        role.setObjectName("mutedText")
        user_box.addWidget(name)
        user_box.addWidget(role)

        minimize = self._window_button("−", self.showMinimized)
        maximize = self._window_button("□", self._toggle_maximized)
        close = self._window_button("×", self.close, close_button=True)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(user_icon)
        layout.addLayout(user_box)
        layout.addSpacing(18)
        layout.addWidget(minimize)
        layout.addWidget(maximize)
        layout.addWidget(close)
        return bar

    def _window_button(self, text: str, callback, close_button: bool = False) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("closeWindowButton" if close_button else "windowButton")
        button.setFixedSize(38, 32)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        return button

    def _sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(14, 20, 14, 16)
        layout.setSpacing(8)

        menu_items = [
            ("Tela Inicial", QStyle.StandardPixmap.SP_DirHomeIcon),
            ("Cadastro de\nAprendizes", QStyle.StandardPixmap.SP_FileDialogNewFolder),
            ("Registro de\nAtividade", QStyle.StandardPixmap.SP_FileDialogDetailedView),
            ("Consulta de\nAndamento", QStyle.StandardPixmap.SP_FileDialogContentsView),
            ("Historico do\nAprendiz", QStyle.StandardPixmap.SP_FileIcon),
            ("Avaliacao de\nDesempenho", QStyle.StandardPixmap.SP_ComputerIcon),
            ("Relatorios", QStyle.StandardPixmap.SP_FileLinkIcon),
            ("Configuracoes", QStyle.StandardPixmap.SP_FileDialogInfoView),
        ]

        for index, (label, icon_type) in enumerate(menu_items):
            button = QPushButton(label)
            button.setObjectName("menuButton")
            button.setIcon(self.style().standardIcon(icon_type))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(50)
            button.clicked.connect(lambda checked=False, page=index: self._set_page(page))
            self.menu_buttons.append(button)
            layout.addWidget(button)

        layout.addStretch()
        layout.addWidget(self._database_status())
        layout.addSpacing(10)
        self.date_label = QLabel()
        self.time_label = QLabel()
        for label in (self.date_label, self.time_label):
            label.setStyleSheet("color: #FFFFFF; font-weight: 600;")
            layout.addWidget(label)

        return sidebar

    def _database_status(self) -> QFrame:
        box = QFrame()
        box.setObjectName("sidebarInfo")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(2)

        title = QLabel("Banco de dados")
        title.setStyleSheet("color: #FFFFFF; font-weight: 800;")
        engine = QLabel("SQLite")
        engine.setStyleSheet("color: #FFFFFF; font-weight: 700;")
        status = QLabel("● Conectado")
        status.setStyleSheet("color: #7CFF76; font-weight: 700;")

        layout.addWidget(title)
        layout.addWidget(engine)
        layout.addWidget(status)
        box.setToolTip(str(DATABASE_PATH))
        return box

    def _footer(self) -> QFrame:
        footer = QFrame()
        footer.setObjectName("topBar")
        footer.setFixedHeight(38)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(24, 0, 24, 0)

        left = QLabel(f"{APP_TITLE}   |   Versao {APP_VERSION}")
        left.setObjectName("mutedText")
        right = QLabel("© 2026 - Todos os direitos reservados")
        right.setObjectName("mutedText")

        layout.addWidget(left)
        layout.addStretch()
        layout.addWidget(right)
        return footer

    def _setup_clock(self):
        self._update_clock()
        timer = QTimer(self)
        timer.timeout.connect(self._update_clock)
        timer.start(30_000)
        self._clock_timer = timer

    def _update_clock(self):
        now = datetime.now()
        meses = [
            "janeiro",
            "fevereiro",
            "marco",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        ]
        self.date_label.setText(f"{now.day} de {meses[now.month - 1]} de {now.year}")
        self.time_label.setText(now.strftime("%H:%M"))

    def _set_page(self, index: int):
        self.stack.setCurrentIndex(index)
        for button_index, button in enumerate(self.menu_buttons):
            button.setProperty("active", button_index == index)
            button.style().unpolish(button)
            button.style().polish(button)

    def _toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def eventFilter(self, watched, event):
        if watched is self.top_bar:
            if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                return True

            if (
                event.type() == QEvent.Type.MouseMove
                and self._drag_position is not None
                and event.buttons() & Qt.MouseButton.LeftButton
                and not self.isMaximized()
            ):
                self.move(event.globalPosition().toPoint() - self._drag_position)
                return True

            if event.type() == QEvent.Type.MouseButtonRelease:
                self._drag_position = None
                return True

        return super().eventFilter(watched, event)
