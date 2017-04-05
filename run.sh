#!/usr/bin/env bash

# one example of run.sh script for implementing the features using python
# the contents of this script could be replaced with similar files from any major language

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
#python ./src/process_log.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/hours.txt ./log_output/resources.txt ./log_output/blocked.txt

py3=python3 # interpreter of python3

if [ $# -ne 0 ]; then
    ### MANUAL MODE ###
    
    # Specify python3 interpreter
    echo ""
    echo "%%%%% MANUAL RUN MODE %%%%%"
    echo "Please specify the python3 interpreter path or command:(default: python3)"
    read py3temp
    if [ ! -z $py3temp ]; then
        py3=$py3temp
    fi
    echo "Using the interpreter $py3 ."
   
    # Determine if run process code or unit test
    echo "Do you want to run unit test? (yes/no)"
    read isUtest
    echo ""
    if [ $isUtest == "yes" ]; then
        echo "Running unit test..."
        $py3 ./src/unit_test_CHHuang.py
    else
        echo "Running process_log..."
        $py3 ./src/process_log_CHHuang.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/resources.txt ./log_output/hours.txt ./log_output/blocked.txt ./log_output/hoursNEW.txt
    fi

else
    ### AUTO MODE ###
    echo ""
    echo "%%%%% AUTO RUN MODE %%%%%"
    echo "Using $py3 as python3 interpreter to run process program."
    echo "NOTE: if you want to manually select running parameter, use 1 or more arguments."
    echo ""

    $py3 ./src/process_log_CHHuang.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/resources.txt ./log_output/hours.txt ./log_output/blocked.txt ./log_output/hoursNEW.txt

fi
