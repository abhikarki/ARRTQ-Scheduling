// round_robin.h
#ifndef ROUND_ROBIN_H
#define ROUND_ROBIN_H

#include <vector>
#include <map>

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int remaining_time;
    int start_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    
    Process(int p, int a, int b) : pid(p), arrival_time(a), burst_time(b), 
                                     remaining_time(b), start_time(-1), 
                                     completion_time(0), turnaround_time(0), 
                                     waiting_time(0) {}
};

struct Metrics {
    double avg_turnaround_time;
    double avg_waiting_time;
    int context_switches;
    int total_context_switch_time;
    int execution_time;
    double throughput;
    double cpu_utilization;
    double context_switch_overhead;
    double avg_first_response_time;
};

Metrics round_robin(std::vector<Process>& processes, int time_quantum, int context_switch_time = 1);

#endif

// round_robin.cpp
#include "round_robin.h"
#include <queue>
#include <algorithm>

using namespace std;

Metrics round_robin(vector<Process>& processes, int time_quantum, int context_switch_time) {
    // Sort by arrival time
    sort(processes.begin(), processes.end(), 
         [](const Process& a, const Process& b) {
             return a.arrival_time < b.arrival_time;
         });
    
    int earliest_arrival_time = processes[0].arrival_time;
    queue<int> ready_queue; // Store process indices
    vector<Process> completed;
    map<int, int> first_response_times;
    
    int idle_time = 0;
    int context_switches = 0;
    int current_time = 0;
    int i = 0;
    int n = processes.size();
    
    while (!ready_queue.empty() || i < n) {
        // Add arrived processes to ready queue
        while (i < n && processes[i].arrival_time <= current_time) {
            ready_queue.push(i);
            i++;
        }
        
        // If queue is empty, jump to next arrival
        if (ready_queue.empty()) {
            if (i < n) {
                idle_time += processes[i].arrival_time - current_time;
                current_time = processes[i].arrival_time;
            }
            continue;
        }
        
        // Get process from ready queue
        int idx = ready_queue.front();
        ready_queue.pop();
        Process& p = processes[idx];
        
        // Set start time if first run
        if (p.start_time == -1) {
            p.start_time = current_time;
            first_response_times[p.pid] = p.start_time - p.arrival_time;
        }
        
        // Run process for time quantum or remaining time
        int runtime = min(p.remaining_time, time_quantum);
        p.remaining_time -= runtime;
        current_time += runtime;
        
        // Add newly arrived processes
        while (i < n && processes[i].arrival_time <= current_time) {
            ready_queue.push(i);
            i++;
        }
        
        // Context switch if more work to do
        if (!ready_queue.empty() || i < n) {
            current_time += context_switch_time;
            context_switches++;
        }
        
        // Add more arrived processes after context switch
        while (i < n && processes[i].arrival_time <= current_time) {
            ready_queue.push(i);
            i++;
        }
        
        // Re-queue or complete process
        if (p.remaining_time > 0) {
            ready_queue.push(idx);
        } else {
            p.completion_time = current_time;
            completed.push_back(p);
        }
    }
    
    // Calculate metrics
    int total_turnaround = 0;
    int total_waiting = 0;
    
    for (auto& p : completed) {
        p.turnaround_time = p.completion_time - p.arrival_time;
        p.waiting_time = p.turnaround_time - p.burst_time;
        total_turnaround += p.turnaround_time;
        total_waiting += p.waiting_time;
    }
    
    int execution_time = current_time - earliest_arrival_time;
    int total_context_switch_time = context_switch_time * context_switches;
    
    double sum_response = 0;
    for (auto& pair : first_response_times) {
        sum_response += pair.second;
    }
    
    Metrics metrics;
    metrics.avg_turnaround_time = (double)total_turnaround / n;
    metrics.avg_waiting_time = (double)total_waiting / n;
    metrics.context_switches = context_switches - 1;
    metrics.total_context_switch_time = total_context_switch_time;
    metrics.execution_time = execution_time;
    metrics.throughput = (double)n / execution_time;
    metrics.cpu_utilization = ((double)(execution_time - idle_time) / execution_time) * 100;
    metrics.context_switch_overhead = ((double)total_context_switch_time / execution_time) * 100;
    metrics.avg_first_response_time = sum_response / first_response_times.size();
    
    return metrics;
}