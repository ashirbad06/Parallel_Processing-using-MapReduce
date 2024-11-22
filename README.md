

This project consists of two primary components:

Driver Code (driver_code.py): This script processes CSV files to compute statistical metrics (min, max, average) for each batch year. It utilizes multiprocessing and threading to handle large datasets efficiently.
Engine Code (engine.py): This script sets up a server that processes tasks received from clients. It uses multiprocessing to handle concurrent tasks and socket programming to communicate with clients.

Please run 
sudo chmod +x driver_code.py engine.py
Command first. otherwise it gives the permission denied error. please male sure the directory is ./skeletom_project

Also just for the flow, kindly run
bash start_engine.sh
bash start_driver.sh

Then you can execute the python3 test_runner.py command.
Kindly ignore the OSError, the program runs fine.

I have given adequate comments to explain the logic and structure of my code. please feel free to reach out to me for any further clarification.
Also I have given a lot of exception handling statement. mostly from debugging the errors I was getting initially.

The Driver Code (driver_code.py) is designed to handle large CSV datasets quickly by using multiprocessing and threading. It splits the workload across multiple processor cores, processing each file simultaneously and calculating key metrics like minimum, maximum, and average values for each batch year. 
This approach speeds up computation by handling many tasks at once, making it efficient even with substantial amounts of data.

In this code, the MapReduce concept is used to handle and process large datasets efficiently through parallel programming. Here’s a brief explanation of how it works and its computational benefits:

Map Phase
In the Map phase, the map_function processes each CSV file to compute statistics such as minimum, maximum, and average scores per batch year. 
Each file is handled independently and concurrently across multiple processor cores.
This parallel processing splits the workload into smaller tasks that are executed simultaneously, thus speeding up the data processing.

Reduce Phase
After the Map phase, the reduce_function aggregates the results from all the processed files. 
It combines the statistics computed in the Map phase, calculates the final minimum, maximum, and average values, and sorts the results by batch year. 
This phase consolidates the dispersed data into a final result, which is then written to an output file.



On the other hand, the Engine Code (engine.py) sets up a server to manage and process tasks sent by clients, utilizing multiprocessing and socket programming. It runs several worker processes in parallel to handle different file processing tasks, 
which helps in scaling the operations and speeding up the results. By efficiently managing and aggregating these results, the engine ensures that the computations are done as quickly as possible, making it well-suited for handling high-performance data processing needs.








