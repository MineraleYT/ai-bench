#!/bin/sh

# This script needs to be sourced, not executed
if [ "$0" = "$BASH_SOURCE" ] || [ "$0" = "$ZSH_NAME" ]; then
    echo "Error: This script needs to be sourced. Run:"
    echo "    source setup.sh"
    echo "or:"
    echo "    . setup.sh"
    exit 1
fi

# Exit on error
set -e

echo "Creating Python virtual environment..."
# Try python3 first, fall back to python if not found
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

$PYTHON -m venv .venv

echo "Activating virtual environment..."
# Handle different shells (bash, zsh)
case "$SHELL" in
    */zsh)
        source .venv/bin/activate || . .venv/bin/activate
        ;;
    *)
        . .venv/bin/activate
        ;;
esac

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup completed successfully!"

# Leave the virtual environment activated for the user
echo -e "\nVirtual environment is now active. You can run:"
echo "    python main.py"
