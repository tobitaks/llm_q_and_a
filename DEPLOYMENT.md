# Deployment Guide - Ubuntu Server

This guide covers deploying the LLM Q&A Service on a fresh Ubuntu Server (20.04 LTS or later).

## Quick Setup for Ubuntu (Automated)

### Step 1: Clone and Run Setup Script

```bash
git clone https://github.com/tobitaks/llm_q_and_a.git
cd llm_q_and_a
chmod +x setup.sh
./setup.sh
```

### Step 2: Set Environment Variables

```bash
cp .env.example .env
nano .env  # Set ONE of: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY
```

### Step 3: Run the Application

```bash
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 4: Verify Deployment

1. Open a browser and navigate to `http://<server-ip>:8000`
2. Enter a question and submit
3. Verify JSON logs appear in the terminal

---

## Manual Setup

## Prerequisites

- Ubuntu Server 20.04 LTS or later
- Root or sudo access
- API key for one of: Anthropic, OpenAI, or Google Gemini

## Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip git
```

## Step 2: Clone the Repository

```bash
cd /opt
sudo git clone https://github.com/tobitaks/llm_q_and_a.git llm_q_and_a
sudo chown -R $USER:$USER llm_q_and_a
cd llm_q_and_a
```

## Step 3: Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

## Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 5: Set Environment Variables

Copy the example environment file and add your API key:

```bash
cp .env.example .env
nano .env  # Set ONE of: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY
```

## Step 6: Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Step 7: Verify Deployment

1. Open a browser and navigate to `http://<server-ip>:8000`
2. Enter a question and submit
3. Verify JSON logs appear in the terminal

## Troubleshooting

### Check Logs

Application logs are output as JSON to stdout in the terminal where uvicorn is running.