from typing import List, Dict
from core.process import Process
from collections import deque

def round_robin(processes: List[Process], time_quantum: int, context_switch_time: int = 1) -> Dict:
    # Find the last arrival time
    last_arrival_time = 0
    total_burst_time = 0

    # Create ready queue with processes
    ready_queue = deque()
    for p in processes:
        process = Process(p.pid, p.burst_time, p.arrival_time)
        total_burst_time += p.burst_time
        ready_queue.append(process)
        last_arrival_time = p.arrival_time    # the input is in increasing order of arrival_time, so take last value
    
    # Start simulation clock after last arrival
    current_time = last_arrival_time
    completed_processes = []
    context_switches = 0
    total_context_switch_time = 0  # Track total time spent in context switching
    
    while ready_queue:
        current_process = ready_queue.popleft()
        
        # If this is the first time process is running, set its start time
        if current_process.start_time is None:
            current_process.start_time = current_time
        
        # Calculate how much time this process will run
        execution_time = min(time_quantum, current_process.remaining_time)
        
        # Update simulated clock and process's remaining time
        current_time += execution_time
        current_process.remaining_time -= execution_time
        
        # If process is not completed, add it back to queue
        if current_process.remaining_time > 0:
            # Add context switch overhead
            current_time += context_switch_time
            total_context_switch_time += context_switch_time
            ready_queue.append(current_process)
            context_switches += 1
        else:
            # Add context switch overhead
            current_time += context_switch_time
            total_context_switch_time += context_switch_time
            current_process.completion_time = current_time
            completed_processes.append(current_process)
            context_switches += 1
    
    total_turnaround_time = 0
    total_waiting_time = 0
    
    for process in completed_processes:
        turnaround_time = process.completion_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
    
    n = len(completed_processes)
    
    # Calculate execution time (total time spent after last arrival)
    execution_time = current_time - last_arrival_time
    
    # Calculate all metrics
    metrics = {
        "average_turnaround_time": total_turnaround_time / n,
        "average_waiting_time": total_waiting_time / n,
        "context_switches": context_switches - 1,  # last switch isn't needed
        "total_context_switch_time": total_context_switch_time,
        "execution_time": execution_time,  # Time taken after all processes arrived
        "throughput": n / execution_time if execution_time > 0 else 0,  # Processes per time
        "cpu_utilization": (total_burst_time / execution_time * 100) if execution_time > 0 else 0,  
        "context_switch_overhead": (total_context_switch_time / execution_time * 100) if execution_time > 0 else 0,  # Percentage of execution time spent in context switching
        "completed_processes": completed_processes
    }
    
    return metrics