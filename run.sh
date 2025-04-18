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

mkdir -p logs

echo "Running the agent"
timestamp=$(date)
start_time=$(date +%s)
log_file="logs/run_$start_time.log"
echo "$timestamp" >> "$log_file"
echo "===========================" >> "$log_file"
echo "Agent is running in background. All logs are in $log_file"
uv run run_crew "$@" >> "$log_file"
end_time=$(date +%s)
echo "Execution time: $(($end_time - $start_time)) seconds"
echo "Execution time: $(($end_time - $start_time)) seconds" >>"$log_file"

