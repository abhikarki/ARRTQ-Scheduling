# ARRTQ - Adaptive Round Robin with Triple Queue 

This project implements and analyzes scheduling algorithms including:

- Base Round Robin (RR) with fixed time quantum
- Adaptive Round Robin Scheduling with Triple Queues (ARRTQ)
- Balanced ARRTQ (proposed algorithm)

## Current Progress  (Balanced ARRTQ shows imporovement in Avg. FRT (Average First Response Time)

| Algorithm | Dataset | Avg. TAT | Avg. WT | Avg. FRT | CPU Util (%) | Ctx Switches | throughput |
|------------|----------|----------|----------|-----------|---------------|---------------|---------------|
| Round Robin | 1000 proc | 8660 | 8649 | ___ | 99.99 | 4049 | ___ |
| ARRTQ | 1000 proc | 5626 | 5615 | 4282 | 99.98| 2124 | 0.0754 |
| Balanced ARRTQ | 1000 proc | 5831 | 5820 | 3295 | 99.98 | 2078 | 0.0756 |


## Approach for Balanced ARRTQ
The Balanced ARRTQ (proposed algorithm) improves the original ARRTQ by dynamically deciding how many new processes from the Ready Queue(RQ) should be admitted into the active queues(SBTQ-Small Burst Time Queue and LBTQ-Large Burst Time Queue). Instead of waiting until both SBTQ and LBTQ are empty (original ARRTQ approach), the scheduler continuously adds some processes from RQ into active queues based on the following admission factor: 

<h2 align = "center">
$$\gamma = \frac{L_{RQ}}{L_{RQ} + c\ * L_{A} + 1}$$  
</h2>
**Where**

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
