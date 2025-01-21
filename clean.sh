#!/bin/bash

# Clean Python cache and bytecode
echo "Cleaning Python cache and bytecode files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Clean pytest cache
echo "Cleaning pytest cache files..."
rm -rf .pytest_cache

# Notify the user
echo "Cleanup complete!"
