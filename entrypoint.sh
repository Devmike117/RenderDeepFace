#!/bin/bash
exec uvicorn deepface_service:app --host 0.0.0.0 --port 8000
