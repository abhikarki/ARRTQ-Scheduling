#include "process.h"
#include <vector>
#include <deque>
#include <map>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <iostream>

struct RRSchedulingMetrics{
    double average_turnaround_time = 0.0;
    double average_waiting_time = 0.0;
    int context_switches = 0;
    int total_context_switch_time = 0;
    int execution_time = 0;
    double throughput = 0.0;
    double cpu_utilization = 0.0;
    double context_switch_overhead = 0.0;
    std::vector<Process> completed_processes;
    std::map<std::string, int> first_response_times;
    double average_first_response_time = 0.0;
    std::vector<std::pair<int, int>> rq_length_over_time;
};

RRSchedulingMetrics round_robin(std::vector<Process>& processes, int time_quantum, int context_switch_time = 1){
    // sort the processes by arrival time for accurate simulation
    std::sort(processes.begin(), processes.end(), [](const Process& a, const Process&  b){
        return a.arrival_time < b.arrival_time;
    });

    if(processes.empty()){
        return RRSchedulingMetrics();
    }

    // This will be our ready_queue for the scheduler and dispatcher to work
    std::deque<Process*> ready_queue;

    RRSchedulingMetrics metrics;

    int earliest_arrival_time = processes[0].arrival_time;

    // some metrics we track to analyze the performance
    int idle_time = 0;
    int context_switches_count = 0;

    // Variable for simulating the clock
    int current_time = 0;

    // variable for simulating incoming processes from the sorted list
    int i = 0;

    while(!ready_queue.empty() || i < processes.size()){
        // adding processes to the ready queue by arrival time
        while(i < processes.size() && processes[i].arrival_time <= current_time){
            ready_queue.push_back(&processes[i]);
            i++;
        }

        metrics.rq_length_over_time.push_back({current_time, (int)ready_queue.size()});

        // passing of time till next process
        if(ready_queue.empty()){
            if(i < processes.size()){
            idle_time += processes[i].arrival_time - current_time;
            current_time = processes[i].arrival_time;
            }

            if(i == processes.size() && ready_queue.empty()) break;
            continue;
        }

        Process* p = ready_queue.front();
        ready_queue.pop_front();

        // set start time
        if(!p->start_time.has_value()){
            p->start_time = current_time;
            metrics.first_response_times[p->pid] = p->start_time.value() - p->arrival_time;
        }

        // run for time quantum or whole burst time
        int p_runtime = std::min(p->remaining_time.value(), time_quantum);
        p->remaining_time = p->remaining_time.value() - p_runtime;
        // update time
        current_time += p_runtime;

        // add new processes to ready queue.
        while(i < processes.size() && processes[i].arrival_time <= current_time){
            ready_queue.push_back(&processes[i]);
            i++;
        }

        // context switch
        if(!ready_queue.empty() || (p->remaining_time.value() > 0 && ready_queue.size() > 0)){
            current_time += context_switch_time;
            context_switches_count++;
        }

        while(i < processes.size() && processes[i].arrival_time <= current_time){
            ready_queue.push_back(&processes[i]);
            i++;
        }
        

        metrics.rq_length_over_time.push_back({current_time, (int)ready_queue.size()});

        // add the process to the end if not finished 
        if(p->remaining_time.value() > 0){
            ready_queue.push_back(p);
        }
        else{
            // process finished execution completely
            p->completion_time = current_time;
            metrics.completed_processes.push_back(*p);
        }
    }

    double total_turnaround_time = 0.0;
    double total_waiting_time = 0.0;

    for(Process& process : metrics.completed_processes){
        process.turnaround_time = process.completion_time.value() - process.arrival_time;
        process.waiting_time = process.turnaround_time.value() - process.burst_time;

        total_turnaround_time += process.turnaround_time.value();
        total_waiting_time += process.waiting_time.value();
    }


    int n = metrics.completed_processes.size();

    if(n > 0){
        metrics.average_turnaround_time = total_turnaround_time / n;
        metrics.average_waiting_time = total_waiting_time / n;
    }

    int total_burst_time = std::accumulate(
        processes.begin(), processes.end(), 0,
        [](int sum, const Process& p) {return sum + p.burst_time;}
    );

    metrics.execution_time = current_time - earliest_arrival_time;

    metrics.total_context_switch_time = context_switch_time * context_switches_count;
    metrics.context_switches = std::max(0, context_switches_count - 1);

    if(metrics.execution_time > 0){
        metrics.throughput = (double)n / metrics.execution_time;
        metrics.cpu_utilization = ((double)(metrics.execution_time - idle_time) / metrics.execution_time) * 100.0;
    }

    if(!metrics.first_response_times.empty()){
        double total_first_response_time = 0.0;
        for(const auto& pair : metrics.first_response_times){
            total_first_response_time += pair.second;
        }
        metrics.average_first_response_time = total_first_response_time / metrics.first_response_times.size();
    }

    return metrics;
}


