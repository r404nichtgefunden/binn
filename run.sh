#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install required Python packages
echo "Installing required Python packages..."
pip3 install psutil python-telegram-bot==20.0
pip3 install python-telegram-bot --upgrade

# Run the bot
echo "Starting Telegram bot..."
python3 bot.py