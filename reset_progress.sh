#!/bin/bash

# Ask for confirmation
echo "This will delete all your progress data. Are you sure? (y/n)"
read -r response

if [[ "$response" == "y" || "$response" == "Y" ]]; then
    # Remove the JSON data file
    echo "Resetting progress..."
    rm -f tactics_progress.json
    echo "Progress has been reset."
else
    echo "Reset canceled."
fi
