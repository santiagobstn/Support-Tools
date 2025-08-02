import sys
import os
import subprocess
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy,
    QDialog, QTextEdit, QDialogButtonBox, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from modules import drivers_update, evidence_collector, printer_fixer, cache_manager
from modules.security_status import get_bitlocker_status, get_antivirus_status

# ===================== THREADS BASE =====================

class BaseThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, action_name):
        super().__init__()
        self.action_name = action_name

    def finish(self):
        self.finished_signal.emit(f"{self.action_name} concluído com sucesso!")


class EvidenceCollectorThread(BaseThread):
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        evidence_collector.collect_evidence(cb)
        self.finish()

class PrinterFixerThread(BaseThread):
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        printer_fixer.fix_printers(cb)
        self.finish()

class CacheManagerThread(BaseThread):
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        cache_manager.cleanup_cache(cb)
        self.finish()

class UpdateDriversThread(BaseThread):
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        summary = drivers_update.update_all_drivers(cb)
        self.finished_signal.emit(summary)


# ===================== STATUS =====================

BITLOCKER_STATUS = get_bitlocker_status()

def get_machine_status_text():
    hostname = os.getenv("COMPUTERNAME", "")
    user = os.getlogin()
    os_name = f"Win{os.sys.getwindowsversion().major}"
    disk = psutil.disk_usage('C:\\')
    disk_text = f"{disk.used//(1024**3)}GB/{disk.total//(1024**3)}GB"
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    uptime = psutil.boot_time()
    from datetime import datetime
    uptime_str = str(datetime.now() - datetime.fromtimestamp(uptime)).split('.')[0]
    av_status = get_antivirus_status()

    col1 = f"HOST: {hostname}\nUSER: {user}\nOS: {os_name}"
    col2 = f"DISK: {disk_text}\nRAM: {ram}%\nCPU: {cpu}%"
    col3 = f"BITLOCKER: {BITLOCKER_STATUS}\nANTI-VIRUS: {av_status}\nUPTIME: {uptime_str}"
    return col1, col2, col3


# ===================== LOG WINDOW =====================

class LogWindow(QDialog):
    def __init__(self, logs):
        super().__init__()
        self.setWindowTitle("Logs")
        self.resize(600, 400)
        layout = QVBoxLayout()

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText("\n".join(logs))
        layout.addWidget(text_area)

        btns = QDialogButtonBox(QDialogButtonBox.Close)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        self.setLayout(layout)


# ===================== AÇÕES =====================

def start_action(win, thread_class, action_name):
    win.add_log(f"Executando {action_name}...")
    thread = thread_class(action_name)
    win.thread = thread
    thread.log_signal.connect(win.add_log)
    thread.finished_signal.connect(lambda msg: show_finished(win, msg))
    thread.start()

def show_finished(win, msg):
    win.add_log(msg)
    QMessageBox.information(win, "Concluído", msg)

def run_cache_manager(win): start_action(win, CacheManagerThread, "Cache Temp Manager")
def run_printer_fixer(win): start_action(win, PrinterFixerThread, "Printer Fixer")
def run_update_all_drivers(win): start_action(win, UpdateDriversThread, "Drivers Update")
def run_evidence_collector(win): start_action(win, EvidenceCollectorThread, "Evidence Collector")

def run_see_evidences(win):
    p = r"C:\Evidencias"
    win.add_log(f"Abrindo {p}")
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)
    subprocess.run(f'explorer "{p}"', shell=True)


# ===================== UI =====================

class SupportToolsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Support Tools")
        self.setGeometry(100, 100, 800, 550)
        self.thread = None
        self.logs = []
        self.initUI()

    def add_log(self, text):
        self.logs.append(text)

    def show_logs(self):
        dlg = LogWindow(self.logs)
        dlg.exec_()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget { font-family: Segoe UI; font-size: 11pt; }
            QPushButton {
                background-color: #d3d3d3;
                color: black; border: none; padding: 12px;
                border-radius: 15px;
                min-width: 180px;
                min-height: 45px;
            }
            QPushButton:hover { background-color: #bfbfbf; }
            QLabel.link {
                color: #2a82da;
                text-decoration: underline;
            }
        """)

        # LOGO CENTRALIZADA
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join("icons", "icon.png")).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # INFO CENTRALIZADA
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-weight: bold; color: white;")
        main_layout.addWidget(self.info_label)

        def update_status():
            c1, c2, c3 = get_machine_status_text()
            self.info_label.setText(f"{c1}\n{c2}\n{c3}")

        update_status()
        timer = QTimer(self)
        timer.timeout.connect(update_status)
        timer.start(5000)

        # BOTÕES
        center_layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(20)

        buttons = [
            ("Cache Temp Manager", lambda: run_cache_manager(self)),
            ("Printer Fixer", lambda: run_printer_fixer(self)),
            ("Evidence Collector", lambda: run_evidence_collector(self)),
            ("Drivers Update", lambda: run_update_all_drivers(self)),
        ]
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for pos, (name, action) in zip(positions, buttons):
            btn = QPushButton(name)
            btn.setFixedSize(200, 50)
            btn.clicked.connect(action)
            grid.addWidget(btn, *pos, alignment=Qt.AlignCenter)

        center_layout.addLayout(grid)

        main_layout.addLayout(center_layout)

        # LINKS
        footer_links = QHBoxLayout()
        footer_links.setAlignment(Qt.AlignCenter)

        see_label = QLabel('<a href="#">See Evidences</a>')
        see_label.setObjectName("link")
        see_label.setAlignment(Qt.AlignCenter)
        see_label.setOpenExternalLinks(False)
        see_label.linkActivated.connect(lambda _: run_see_evidences(self))

        logs_label = QLabel('<a href="#">View Logs</a>')
        logs_label.setObjectName("link")
        logs_label.setAlignment(Qt.AlignCenter)
        logs_label.setOpenExternalLinks(False)
        logs_label.linkActivated.connect(lambda _: self.show_logs())

        footer_links.addWidget(see_label)
        footer_links.addSpacing(40)
        footer_links.addWidget(logs_label)

        main_layout.addLayout(footer_links)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)


# ===================== THEME =====================

def set_dark_theme(app):
    app.setStyle("Fusion")
    p = QPalette()
    p.setColor(QPalette.Window, QColor(30, 30, 30))
    p.setColor(QPalette.WindowText, Qt.white)
    p.setColor(QPalette.Base, QColor(20, 20, 20))
    p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    p.setColor(QPalette.Text, Qt.white)
    p.setColor(QPalette.Button, QColor(53, 53, 53))
    p.setColor(QPalette.ButtonText, Qt.white)
    p.setColor(QPalette.Link, QColor(42, 130, 218))
    p.setColor(QPalette.Highlight, QColor(42, 130, 218))
    p.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme(app)
    w = SupportToolsApp()
    w.show()
    sys.exit(app.exec_())
