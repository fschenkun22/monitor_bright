#!/bin/bash
# Startup script for Monitor Brightness API

echo "Monitor Brightness API - Startup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully"
echo ""

# Parse command line arguments
PORT=5000
HOST="0.0.0.0"
DEBUG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--port PORT] [--host HOST] [--debug]"
            exit 1
            ;;
    esac
done

# Start the server
echo "Starting Monitor Brightness API..."
echo "Host: $HOST"
echo "Port: $PORT"
echo ""

python3 app.py --port=$PORT --host=$HOST $DEBUG
