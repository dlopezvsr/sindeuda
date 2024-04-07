#!/bin/bash

# Start the Uvicorn server with live reload for development
uvicorn src.application.api_routes:app --host 0.0.0.0 --port 8000 --reload
