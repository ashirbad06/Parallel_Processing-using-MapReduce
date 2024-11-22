import csv
import multiprocessing
import threading
import os
import sys
from collections import defaultdict
import math

# Add the parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from engine_source_code.engine import Task

#Here we make the data-path for the files for processing
def break_down_tasks(data_dir):
    tasks = []
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(data_dir, file)
            tasks.append(file_path)
    return tasks

# Map Phase: Process each file and calculate min, max, and average per batch year
def map_function(file_path):
    batch_year_stats = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'total': 0, 'count': 0})

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # Check if the file has a header and skip it if necessary
            header = next(reader, None)
            
            for row in reader:
                batch_year = row[1].strip()
                score_str = row[2].strip()
                
                if not batch_year or not score_str:
                    print(f"Skipping row with missing batch year or score in file {file_path}: {row}")
                    continue  # Skip rows with missing batch year or score

                try:
                    score = float(score_str)
                except ValueError:
                    print(f"Skipping row with invalid score in file {file_path}: {row}")
                    continue  # Skip rows where score is not a valid float

                stats = batch_year_stats[batch_year]
                stats['min'] = min(stats['min'], score)
                stats['max'] = max(stats['max'], score)
                stats['total'] += score
                stats['count'] += 1

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

    # Compute averages
    results = []
    for batch_year, stats in batch_year_stats.items():
        avg = stats['total'] / stats['count'] if stats['count'] > 0 else 0
        results.append((batch_year, int(stats['min']), int(stats['max']), avg))

    return results

# Reduce Phase: Aggregate results from each file
def reduce_function(results):
    aggregated_stats = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'total': 0, 'count': 0})

    for result in results:
        for batch_year, min_value, max_value, avg_value in result:
            stats = aggregated_stats[batch_year]
            stats['min'] = min(stats['min'], min_value)
            stats['max'] = max(stats['max'], max_value)
            stats['total'] += avg_value
            stats['count'] += 1

    final_results = []
    for batch_year, stats in aggregated_stats.items():
        avg = int(stats['total'] / stats['count']) if stats['count'] > 0 else 0
        final_results.append((batch_year, int(stats['min']), int(stats['max']), avg))

    return sorted(final_results, key=lambda x: int(x[0]))  # Sort by batch year

def write_output(results, output_file):
    try:
        with open(output_file, 'w') as file:
            for batch_year, min_val, max_val, avg_val in results[:-1]:
                avg = math.floor(avg_val)
                file.write(f"{batch_year},{min_val},{max_val},{avg}\n")
            # Write the last line without adding an extra newline
            if results:
                batch_year, min_val, max_val, avg_val = results[-1]
                avg = math.floor(avg_val)
                file.write(f"{batch_year},{min_val},{max_val},{avg}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")

def threaded_write(results, output_file):
    thread = threading.Thread(target=write_output, args=(results, output_file))
    thread.start()
    thread.join()

def clean_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Remove trailing whitespace from each line
    cleaned_lines = [line.rstrip() for line in lines]
    
    # Write cleaned lines to a new file
    with open(file_path, 'w') as file:
        for line in cleaned_lines:
            file.write(f"{line}\n")

if __name__ == '__main__':
    data_dir = 'sample_dataset/student_scores'
    tasks = break_down_tasks(data_dir)

    if not tasks:
        print("No tasks were created.")
        sys.exit(1)

    num_cores = multiprocessing.cpu_count() #I could have hardcoded it to 4 but we can see the performance better in this way.
    print(f"Using {num_cores} cores for processing.")

    # Map Phase: Distribute tasks to worker processes
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(map_function, tasks)

    if not results:
        print("No results were generated.")
        sys.exit(1)

    # Reduce Phase: Aggregate results
    final_results = reduce_function(results)

    # Use threading to write output file in parallel
    threaded_write(final_results, 'output.txt')
    clean_file('output.txt')
    print("Processing complete. Results written to output.txt.")
