import csv
import multiprocessing
import socket
import sys
import math
# Define a task structure to hold the file path and target column index
class Task:
    def __init__(self, file_path, target_column):
        self.file_path = file_path
        self.target_column = target_column

# Define a function to read a CSV file and calculate min, max, and avg of the target column
def process_file(task):
    min_value = float('inf')
    max_value = float('-inf')
    total = 0
    count = 0

    with open(task.file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header if it exists, remove if not needed
        for row in reader:
            try:
                value = float(row[task.target_column])
                min_value = min(min_value, value)
                max_value = max(max_value, value)
                total += value
                count += 1
            except ValueError:
                # Handle the case where conversion to float fails
                continue

    avg_value = total / count if count > 0 else 0
    return min_value, max_value, avg_value

# Define a function to handle incoming connections from the driver
def handle_connection(conn, task_queue, result_queue):
    try:
        while True:
            task_data = conn.recv(1024)
            if not task_data:
                break
            task_info = task_data.decode().strip().split(',')
            task = Task(task_info[0], int(task_info[1]))
            task_queue.put(task)  # Put task in queue for worker processes

            # Collect results from worker processes
            results = []
            for _ in range(multiprocessing.cpu_count()):
                results.append(result_queue.get())

            # Process and send aggregated results
            min_values, max_values, avg_values = zip(*results)
            min_result = min(min_values)
            max_result = max(max_values)
            avg_result = sum(avg_values) / len(avg_values) if avg_values else 0
            conn.sendall(f"{min_result},{max_result},{avg_result}".encode())  # Round avg_result to floor value
    finally:
        conn.close()

# Define a function to handle worker processes
def worker(task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:
            break
        result = process_file(task)
        result_queue.put(result)

# Define the engine instance
def engine(port):
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    
    num_workers = multiprocessing.cpu_count()
    processes = []
    
    # Start worker processes
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(task_queue, result_queue))
        p.start()
        processes.append(p)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)  # Listen for up to 5 connections
    print(f'Engine instance started on port {port}')
    
    try:
        while True:
            conn, addr = sock.accept()
            print(f'Connected by {addr}')
            # Handle connection in a separate process
            process_conn = multiprocessing.Process(target=handle_connection, args=(conn, task_queue, result_queue))
            process_conn.start()
            process_conn.join()  # Wait for the connection handling to complete
    finally:
        # Close sockets and stop worker processes
        sock.close()
        for _ in range(num_workers):
            task_queue.put(None)  # Signal workers to exit
        for p in processes:
            p.join()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python engine.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    engine(port)
