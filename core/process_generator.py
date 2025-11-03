import random
from core.process import Process

# Generate synthetic processes
def generate_processes(n: int, seed: int = 42, arrival_rate: float = 3.0, burst_min: int = 2, burst_max: int = 20):
    random.seed(seed)
    processes = []
    current_arrival = 0

    for pid in range(1, n + 1):
        # Inter-arrival time (can be exponential for realism)
        inter_arrival = random.expovariate(1 / arrival_rate)
        current_arrival += int(inter_arrival)

        burst_time = random.randint(burst_min, burst_max)
        processes.append(Process(pid=pid, arrival_time=current_arrival, burst_time=burst_time))

    return processes
