import re

# Per-interval TCP / UDP
INTERVAL_PATTERN = re.compile(
    r"\[\s*\d+\]\s+([\d\.]+-[\d\.]+)\s+sec\s+[\d\.]+\s+\w+Bytes\s+([\d\.]+)\s+([MG])bits/sec"
)

# UDP summary
UDP_SUMMARY_PATTERN = re.compile(
    r"\[\s*\d+\]\s+0\.00-[\d\.]+\s+sec\s+[\d\.]+\s+\w+Bytes\s+([\d\.]+)\s+Mbits/sec\s+([\d\.]+)\s+ms\s+(\d+)/(\d+)"
)

# TCP summary (SUM)
TCP_SUMMARY_PATTERN = re.compile(
    r"\[SUM\]\s+0\.00-[\d\.]+\s+sec\s+[\d\.]+\s+\w+Bytes\s+([\d\.]+)\s+([MG])bits/sec"
)


def parse_iperf_line(line: str):
    line = line.strip()

    # ---------- UDP SUMMARY (FINAL) ----------
    udp_sum = UDP_SUMMARY_PATTERN.search(line)
    if udp_sum:
        throughput = float(udp_sum.group(1))
        jitter = float(udp_sum.group(2))
        lost = int(udp_sum.group(3))
        total = int(udp_sum.group(4))
        loss = round((lost / total) * 100, 4) if total else 0.0

        return {
            "throughput": throughput,
            "jitter": jitter,
            "loss": loss,
            "final": True
        }

    # ---------- TCP SUMMARY (FINAL) ----------
    tcp_sum = TCP_SUMMARY_PATTERN.search(line)
    if tcp_sum:
        value = float(tcp_sum.group(1))
        unit = tcp_sum.group(2)
        throughput = value * 1000 if unit == "G" else value

        return {
            "throughput": throughput,
            "jitter": None,
            "loss": None,
            "final": True
        }

    # ---------- PER-INTERVAL ----------
    interval = INTERVAL_PATTERN.search(line)
    if interval:
        value = float(interval.group(2))
        unit = interval.group(3)
        throughput = value * 1000 if unit == "G" else value

        return {
            "throughput": throughput,
            "jitter": None,
            "loss": None,
            "final": False
        }

    return None
