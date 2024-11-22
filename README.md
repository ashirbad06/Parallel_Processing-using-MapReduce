# Skeleton Project

This project consists of two main components that leverage parallel and distributed processing for efficient data computation and task management:

1. **Driver Code (`driver_code.py`)**: Processes large CSV datasets to compute statistical metrics (min, max, average) for each batch year, utilizing multiprocessing and threading.
2. **Engine Code (`engine.py`)**: Implements a server using multiprocessing and socket programming to manage and process tasks received from clients.

---

## Features

- **MapReduce Implementation**:
  - **Map Phase**: Processes CSV files independently to calculate statistics for each batch year.
  - **Reduce Phase**: Aggregates results from all files, producing consolidated output.
- **High Performance**:
  - Multiprocessing and threading for fast and scalable processing.
  - Socket programming for efficient client-server communication.
- **Robust Exception Handling**:
  - Handles errors gracefully, ensuring uninterrupted execution.

---

## Prerequisites

Ensure the following are installed on your system:

- **Python 3.x**
- **Bash** (for script execution)

### Install Required Python Libraries:
Install necessary Python dependencies using `pip`:
```bash
pip install -r requirements.txt
```

```bash
sudo chmod +x driver_code.py engine.py
```
```bash
bash start_engine.sh
```
```bash
bash start_driver.sh
```
```bash
bash start_driver.sh
```

```bash
python3 test_runner.py
```
