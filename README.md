# Background: CPU Scheduling

CPU scheduling determines which process gets to run on the CPU and when, with the goal of optimizing overall system performance.

### Key Objectives
A good scheduler aims to: <br>
Minimize
* Turnaround Time (TAT) – total time from process submission to completion
* Waiting Time (WT) – time a process spends waiting in the ready queue
* Response Time – time until the process first gets the CPU

Maximize
* CPU Utilization – percentage of time CPU is actively executing
* Throughput – number of processes completed per unit time

### Classical Round Robin (RR)
Round Robin is one of the most widely used preemptive scheduling algorithms.
In Round Robin, Each process is assigned a fixed Time Quantum (TQ) and each process executes for at most one TQ. If unfinished, it moves to the back of the ready queue. This ensures fairness since every process receives equal CPU slices.

### Limitations of RR
Despite its simplicity, fixed-quantum RR suffers from:
*High context-switch overhead when TQ is too small→ CPU spends more time switching than executing

* Poor responsiveness when TQ is too large
→ Processes wait longer before getting CPU time

* No adaptation to burst-time characteristics
→ Both short and long processes are treated the same


# ARRTQ - Adaptive Round Robin with Triple Queue 

This project implements and analyzes scheduling algorithms including:

- Base Round Robin (RR) with fixed time quantum
- Adaptive Round Robin Scheduling with Triple Queues (ARRTQ)
- Balanced ARRTQ (proposed algorithm)

## Current Progress - Balanced ARRTQ shows improvement in Avg. FRT (Average First Response Time)

| Algorithm | Dataset | Avg. TAT | Avg. WT | Avg. FRT | CPU Util (%) | Context Switches | throughput |
|------------|----------|----------|----------|-----------|---------------|---------------|---------------|
| ARRTQ | 10000 processes | 58942 | 58931 | 38715 |99.99| 21342 |0.07576  |
| Balanced ARRTQ | 10000 processes | 58296 | 58285 | 32871 (15% reduction) |99.99| 20496 | 0.076253|
| ARRTQ | 5000 processes | 28493 | 28482 | 21785 |99.99| 10748 | 0.075571|
| Balanced ARRTQ | 5000 processes | 28992 | 28981 | 16270 (25% reduction) |99.99| 10264 | 0.076128|





## Proposed Balanced ARRTQ Approach
The Balanced ARRTQ (proposed algorithm) improves the original ARRTQ by dynamically deciding how many new processes from the Ready Queue(RQ) should be admitted into the active queues(SBTQ-Small Burst Time Queue and LBTQ-Large Burst Time Queue). Instead of waiting until both SBTQ and LBTQ are empty (original ARRTQ approach), the scheduler continuously adds some processes from RQ into active queues based on the following admission factor: 

<h2 align = "center">
$$\gamma = \frac{L_{RQ}}{L_{RQ} + c\ * L_{A} + 1}$$  
</h2>
Where

- $L_{RQ}$ — Number of processes currently waiting in the Ready Queue.
- $L_{A}$ = |SBTQ| + |LBTQ| — Total number of active processes.
- c — Control parameter balancing First Response Time (FRT) and Turnaround Time (TAT).
  - Smaller c → more aggressive admission from RQ to active queues → lower FRT.
  - Larger c → more conservative admission from RQ to active queues → lower TAT.
- $\\gamma\$ — Admission fraction.


<h2 align = "center">
$m = \max\{1,\ \lfloor \gamma \cdot L_{RQ} \rfloor\}$
</h2>
where 'm' is the number of processes to be added from RQ to active queues. 

## Metrics Comparision for different datasets

### 1. Balanced ARRTQ shows improvement in Average First Response Time
<img width="1717" height="525" alt="Screenshot (85)" src="https://github.com/user-attachments/assets/8ce03ed4-ead2-43ec-931c-15793eb1ac05" />

### 2. Balanced ARRTQ shows similar performance in Average TurnAround Time with ARRTQ (meaning no tradeoff of turnaround time for better first response time)
<img width="1742" height="550" alt="Screenshot (86)" src="https://github.com/user-attachments/assets/765f7433-bc5b-4e7a-af1d-6078ac8dd69d" />

### 3. No tradeoff in waiting times
<img width="1729" height="546" alt="Screenshot (87)" src="https://github.com/user-attachments/assets/7a4d454c-6cdb-47ee-8acd-0bfedbf3dc7c" />

### 4. Similar or Better performance in Number of Context switches
<img width="1737" height="546" alt="Screenshot (89)" src="https://github.com/user-attachments/assets/4cacd3f4-2c3e-480e-9210-f26382ba386e" />






## Project Structure

```
ARRTQ/
├── core/               # Core implementation of scheduling algorithms
│   ├── __init__.py
│   ├── metrics.py     # Performance metrics calculations
│   ├── process.py     # Process class definition
│   ├── scheduler_rr.py # Base Round Robin implementation
│   └── scheduler_arrtq.py # ARRTQ implementation
│   ├── scheduler_modified_ARRTQ.py     # proposed modified ARRTQ Algorithm
│   ├── process_generator.py     # generate datasets


├── notebooks/         # Jupyter notebooks for visualization and analysis
└── requirements.txt   # Python dependencies
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The project includes Jupyter notebooks demonstrating the algorithms:

- `notebooks/demo_baseRR.ipynb`: Demonstrates base Round Robin scheduling
- `notebooks/demo_baseARRTQ.ipynb`: Demonstrates base ARRTQ scheduling, also the resulting metrics show that it performs better than the base Round Robin scheduling(compare with previous notebook results)
- `notebooks/compare_baseRR_ARRTQ_modifiedARRTQ.ipynb`: Compares all three algorithms(base Round Robin, ARRTQ, modified ARRTQ) 

## Features

- Process scheduling simulation
- Performance metrics calculation:
  - Average Turnaround Time
  - Average Waiting Time
  - First Response Times & Average First Response Time
  - CPU Utilization
  - Context Switch Overhead
- Visualization of scheduling results
