import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.iperf_worker_FINAL import IperfWorker


def start_test(ui):
    worker = IperfWorker(
        server=ui.server_ip(),
        client_bind=ui.client_bind_ip(),
        protocol=ui.protocol(),
        duration=ui.duration(),
        parallel=ui.parallel_streams()
    )

    ui.worker = worker
    worker.output.connect(ui.on_iperf_output)
    worker.finished.connect(ui.on_test_finished)
    worker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
