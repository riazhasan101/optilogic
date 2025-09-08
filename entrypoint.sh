#!/bin/bash

echo "Running migrations ...."

echo "Startting FastAPI Server ...."
exec uvicorn main:app --host 0.0.0.0 --port 8000
