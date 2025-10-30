from typing import List, Dict
from core.process import Process
from collections import deque

import numpy as np

def arrtq(processes: List[Process], context_switch_time: int = 1) -> Dict:
    #Sort the processes by arrival time for accurate simulation
    processes = sorted(processes, key = lambda p: p.arrival_time)
    earliest_arrival_time = processes[0].arrival_time

    RQ = deque()
    SBTQ = deque()
    LBTQ = deque()
    completed_processes = []

    current_time = 0
    i = 0

    idle_time = 0
    context_switches_count = 0
    total_turnaround_time = 0
    total_waiting_time = 0

    def add_new_arrivals_RQ():
        nonlocal i
        while i < len(processes) and processes[i].arrival_time <= current_time:
            RQ.append(processes[i])
            i += 1

    def run_queue(queue, TQ):
        nonlocal current_time, context_switches_count
        if not queue:
            return
        p = queue.popleft()
        if p.start_time is None:
            p.start_time = current_time
        run_time = min(p.remaining_time, TQ)
        p.remaining_time -= run_time
        current_time += run_time
        add_new_arrivals_RQ()
        if p.remaining_time > 0:
            queue.append(p)
        else:
            p.completion_time = current_time
            completed_processes.append(p)
        if queue or SBTQ or LBTQ or RQ or i < len(processes):
            current_time += context_switch_time
            context_switches_count += 1


    while RQ or SBTQ or LBTQ or i < len(processes):
        # adding new arriving processes to the RQ i.e. Ready Queue
        add_new_arrivals_RQ()
        
        # If the queues are empty, for example, when we are running for the first
        # time, update the time to be the first arriving process time and add process to queue
        if not (RQ or SBTQ or LBTQ):
            if i < len(processes):
                idle_time += processes[i].arrival_time - current_time
                current_time = processes[i].arrival_time     
            continue

        
        if not (SBTQ or LBTQ) and RQ:
            abt_all = np.mean([p.remaining_time for p in RQ])

            while RQ:
                p = RQ.popleft()
                if p.remaining_time >= abt_all:
                    LBTQ.append(p)
                else:
                    SBTQ.append(p)

        while SBTQ and LBTQ:
            abt_lbtq = np.mean([p.remaining_time for p in LBTQ])
            abt_sbtq = np.mean([p.remaining_time for p in SBTQ])
            TQ = (abt_lbtq + abt_sbtq) / 2
            run_queue(LBTQ, TQ)
            run_queue(SBTQ, TQ)
            add_new_arrivals_RQ()
        
        if LBTQ:
            abt_lbtq = np.mean([p.remaining_time for p in LBTQ])
            run_queue(LBTQ, abt_lbtq)
        elif SBTQ:
            abt_sbtq = np.mean([p.remaining_time for p in SBTQ])
            run_queue(SBTQ, abt_sbtq)

        
        if not (LBTQ or SBTQ) and RQ:
            abt_all = np.mean([p.remaining_time for p in RQ])
            while RQ:
                p = RQ.popleft()
                if p.remaining_time >= abt_all:
                    LBTQ.append(p)
                else:
                    SBTQ.append(p)


    for p in completed_processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        total_turnaround_time += p.turnaround_time
        total_waiting_time += p.waiting_time

    n = len(completed_processes)
    execution_time = current_time - earliest_arrival_time
    total_context_switch_time = context_switch_time * context_switches_count
    total_burst_time = sum(p.burst_time for p in processes)

    metrics = {
        "average_turnaround_time" : total_turnaround_time / n,
        "average_waiting_time" : total_waiting_time / n,
        "context_switches": context_switches_count,
        "total_context_switch_time": total_context_switch_time,
        "execution_time": execution_time,
        "throughput": n / execution_time if execution_time > 0 else 0,
        "cpu_utilization": ((execution_time - idle_time) / execution_time * 100) if execution_time > 0 else 0,
        "context_switch_overhead": (total_context_switch_time / execution_time * 100) if execution_time > 0 else 0,
        "completed_processes": completed_processes
    }

    return metrics

        




