## Project Structure

```
ARRTQ/
├── core/               # Core implementation of scheduling algorithms
│   ├── __init__.py
│   ├── process.py     # Process class definition
│   ├── scheduler_rr.py # Base Round Robin implementation
│   └── scheduler_arrtq.py # ARRTQ implementation
│   ├── scheduler_modified_ARRTQ.py     # proposed balanced ARRTQ Algorithm
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

- `notebooks/compare_ARRTQ_balancedARRTQ.ipynb`: Compares the algorithms( ARRTQ, balanced ARRTQ) 

## Features

- Process scheduling simulation
- Performance metrics calculation:
  - Average Turnaround Time
  - Average Waiting Time
  - First Response Times & Average First Response Time
  - CPU Utilization
  - Context Switch Overhead
- Visualization of scheduling results
