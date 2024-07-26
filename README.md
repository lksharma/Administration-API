# Flask API Application

## Overview

This repository contains a Flask application that interacts with a PostgreSQL database. The application includes API endpoints to manage content with encryption and decryption capabilities. This document provides a guide to set up and use the application, including detailed API documentation.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

```
docker compose up -d
```

## Running Tests
```
docker compose -f docker-compose.test.yml up
```

## API Documentation

### Health Check
```
curl http://localhost:5000/health
```

### Create a new content
```
curl -X POST http://localhost:5000/contents \
    -H "Content-Type: application/json" \
    -d '{
        "protection_system": 1,
        "encryption_key": "p2iW1rL0WwjbkBFv6Er67Q==",
        "plaintext_payload": "This is a new payload."
    }'
```

### Decrypt content by ondent ID and device ID

```
curl -X GET http://localhost:5000/decrypt/content/<int:content_id>/device/<int:device_id>
```

### Retrieve all contents
```
curl http://localhost:5000/contents
```

### Retrieve a specific content by ID
```
curl http://localhost:5000/contents/<int:content_id>
```

### Update a content by ID
```
curl -X PUT http://localhost:5000/contents/<int:content_id> \
    -H "Content-Type: application/json" \
    -d '{
        "protection_system": 2,
        "encryption_key": "new_encryption_key",
        "plaintext_payload": "Updated payload"
    }'
```

### Delete a content by ID
```
curl -X DELETE http://localhost:5000/contents/<int:content_id>
```