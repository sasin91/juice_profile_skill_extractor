# Stage 1: Dependencies
FROM python:3.12-slim as dependencies

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in one RUN to reduce layers
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Stage 2: Build
FROM python:3.12-slim as builder

WORKDIR /app

# Copy only what's needed from dependencies
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Stage 3: Runtime
FROM python:3.12-slim as runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Clean up unnecessary files more efficiently
RUN find /usr/local/lib/python3.12/site-packages \
    \( -type d -name "tests" -o -name "test" -o -name "__pycache__" \) -exec rm -rf {} + \
    && find /usr/local/lib/python3.12/site-packages -type f -name "*.pyc" -delete

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Use a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=2)"

EXPOSE 5000

# Use exec form for CMD
CMD ["python", "app.py"]