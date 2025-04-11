# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies in stages
RUN pip install --no-cache-dir numpy==2.0.0
RUN pip install --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir spacy==3.7.2
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_lg
RUN pip install --no-cache-dir danlp[all]
RUN pip install --no-cache-dir skillNer
RUN pip install --no-cache-dir IPython
RUN pip install --no-cache-dir gensim==4.3.2
RUN pip install --no-cache-dir torch
RUN pip install --no-cache-dir flask flask-cors

# Create output directory
RUN mkdir -p /app/output

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"] 