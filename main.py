import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from config import APP_ICON_PATH, garantir_pastas_execucao
from database.criar_tabelas import inicializar_banco
from views.tela_principal import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Acompanhamento de Jovens Aprendizes")
    if APP_ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(APP_ICON_PATH)))

    try:
        garantir_pastas_execucao()
        inicializar_banco()
    except Exception as exc:
        QMessageBox.critical(
            None,
            "Erro ao iniciar",
            f"Nao foi possivel inicializar o banco de dados.\n\n{exc}",
        )
        return 1

    window = MainWindow()
    if APP_ICON_PATH.exists():
        window.setWindowIcon(QIcon(str(APP_ICON_PATH)))
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
