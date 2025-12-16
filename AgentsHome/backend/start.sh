#!/bin/bash

# Start AgentsHome Backend API
cd /workspaces/yashus/AgentsHome/backend

# Install dependencies
pip install -r requirements.txt

# Run migrations (create tables)
python -m app.main

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
