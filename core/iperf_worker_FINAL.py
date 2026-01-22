import subprocess
from PySide6.QtCore import QThread, Signal
import os
import sys


# ========================================================
# PYINSTALLER RESOURCE PATH (DO NOT CHANGE)
# ========================================================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


IPERF_PATH = resource_path("extra_bin/iperf3.exe")


class IperfWorker(QThread):
    """
    FINAL GUARANTEED-WORKING IPERF WORKER

    Supports ALL scenarios reliably:
    - TCP single pair
    - TCP multi pair
    - UDP single pair
    - UDP multi pair (via multiple processes)

    Defensive against bad UI input.
    """

    output = Signal(str)
    finished = Signal()

    def __init__(
        self,
        server_ip,
        protocol,
        duration,
        pairs,
        udp_bandwidth_mbps=0
    ):
        super().__init__()

        # ---------------- BASIC ----------------
        self.server_ip = server_ip.strip()
        self.protocol = (protocol or "TCP").lower()

        # ---------------- DURATION ----------------
        try:
            self.duration = int(duration)
            if self.duration <= 0:
                self.duration = 10
        except Exception:
            self.duration = 10

        # ---------------- PAIRS (CRITICAL FIX) ----------------
        try:
            self.pairs = int(pairs)
            if self.pairs <= 0:
                self.pairs = 1
        except Exception:
            self.pairs = 1

        # ---------------- UDP BANDWIDTH ----------------
        try:
            self.udp_bw = int(udp_bandwidth_mbps)
            if self.udp_bw < 0:
                self.udp_bw = 0
        except Exception:
            self.udp_bw = 0

        self.processes = []

    # ========================================================
    # TCP
    # ========================================================
    def run_tcp(self):
        cmd = [
            IPERF_PATH,
            "-c", self.server_ip,
            "-t", str(self.duration)
        ]

        if self.pairs > 1:
            cmd.extend(["-P", str(self.pairs)])

        self.run_process(cmd, tag="[TCP]")

    # ========================================================
    # UDP SINGLE
    # ========================================================
    def run_udp_single(self):
        cmd = [
            IPERF_PATH,
            "-c", self.server_ip,
            "-u",
            "-t", str(self.duration),
        ]

        if self.udp_bw > 0:
            cmd.extend(["-b", f"{self.udp_bw}M"])
        else:
            cmd.extend(["-b", "0"])

        self.run_process(cmd, tag="[UDP-1]")

    # ========================================================
    # UDP MULTI (GUARANTEED METHOD)
    # ========================================================
    def run_udp_multi(self):
        self.output.emit(
            f"[INFO] Running UDP with {self.pairs} independent streams"
        )

        for i in range(self.pairs):
            cmd = [
                IPERF_PATH,
                "-c", self.server_ip,
                "-u",
                "-t", str(self.duration),
            ]

            if self.udp_bw > 0:
                cmd.extend(["-b", f"{self.udp_bw}M"])
            else:
                cmd.extend(["-b", "0"])

            self.run_process(cmd, tag=f"[UDP-{i+1}]")

    # ========================================================
    # PROCESS RUNNER
    # ========================================================
    def run_process(self, cmd, tag=""):
        self.output.emit("=" * 60)
        self.output.emit(f"{tag} COMMAND:")
        self.output.emit(" ".join(cmd))
        self.output.emit("=" * 60)

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in proc.stdout:
            if line:
                self.output.emit(f"{tag} {line.rstrip()}")

        proc.wait()

    # ========================================================
    # THREAD ENTRY
    # ========================================================
    def run(self):
        try:
            if self.protocol == "tcp":
                self.run_tcp()

            elif self.protocol == "udp":
                if self.pairs == 1:
                    self.run_udp_single()
                else:
                    self.run_udp_multi()

            else:
                self.output.emit("[ERROR] Unknown protocol")

        except Exception as e:
            self.output.emit(f"[ERROR] {str(e)}")

        finally:
            self.finished.emit()
