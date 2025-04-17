#!/bin/bash
if ! command -v uv &> /dev/null
then
    echo "'uv' is not installed. Installing..."
    # Check if pip is available and install uv
    if command -v pip &> /dev/null
    then
        pip install uv
    else
        echo "Error: pip is not installed. Please install pip and try again."
        exit 1
    fi
fi
if [ ! -d ".venv" ]; then
    echo "Virtual environment '.venv' not found. Creating a new one..."
    uv venv .venv
    source .venv/bin/activate
    echo "Installing uv and dependencies..."
    uv pip install -r requirements.txt
else
    source .venv/bin/activate
fi
echo "Running the agent"
start_time=$(date +%s)
timestamp=$(date)
echo $timestamp >> logs/run.log
echo "===========================" >> logs/run.log
echo "Agent is running in background all logs are in logs/run_$start_time.log"
uv run run_crew "$@" > logs/run_$start_time.log 
end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Time taken for the blog writing is: $elapsed_time seconds"

