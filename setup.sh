#!/bin/bash

# LLM Q&A Service - Automated Setup Script
# Run this script on a fresh Ubuntu Server (20.04 LTS or later)

set -e  # Exit on any error

echo "=== LLM Q&A Service Setup ==="
echo ""

# Step 1: Install system dependencies
echo "[1/5] Installing system dependencies..."
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip git

# Step 2: Clone repository (if not already in the project directory)
if [ ! -f "main.py" ]; then
    echo "[2/5] Cloning repository..."
    cd /opt
    sudo git clone https://github.com/tobitaks/llm_q_and_a.git llm_q_and_a
    sudo chown -R $USER:$USER llm_q_and_a
    cd llm_q_and_a
else
    echo "[2/5] Already in project directory, skipping clone..."
fi

# Step 3: Create virtual environment
echo "[3/5] Creating virtual environment..."
python3.12 -m venv venv
source venv/bin/activate

# Step 4: Install Python dependencies
echo "[4/5] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Set up environment file
echo "[5/5] Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "=== IMPORTANT ==="
    echo "Please edit the .env file and add your Anthropic API key:"
    echo "  nano .env"
    echo ""
fi

echo "=== Setup Complete ==="
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Then open http://<server-ip>:8000 in your browser."
