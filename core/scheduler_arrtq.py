from typing import List, Dict
from core.process import Process
from collections import deque

import numpy as np

def arrtq(processes: List[Process], context_switch_time: int = 1) -> Dict:
    #Sort the processes by arrival time for accurate simulation
    processes = sorted(processes, key = lambda p: p.arrival_time)
    earliest_arrival_time = processes[0].arrival_time

    # Three queues as in the paper
    RQ = deque()
    SBTQ = deque()
    LBTQ = deque()
    completed_processes = []

    # variable for simulating the clock
    current_time = 0
    # variable for simulating incoming processes from the sorted list
    i = 0

    # some metrics we track to analyze the performance
    idle_time = 0
    context_switches_count = 0
    total_turnaround_time = 0
    total_waiting_time = 0

    # to track the accumulation on Ready Queue
    rq_length_over_time = []
    # first response time
    first_response_times = {}

    # To add the newly arriving processes to the Ready Queue as the rest of the algorithm keeps running for LBTQ and SBTQ
    def add_new_arrivals_RQ():
        nonlocal i
        # simulate the arrival of new processes by adding them to the Ready Queue
        while i < len(processes) and processes[i].arrival_time <= current_time:
            RQ.append(processes[i])
            i += 1
        rq_length_over_time.append((current_time, len(RQ)))


    # This method runs the individual queue, either the LBTQ or SBTQ once for the current time quantum
    # it only runs for one time quantum and returns since the algorithm has to switch continuously between LBTQ and SBTQ
    # with each time quantum
    def run_queue(queue, TQ):
        nonlocal current_time, context_switches_count

        if not queue:
            return
        
        p = queue.popleft()
        # if this process running for first time, set the start_time and first response time
        if p.start_time is None:
            p.start_time = current_time
            first_response_times[p.pid] = p.start_time - p.arrival_time


        run_time = min(p.remaining_time, TQ)
        p.remaining_time -= run_time
        current_time += run_time

        # since we updated the current_time (our clock) more processes might have arrived to the Ready Queue, so we simulate that
        add_new_arrivals_RQ()

        if p.remaining_time > 0:
            queue.append(p)
        else:
            p.completion_time = current_time
            completed_processes.append(p)
        if queue or SBTQ or LBTQ or RQ or i < len(processes):    # donot account for context switch if it is last process
            current_time += context_switch_time
            context_switches_count += 1


    # The algorithm starts
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


        # if both the SBTQ and LBTQ are empty, we take the processes in the ready queue and divide them into SBTQ and LBTQ
        if not (SBTQ or LBTQ) and RQ:
            # average burst time of all processes currently ready in Ready Queue
            abt_all = np.mean([p.remaining_time for p in RQ])

            # Divide them into LBTQ and SBTQ. If burst time < average burst time, SBTQ(Small Burst Time Queue), else LBTQ(Large Burst Time Queue)
            while RQ:
                p = RQ.popleft()
                if p.remaining_time >= abt_all:
                    LBTQ.append(p)
                else:
                    SBTQ.append(p)

        # Then, we keep switching between the process from SBTQ and LBTQ until both are empty
        while SBTQ and LBTQ:
            abt_lbtq = np.mean([p.remaining_time for p in LBTQ])
            abt_sbtq = np.mean([p.remaining_time for p in SBTQ])
            TQ = (abt_lbtq + abt_sbtq) / 2
            run_queue(LBTQ, TQ)
            run_queue(SBTQ, TQ)
            run_queue(SBTQ, TQ)

            # as we run the processes from LBTQ and SBTQ, the time passes and more processes can arrive in Ready Queue, so we simulate that
            add_new_arrivals_RQ()
        
        # remaining from LBTQ or SBTQ
        if LBTQ:
            abt_lbtq = np.mean([p.remaining_time for p in LBTQ])
            run_queue(LBTQ, abt_lbtq)
        elif SBTQ:
            abt_sbtq = np.mean([p.remaining_time for p in SBTQ])
            run_queue(SBTQ, abt_sbtq)

        # Once we are done and both LBTQ and SBTQ are empty, we again repeat by dividing the ready processes in Ready Queue to SBTQ and LBTQ
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
        "completed_processes": completed_processes,
        "first_response_times": first_response_times,
        "average_first_response_time": np.mean(list(first_response_times.values())) if first_response_times else 0,
        "rq_length_over_time": rq_length_over_time,
    }

    return metrics