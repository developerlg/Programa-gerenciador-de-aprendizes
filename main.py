import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from database.criar_tabelas import inicializar_banco
from views.tela_principal import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Acompanhamento de Jovens Aprendizes")

    try:
        inicializar_banco()
    except Exception as exc:
        QMessageBox.critical(
            None,
            "Erro ao iniciar",
            f"Nao foi possivel inicializar o banco de dados.\n\n{exc}",
        )
        return 1

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
