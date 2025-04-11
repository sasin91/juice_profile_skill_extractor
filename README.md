# Juice Skill Extractor

A powerful skill extraction service that uses NLP to identify and extract skills from text. Built with spaCy, skillNer, and Flask, this service provides a simple API endpoint to extract skills from job descriptions, resumes, or any text content.

## Features

- Extracts skills from text using advanced NLP techniques
- Handles various skill formats and combinations (e.g., "UX/UI", "product design")
- Supports multiple languages through automatic translation
- RESTful API endpoint with CORS support
- Dockerized for easy deployment
- Built with Python 3.12 and modern NLP libraries

## Use Cases

- Resume parsing and skill extraction
- Job description analysis
- Skill gap analysis
- Talent matching
- Automated skill tagging

## Prerequisites

- Docker installed on your system
- Postman (for testing the API)

## Setup and Running

1. Clone the repository:
```bash
git clone <repository-url>
cd juice_profile_skill_extractor
```

2. Build the Docker image:
```bash
docker build -t juice-skill-extractor .
```

3. Run the container:
```bash
docker run -p 5000:5000 juice-skill-extractor
```

The API will be available at `http://localhost:5000`

## API Usage

### Endpoint
```
POST /extract-skills
```

### Request Format
```json
{
    "text": "Your text content here"
}
```

### Example Request
```json
{
    "text": "5+ years of experience in product design\nStrong portfolio showcasing UX/UI work\nExperience with Figma or similar tools\nAbility to work in a fast-paced environment\nExcellent communication skills"
}
```

### Example Response
```json
{
    "skills": [
        "Communication",
        "Figma",
        "UI",
        "UX",
        "communication skills",
        "product design"
    ],
    "original_language": "en"
}
```

### Non-English Language Support

The API automatically detects and handles non-English text by translating it to English before processing. This ensures consistent skill extraction across languages.

#### Danish Example

Request:
```json
{
    "text": "5 års erfaring med produktdesign\nStærkt portfolio der viser UX/UI arbejde\nErfaring med Figma eller lignende værktøjer\nEvne til at arbejde i et hurtigt tempo\nFremragende kommunikationsevner"
}
```

Response:
```json
{
    "skills": [
        "Communication",
        "Figma",
        "UI",
        "UX",
        "communication skills",
        "product design"
    ],
    "original_language": "da"
}
```

### Error Response
```json
{
    "error": "No text provided"
}
```

## Testing with Postman

1. Import the Postman collection:
   - Open Postman
   - Click "Import" and select `skill_extractor.postman_collection.json`
   - The collection will be imported with example requests

2. Test the API:
   - Select the "Extract Skills" request
   - Click "Send" to test with the example text
   - Modify the request body to test with different text

## Deployment

### Docker Hub

The image is available on Docker Hub as `lotd/juice-skill-extractor`:

```bash
docker pull lotd/juice-skill-extractor
```

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  skill-extractor:
    image: lotd/juice-skill-extractor:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Kubernetes

Example Kubernetes deployment (`skill-extractor-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-extractor
spec:
  replicas: 2
  selector:
    matchLabels:
      app: skill-extractor
  template:
    metadata:
      labels:
        app: skill-extractor
    spec:
      containers:
      - name: skill-extractor
        image: lotd/juice-skill-extractor:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: skill-extractor
spec:
  selector:
    app: skill-extractor
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

Apply with:
```bash
kubectl apply -f skill-extractor-deployment.yaml
```

## Development

### Dependencies
The project uses the following main dependencies:
- spaCy: For NLP processing
- skillNer: For skill extraction
- Flask: For the API server
- Flask-CORS: For CORS support

All dependencies are listed in `requirements.txt`

### Running in Development Mode
To run the Flask application directly (without Docker):
```bash
python app.py
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here] 