PRIMARY = "#0B55B7"
PRIMARY_DARK = "#073B82"
PRIMARY_LIGHT = "#EAF3FF"
BACKGROUND = "#F6F9FD"
BORDER = "#DCE6F2"
TEXT = "#0F172A"
MUTED = "#667085"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#F97316"


APP_STYLESHEET = f"""
QWidget {{
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 14px;
    color: {TEXT};
}}

QWidget#appRoot, QWidget#pageBackground {{
    background: {BACKGROUND};
}}

QFrame#topBar {{
    background: #FFFFFF;
    border-bottom: 1px solid {BORDER};
}}

QFrame#sidebar {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 {PRIMARY_DARK},
        stop: 1 #0057C2
    );
}}

QLabel#appTitle {{
    font-size: 16px;
    font-weight: 700;
}}

QLabel#pageTitle {{
    font-size: 26px;
    font-weight: 800;
}}

QLabel#sectionTitle {{
    font-size: 16px;
    font-weight: 700;
}}

QLabel#mutedText {{
    color: {MUTED};
}}

QPushButton#menuButton {{
    background: transparent;
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
    padding: 8px 14px;
    text-align: left;
}}

QPushButton#menuButton:hover {{
    background: rgba(255, 255, 255, 0.12);
}}

QPushButton#menuButton[active="true"] {{
    background: #1268D6;
}}

QPushButton#primaryButton {{
    background: {PRIMARY};
    border: 1px solid {PRIMARY};
    border-radius: 7px;
    color: #FFFFFF;
    font-weight: 700;
    padding: 9px 16px;
}}

QPushButton#primaryButton:hover {{
    background: #074DAA;
}}

QPushButton#secondaryButton {{
    background: #FFFFFF;
    border: 1px solid #B8C7DA;
    border-radius: 7px;
    color: {TEXT};
    font-weight: 600;
    padding: 9px 16px;
}}

QPushButton#secondaryButton:hover {{
    background: #F3F7FC;
}}

QPushButton#iconButton {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 7px;
    color: {PRIMARY};
    font-weight: 700;
    padding: 6px 10px;
}}

QPushButton#dangerButton {{
    background: #FFFFFF;
    border: 1px solid #F8B4B4;
    border-radius: 7px;
    color: {DANGER};
    font-weight: 700;
    padding: 6px 10px;
}}

QPushButton#windowButton {{
    background: transparent;
    border: none;
    color: {TEXT};
    font-size: 18px;
    padding: 6px 12px;
}}

QPushButton#windowButton:hover {{
    background: #EEF3F8;
}}

QPushButton#closeWindowButton {{
    background: transparent;
    border: none;
    color: {TEXT};
    font-size: 18px;
    padding: 6px 12px;
}}

QPushButton#closeWindowButton:hover {{
    background: #E5484D;
    color: #FFFFFF;
}}

QFrame#panel, QFrame#statCard {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

QFrame#sidebarInfo {{
    background: rgba(3, 24, 70, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 8px;
}}

QLineEdit, QComboBox, QTextEdit {{
    background: #FFFFFF;
    border: 1px solid #C8D4E3;
    border-radius: 7px;
    padding: 8px 10px;
}}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
    border: 1px solid {PRIMARY};
}}

QTableWidget {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 7px;
    gridline-color: #E6ECF4;
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {TEXT};
}}

QHeaderView::section {{
    background: #F5F8FC;
    border: none;
    border-right: 1px solid #E1E8F0;
    border-bottom: 1px solid #E1E8F0;
    font-weight: 700;
    padding: 8px;
}}

QScrollArea {{
    background: transparent;
    border: none;
}}
"""
