from typing import List, Dict
from core.process import Process
from collections import deque

def round_robin(processes: List[Process], time_quantum: int, context_switch_time: int = 1) -> Dict:
    # Sort the processes by arrival time for accurate simulation
    processes = sorted(processes, key=lambda p: p.arrival_time)

    earliest_arrival_time = processes[0].arrival_time
    # This will be our ready_queue for the scheduler and dispatcher to work
    ready_queue = deque()
    
    # Tracking completed processes
    completed_processes = []

    # some metrics we track to analyze the performance
    idle_time = 0
    context_switches_count = 0
    total_turnaround_time = 0
    total_waiting_time = 0

    # Variable for simulating the clock
    current_time = 0

    # variable for simulating incoming processes from the sorted list
    i = 0

    rq_length_over_time = []
    first_response_times = {}

    while ready_queue or i < len(processes):
        # Simulate by adding processes to the ready queue by arrival time
        while(i < len(processes) and processes[i].arrival_time <= current_time):
            ready_queue.append(processes[i])
            # calculating total burst_time as we add new processes
            i += 1
        
        rq_length_over_time.append((current_time, len(ready_queue)))
    
        # So, if the queue is empty, for example, when we are in first iteration
        # our time starts as 0 and so nothing is added to we will change the time to the 
        # next arriving process time, simulating that amount of time passed 
        # this is a idle time for the cpu
        if not ready_queue:
            if i < len(processes):
                idle_time += processes[i].arrival_time - current_time
                current_time = processes[i].arrival_time
            continue

        # take the process 
        p = ready_queue.popleft()

        # we will set its start time if it running for the first time and also the first_response_time
        if p.start_time is None:
            p.start_time = current_time
            first_response_times[p.pid] = p.start_time - p.arrival_time
        
        # simulating that the process ran for either time_quantum time or its whole thing if 
        # remaining time is less than the burst time
        p_runtime = min(p.remaining_time, time_quantum)
        p.remaining_time -= p_runtime
        # updating our time to reflect the passing of time
        current_time += p_runtime

        # As the process was running, new processes could have arrived,
        # so adding them from the list
        while i < len(processes) and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i += 1

        # The code below seems redundant and logically we could merge the time passage of runtime
        # and context switch into one, but here, we chose to separate it so that the passage of time
        # is little more visible

        # Simulating small time passage for context_switch
        if ready_queue or i < len(processes):
            current_time += context_switch_time
            context_switches_count += 1

        # Note that we take into account context_switch_time but as that time passed,
        # more processes could have arrived though context_switch time is small
        while i < len(processes) and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i +=1

        rq_length_over_time.append((current_time, len(ready_queue)))

        # add to end of queue if process didnot finish
        if(p.remaining_time > 0):
            ready_queue.append(p)
        else:
            # process finished so we donot add back
            p.completion_time = current_time
            completed_processes.append(p)

    
    for process in completed_processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        total_turnaround_time += process.turnaround_time
        total_waiting_time += process.waiting_time
    
    n = len(completed_processes)

    # calculate execution time.
    execution_time = current_time - earliest_arrival_time
    total_context_switch_time = context_switch_time * context_switches_count
    
    # Calculate all metrics
    metrics = {
        "average_turnaround_time": total_turnaround_time / n,
        "average_waiting_time": total_waiting_time / n,
        "context_switches": context_switches_count - 1,  # last switch isn't needed
        "total_context_switch_time": total_context_switch_time,
        "execution_time": execution_time,  # Time taken after all processes arrived
        "throughput": n / execution_time if execution_time > 0 else 0,  # Processes per time
        "cpu_utilization": ((execution_time - idle_time) / execution_time * 100) if execution_time > 0 else 0,  
        "context_switch_overhead": (total_context_switch_time / execution_time * 100) if execution_time > 0 else 0,  # Percentage of execution time spent in context switching
        "completed_processes": completed_processes,
        "first_response_times": first_response_times,
        "average_first_response_time":(
            sum(first_response_times.values()) / len(first_response_times)
            if first_response_times else 0
        ),
        "rq_length_over_time": rq_length_over_time,
    }
    
    return metrics