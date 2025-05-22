#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <command> [args...]"
    exit 1
fi

# Extract the command and arguments
subprocess_command="$1"
shift
subprocess_args="$@"

# Check if the subprocess command is available and executable
if [[ ! -x "$(command -v $subprocess_command)" ]]; then
    echo "Command '$subprocess_command' not found or not executable. Exiting..."
    exit 1
fi

# Check if subprocess args contains '<' or '>', if so exit
if [[ "$subprocess_args" == *"<"* || "$subprocess_args" == *">"* ]]; then
    echo "Subprocess command should not contain '<' or '>'. Exiting..."
    exit 1
fi

# Create named pipes (FIFOs) for communication
input_pipe="/tmp/input_pipe"
output_pipe="/tmp/output_pipe"

if [[ ! -p $input_pipe ]]; then
    mkfifo $input_pipe
    if [[ $? -ne 0 ]]; then
        echo "Failed to create input pipe. Exiting..."
        exit 1
    fi
fi

if [[ ! -p $output_pipe ]]; then
    mkfifo $output_pipe
    if [[ $? -ne 0 ]]; then
        echo "Failed to create output pipe. Exiting..."
        exit 1
    fi
fi

# Start the subprocess in the background
$subprocess_command $subprocess_args < $input_pipe > $output_pipe &
subprocess_pid=$!

# Function to handle cleanup
cleanup() {
    echo "Cleaning up..."
    kill $subprocess_pid 2>/dev/null
    rm -f $input_pipe $output_pipe
}
trap cleanup EXIT
trap 'cleanup; exit' SIGINT SIGTERM

# Function to execute the subprocess
while true; do
    echo -n "Enter Input > "
    read user_input
    if [[ "$user_input" == "exit" ]]; then
        echo "Exiting..."
        break
    fi

    # Check if the subprocess is already running
    if ! kill -0 $subprocess_pid 2>/dev/null; then
        echo "Subprocess is NOT running. Exiting..."
        exit 1
    fi

    echo "$user_input" > $input_pipe

    # Read the command from the input pipe
    read -r response < $output_pipe
    echo "Response > $response"
done 