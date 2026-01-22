import csv
from datetime import datetime

def export_csv(samples):
    if not samples:
        return

    filename = f"iperf_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["throughput", "jitter", "loss"]
        )
        writer.writeheader()
        for s in samples:
            writer.writerow(s)
