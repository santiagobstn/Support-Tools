import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from modules import evidence_collector, printer_fixer, cache_manager, driver_doctor

class EvidenceCollectorThread(QThread):
    log_signal = pyqtSignal(str)
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        evidence_collector.collect_evidence(cb)

class PrinterFixerThread(QThread):
    log_signal = pyqtSignal(str)
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        printer_fixer.fix_printers(cb)

class CacheManagerThread(QThread):
    log_signal = pyqtSignal(str)
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        cache_manager.cleanup_cache(cb)

class DriverDoctorThread(QThread):
    log_signal = pyqtSignal(str)
    def run(self):
        def cb(msg): self.log_signal.emit(msg)
        driver_doctor.scan_drivers(cb)

def run_machine_infos(log):
    log("Coletando informações da máquina...")
    try:
        r = subprocess.run("systeminfo", capture_output=True, text=True, shell=True)
        log(r.stdout)
    except Exception as e:
        log(f"[ERRO] {e}")

def run_cache_manager(log, win):
    log("Executando Cache & Temp Manager...")
    win.thread = CacheManagerThread()
    win.thread.log_signal.connect(log)
    win.thread.start()

def run_printer_fixer(log, win):
    log("Executando Printer Fixer...")
    win.thread = PrinterFixerThread()
    win.thread.log_signal.connect(log)
    win.thread.start()

def run_driver_doctor(log, win):
    log("Executando Driver Doctor...")
    win.thread = DriverDoctorThread()
    win.thread.log_signal.connect(log)
    win.thread.start()

def run_evidence_collector(log, win):
    log("Executando Evidence Collector...")
    win.thread = EvidenceCollectorThread()
    win.thread.log_signal.connect(log)
    win.thread.start()

def run_see_evidences(log):
    p = r"C:\Evidencias"
    log(f"Abrindo {p}")
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)
    subprocess.run(f'explorer "{p}"', shell=True)

class SupportToolsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Support Tools – Made by: Santiago")
        self.setGeometry(100, 100, 600, 400)
        self.thread = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        title = QLabel("Support Tools – Made by: Santiago")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        def log(text): self.log_area.append(text)

        btn_machine = QPushButton("Machine Infos")
        btn_machine.clicked.connect(lambda: run_machine_infos(log))
        layout.addWidget(btn_machine)

        btn_cache = QPushButton("Cache & Temp Manager")
        btn_cache.clicked.connect(lambda: run_cache_manager(log, self))
        layout.addWidget(btn_cache)

        btn_printer = QPushButton("Printer Fixer")
        btn_printer.clicked.connect(lambda: run_printer_fixer(log, self))
        layout.addWidget(btn_printer)

        btn_driver = QPushButton("Driver Doctor")
        btn_driver.clicked.connect(lambda: run_driver_doctor(log, self))
        layout.addWidget(btn_driver)

        btn_evidence = QPushButton("Evidence Collector")
        btn_evidence.clicked.connect(lambda: run_evidence_collector(log, self))
        layout.addWidget(btn_evidence)

        btn_see = QPushButton("See Evidences")
        btn_see.clicked.connect(lambda: run_see_evidences(log))
        layout.addWidget(btn_see)

        self.setLayout(layout)

def set_dark_theme(app):
    app.setStyle("Fusion")
    p = QPalette()
    p.setColor(QPalette.Window, QColor(53, 53, 53))
    p.setColor(QPalette.WindowText, Qt.white)
    p.setColor(QPalette.Base, QColor(35, 35, 35))
    p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    p.setColor(QPalette.ToolTipBase, Qt.white)
    p.setColor(QPalette.ToolTipText, Qt.white)
    p.setColor(QPalette.Text, Qt.white)
    p.setColor(QPalette.Button, QColor(53, 53, 53))
    p.setColor(QPalette.ButtonText, Qt.white)
    p.setColor(QPalette.BrightText, Qt.red)
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
