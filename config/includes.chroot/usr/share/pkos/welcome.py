"""Small first-login welcome and permanent About pkOS application."""
from pathlib import Path
import subprocess
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

live = 'boot=live' in Path('/proc/cmdline').read_text().split()
state = Path.home() / '.local/state/pkos'
shown = state / 'welcome-shown'
if '--autostart' in sys.argv and shown.exists() and not live:
    sys.exit(0)
app = QApplication(sys.argv)
app.setDesktopFileName('pk-welcome')
app.setWindowIcon(QIcon('/usr/share/icons/hicolor/scalable/apps/pkos.svg'))
window = QWidget()
window.setWindowTitle('pkOS')
window.setFixedSize(580, 480)
window.setStyleSheet('''
QWidget { background:#10151b; color:#dce4ed; font:14px "Inter"; }
QPushButton { background:#253443; border:1px solid #41586a; border-radius:8px; padding:14px; text-align:left; }
QPushButton:hover { background:#334858; }
QLabel { background:transparent; }
''')
layout = QVBoxLayout(window)
layout.setContentsMargins(40, 32, 40, 32)
layout.setSpacing(18)
logo = QLabel('pkOS')
logo.setStyleSheet('font-size:44px; font-weight:600; color:#edf2f7;')
layout.addWidget(logo)
layout.addWidget(QLabel('A quiet place to build.'))
description = QLabel('A focused workspace for code and AI.\nPlasma 6 · Wayland · Intel + NVIDIA')
description.setStyleSheet('color:#9baab9;')
layout.addWidget(description)
if live:
    warning = QLabel('Install replaces the selected disk, including Windows,\nits recovery partitions and all personal files. Back up first.')
    warning.setWordWrap(True)
    warning.setStyleSheet('color:#d8b99a;')
    layout.addWidget(warning)
    install = QPushButton('Install pkOS  →')
    install.clicked.connect(lambda: subprocess.Popen(['pk-install']))
    layout.addWidget(install)
else:
    setup = QPushButton('Prepare your workspace  →')
    setup.clicked.connect(lambda: subprocess.Popen(['konsole', '-e', 'pk-setup']))
    layout.addWidget(setup)
help_button = QPushButton('Read the guide')
help_button.clicked.connect(lambda: subprocess.Popen(['kate', '/usr/share/doc/pkos/README.md']))
layout.addWidget(help_button)
close = QPushButton('Explore pkOS' if live else 'Later')
close.clicked.connect(window.close)
layout.addWidget(close)
state.mkdir(parents=True, exist_ok=True)
shown.touch()
window.show()
sys.exit(app.exec())

