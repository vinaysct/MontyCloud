# Image Upload Service (FastAPI + AWS + LocalStack)

This project implements a scalable image upload and storage service (Instagram-like)
using AWS serverless services and FastAPI. It can run completely locally using LocalStack.

## Architecture
Client
 -> API Gateway
 -> Lambda (FastAPI)
 -> S3 (image storage)
 -> DynamoDB (metadata)

## Tech Stack
- Python 3.7+
- FastAPI
- AWS Lambda + API Gateway
- Amazon S3
- Amazon DynamoDB
- LocalStack
- Docker / Docker Compose

## Prerequisites
- Docker & Docker Compose
- Python 3.7+

## Setup Instructions

### 1. Start LocalStack
docker-compose up -d

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the API locally
uvicorn app.main:app --reload

### 4. Open API Docs
http://localhost:8000/docs

## APIs
POST /images/upload
GET /images
GET /images/{image_id}
DELETE /images/{image_id}

## Testing
pytest

## Notes
- Images stored in S3
- Metadata stored in DynamoDB
- Presigned URLs used for download
