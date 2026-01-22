from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFrame
)
from PySide6.QtCore import Qt

from core.iperf_worker_FINAL import IperfWorker
from core.ping_worker import PingWorker
from core.parser import parse_iperf_line

from utils.exporter import export_csv


# ================= STYLES =================

BTN_PRIMARY = """
QPushButton {
    background-color:#2563eb;
    color:white;
    border-radius:10px;
    padding:10px;
    font-weight:600;
}
QPushButton:hover { background-color:#1d4ed8; }
QPushButton:pressed { background-color:#1e40af; }
"""

BTN_SECONDARY = """
QPushButton {
    background-color:#0f172a;
    color:#e5e7eb;
    border:1px solid #334155;
    border-radius:10px;
    padding:10px;
}
QPushButton:hover { border:1px solid #60a5fa; }
"""

INPUT_STYLE = """
QLineEdit, QComboBox {
    background-color:#0f172a;
    border:1px solid #334155;
    border-radius:8px;
    padding:8px;
}
"""


# ================= MAIN WINDOW =================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPerf Tool – Network Engineering")
        self.resize(1450, 820)

        self.samples = []
        self.worker = None

        root = QWidget()
        root.setStyleSheet("background:#020617;color:#e5e7eb;")
        main = QHBoxLayout(root)

        # ========== SIDEBAR ==========
        side = QVBoxLayout()
        side.setSpacing(12)

        self.server = QLineEdit()
        self.server.setPlaceholderText("Server IP (Target)")
        self.server.setStyleSheet(INPUT_STYLE)

        self.protocol = QComboBox()
        self.protocol.addItems(["TCP", "UDP"])
        self.protocol.setStyleSheet(INPUT_STYLE)

        self.duration = QLineEdit("10")
        self.duration.setStyleSheet(INPUT_STYLE)

        # 🔑 IMPORTANT: default pairs = 1
        self.parallel = QLineEdit("1")
        self.parallel.setStyleSheet(INPUT_STYLE)

        self.ping_btn = QPushButton("📡 Ping Test")
        self.ping_btn.setStyleSheet(BTN_SECONDARY)

        self.start_btn = QPushButton("⚡ Start iPerf Test")
        self.start_btn.setStyleSheet(BTN_PRIMARY)

        self.stop_btn = QPushButton("🛑 Stop Test")
        self.stop_btn.setStyleSheet(BTN_SECONDARY)
        self.stop_btn.setEnabled(False)

        self.export_btn = QPushButton("Export CSV")
        self.export_btn.setStyleSheet(BTN_SECONDARY)

        for w in [
            QLabel("Server IP"), self.server,
            QLabel("Protocol"), self.protocol,
            QLabel("Duration (s)"), self.duration,
            QLabel("Parallel Streams"), self.parallel,
            self.ping_btn,
            self.start_btn,
            self.stop_btn,
            self.export_btn
        ]:
            side.addWidget(w)

        side.addStretch()

        # ========== MAIN CONTENT ==========
        content = QVBoxLayout()

        title = QLabel("Performance Dashboard")
        title.setStyleSheet("font-size:22px;font-weight:600;")
        content.addWidget(title)

        # KPI CARDS
        self.throughput = QLabel("0.00 Mbps")
        self.jitter = QLabel("N/A")
        self.loss = QLabel("N/A")

        kpi_layout = QHBoxLayout()
        for name, lbl in [
            ("Throughput", self.throughput),
            ("Jitter", self.jitter),
            ("Packet Loss", self.loss)
        ]:
            frame = QFrame()
            frame.setStyleSheet(
                "background:#020617;border:1px solid #1e293b;"
                "border-radius:12px;padding:16px;"
            )
            v = QVBoxLayout(frame)
            v.addWidget(QLabel(name.upper()))
            v.addWidget(lbl)
            kpi_layout.addWidget(frame)

        content.addLayout(kpi_layout)

        # GRAPH
        self.figure = Figure(facecolor="#020617")
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self._init_graph()
        content.addWidget(self.canvas, 1)

        # TERMINAL
        terminal_frame = QFrame()
        terminal_frame.setStyleSheet(
            "background:#020617;border:1px solid #1e293b;border-radius:12px;"
        )
        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.addWidget(QLabel("SYSTEM OUTPUT"))

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(
            "background:#020617;border:none;color:#e5e7eb;"
            "font-family:Consolas;font-size:12px;"
        )
        terminal_layout.addWidget(self.console)
        content.addWidget(terminal_frame, 1)

        main.addLayout(side, 1)
        main.addLayout(content, 4)
        self.setCentralWidget(root)

        # ACTIONS
        self.start_btn.clicked.connect(self.start_test)
        self.stop_btn.clicked.connect(self.stop_test)
        self.ping_btn.clicked.connect(self.ping_test)
        self.export_btn.clicked.connect(lambda: export_csv(self.samples))

    # ================= GRAPH =================

    def _init_graph(self):
        self.ax.clear()
        self.ax.set_facecolor("#020617")
        self.ax.set_title("Throughput vs Time", color="white")
        self.ax.set_xlabel("Time (seconds)", color="white")
        self.ax.set_ylabel("Throughput (Mbps)", color="white")
        self.ax.grid(True, color="#1e293b")
        self.ax.tick_params(colors="white")
        self.canvas.draw_idle()

    # ================= ACTIONS =================

    def ping_test(self):
        server_ip = self.server.text().strip()
        if not server_ip:
            self.console.append("[ERROR] Server IP required for ping.")
            return

        self.console.append("\n--- PING TEST ---")
        PingWorker(server_ip, self.console.append).start()

    def start_test(self):
        server_ip = self.server.text().strip()
        if not server_ip:
            self.console.append("[ERROR] Server IP is required.")
            return

        if self.worker:
            self.console.append("[INFO] Test already running.")
            return

        # -------- Parse inputs safely --------
        protocol = self.protocol.currentText()
        duration = int(self.duration.text().strip() or 10)

        pairs_raw = int(self.parallel.text().strip() or 1)
        pairs = None if pairs_raw == 1 else pairs_raw

        self.samples.clear()
        self._init_graph()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.console.append("\n--- IPERF TEST STARTED ---")

        # 🔑 EXPLICIT, CORRECT CALL
        self.worker = IperfWorker(
            server_ip,
            protocol,
            duration,
            pairs
        )

        self.worker.output.connect(self.on_output)
        self.worker.finished.connect(self.on_test_finished)
        self.worker.start()

    def stop_test(self):
        if self.worker:
            self.console.append("[INFO] Test stopped by user.")
            self.worker.terminate()
            self.worker = None

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def on_test_finished(self):
        self.console.append("[INFO] Test completed.")
        self.worker = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def on_output(self, line):
        self.console.append(line)

        parsed = parse_iperf_line(line)
        if not parsed:
            return

        self.samples.append(parsed)

        # KPI UPDATE
        self.throughput.setText(f"{parsed['throughput']:.2f} Mbps")

        self.jitter.setText(
            f"{parsed['jitter']} ms" if parsed["jitter"] is not None else "N/A"
        )
        self.loss.setText(
            f"{parsed['loss']} %" if parsed["loss"] is not None else "N/A"
        )

        # GRAPH UPDATE
        x = list(range(1, len(self.samples) + 1))
        y = [s["throughput"] for s in self.samples]

        self.ax.clear()
        self.ax.set_facecolor("#020617")
        self.ax.set_title("Throughput vs Time", color="white")
        self.ax.set_xlabel("Time (seconds)", color="white")
        self.ax.set_ylabel("Throughput (Mbps)", color="white")
        self.ax.grid(True, color="#1e293b")
        self.ax.tick_params(colors="white")

        self.ax.plot(x, y, color="#3b82f6", marker="o")
        self.ax.set_ylim(0, max(y) * 1.2)

        self.canvas.draw_idle()
