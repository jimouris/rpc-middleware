# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and config
COPY src/ ./src/
COPY rpc-providers/ ./rpc-providers/

# Expose FastAPI default port
EXPOSE 8000

# Add a default command to run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
