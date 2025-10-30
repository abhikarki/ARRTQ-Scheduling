# ARRTQ - Adaptive Round Robin with Time Quantum

This project implements and analyzes scheduling algorithms including:

- Base Round Robin (RR) with fixed time quantum
- Adaptive Round Robin Scheduling with Triple Queues (ARRTQ)

## Project Structure

```
ARRTQ/
├── core/               # Core implementation of scheduling algorithms
│   ├── __init__.py
│   ├── metrics.py     # Performance metrics calculations
│   ├── process.py     # Process class definition
│   ├── scheduler_rr.py # Base Round Robin implementation
│   └── scheduler_arrtq.py # ARRTQ implementation
├── data/              # Data files and test cases
├── notebooks/         # Jupyter notebooks for visualization and analysis
└── requirements.txt   # Python dependencies
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ARRTQ.git
cd ARRTQ
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The project includes Jupyter notebooks demonstrating the algorithms:

- `notebooks/demo_baseRR.ipynb`: Demonstrates base Round Robin scheduling
- `notebooks/demo_baseARRTQ.ipynb`: Demonstrates base ARRTQ scheduling, also the resulting metrics show that it performs better than the base Round Robin scheduling(compare with previous notebook results)
- `notebooks/compare_baseRR_with_ARRTQ.ipynb`: Compares RR with ARRTQ    (To be implemented)

## Features

- Process scheduling simulation
- Performance metrics calculation:
  - Average Turnaround Time
  - Average Waiting Time
  - CPU Utilization
  - Context Switch Overhead
- Visualization of scheduling results
\
