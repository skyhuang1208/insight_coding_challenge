# Programming language used
Python 3

# How to run
To run the code with auto mode, simply enter the command ./run.sh  
To run the code with manual mode, execute run.sh with 1 or more arguments, e.g., ./run.sh manual  
It would ask user to specify the python3 path/command and whether to run the unit tests.

# File added/modified
1. process_log_CHHunag.py (at ./src/)
2. unit_test_CHHuang.py (at ./src/)
3. run.sh (at ./)

## process_log_CHHuang.py

Implementations of process log features. Read in "log.txt", parse variables, and calculate the following features:

### Feature 1:
List the top 10 most active host/IP addresses that have accessed the site.  
Implementation: a dictionary Naccs_host(key: host/IP, value: count) stores counts during reading log.txt, then sort it and get top 10.

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site.  
Implementation: a dictionary Bytes_rsrc(key: resources, value: sum_bytes) stores sum of bytes during reading log.txt, then sort it and get top 10.

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods. The detailed definitions are: (1) the hour windows can overlap (2) the window cannot starts before the beginning of time of log.txt, but can include time range after the end of log.txt (e.g., if log.txt is from 01:02:03 to 13:14:15, the possible starting time of windows are from 01:02:03 to 13:14:15)  
Implementation: a dictionary Naccs_time(key: Epoch time in seconds, value: event counts) stores counts in a second during reading log.txt, then do rolling sum over all windows with different starting times. After that, sort it and get top 10.

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.  
Implementation: a dictionary Nfail_host (key: host/IP, value: [Nfails, Epoch_time]), storing number of fails and time of 1st-fail or beginning of the block, is kept updating during reading log.txt. When the block criteria meet, output the blocked lines.

### Feature 5 (NEW hour) (Additional):
Since Feature 3 could easily end up with 10 windows with only few seconds different, which makes the feature less meaningful/useful, I implemented a new hour feature. In the feature, hour windows are strictly defined as from XX:00:00 to XX:59:59, where XX are possible hours. In this case, the windows do not overlap with each other, and the property can be easily interprete (Although we might lose some resolutions).  
Implementation: sum over the Naccs_time dictionary in feature 3 within the strictly hour windows. After that, sort the results and get top 10.

### Program structures (functions):
* parse_data: input a line of string, return variables
* compute_feature1: post processing after reading. Compute feature 1 and print data to hosts.txt
* compute_feature2: post processing after reading. Compute feature 2 and print data to resources.txt
* compute_feature3: post processing after reading. Compute feature 3 and print data to hours.txt
* checkNfail_feature4: use replycode and timesecs to determine the status of a host/IP. Modify Nfail_host, return True if the request is blocked; False otherwise.
* compute_feature5: post processing after reading. Compute feature 5 and print data to hoursNEW.txt
* main: main function. read log.txt file and perform analysis.

The program can be imported as a module or executed as the main function.

## unit_test_CHHuang.py

Used to test if functions work properly. Right now only the following tests were implemented:

* test_parse_data: 4 test cases are used to test parse_data (including an error case).
* test_checkNfail_feature4: 15 cases are used to test checkNfail_feature4 (including an error case).

The program can be imported as a module or executed as the main function as well.

## run.sh

Used to run programs. Two modes can be used:

* AUTO MODE: simply execute "./run.sh", the shell script would run process log (process_log_CHHuang.py) with python3.
* MANUAL MODE: if execute with 1 or more arguements, e.g., "./run.sh manual", it would ask user to enter python3 path/command, and whether to perform unit tests.

