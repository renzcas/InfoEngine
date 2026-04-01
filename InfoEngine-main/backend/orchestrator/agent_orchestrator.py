import time
from backend.organs.agentdash.geometry_loop import run_geometry_cycle


def start_heartbeat(interval: float = 0.5):
    """
    Runs the geometric agent loop forever at a stable interval.
    interval = seconds between ticks (0.5 = 2Hz)
    """
    while True:
        start = time.time()

        snapshot = run_geometry_cycle()

        # Keep the heartbeat stable
        elapsed = time.time() - start
        time.sleep(max(0, interval - elapsed))

        # Optional: print or log the snapshot
        # print(snapshot)
