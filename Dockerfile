# Stage 1: Dependencies
FROM python:3.12-slim as dependencies

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_lg

# Stage 2: Build
FROM dependencies as build

# Copy the rest of the application
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Stage 3: Runtime
FROM python:3.12-slim as runtime

# Copy only necessary files from build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app /app

# Set working directory
WORKDIR /app

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"] 