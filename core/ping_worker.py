import subprocess
import threading


class PingWorker(threading.Thread):
    def __init__(self, target, on_output):
        super().__init__(daemon=True)
        self.target = target
        self.on_output = on_output

    def run(self):
        try:
            cmd = ["ping", "-n", "4", self.target]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.on_output(line.rstrip())

        except Exception as e:
            self.on_output(f"[ERROR] Ping failed: {e}")
