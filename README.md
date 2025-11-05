# ARRTQ - Adaptive Round Robin with Triple Queue 

This project implements and analyzes scheduling algorithms including:

- Base Round Robin (RR) with fixed time quantum
- Adaptive Round Robin Scheduling with Triple Queues (ARRTQ)
- Modified ARRTQ (proposed algorithm)

## Current Progress

| Algorithm | Dataset | Avg. TAT | Avg. WT | Avg. FRT | CPU Util (%) | Ctx Switches | throughput |
|------------|----------|----------|----------|-----------|---------------|---------------|---------------|
| Round Robin | 1000 proc | 8660 | 8649 | ___ | 99.99 | 4049 | ___ |
| ARRTQ | 1000 proc | 5626 | 5615 | 4282 | 99.98| 2124 | 0.0754 |
| Balanced ARRTQ | 1000 proc | 5831 | 5820 | 3295 | 99.98 | 2078 | 0.0756 |

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
