#!/bin/bash

# Set Google Cloud project ID and region
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_REGION="us-central1"

# Build the Docker images
docker build -t gcr.io/$GOOGLE_CLOUD_PROJECT/frontend:latest ./ui-server
docker build -t gcr.io/$GOOGLE_CLOUD_PROJECT/backend:latest ./api-server

# Push the images to Google Container Registry
docker push gcr.io/$GOOGLE_CLOUD_PROJECT/frontend:latest
docker push gcr.io/$GOOGLE_CLOUD_PROJECT/backend:latest

# Deploy the services to Google Cloud Run
gcloud run deploy frontend \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/frontend:latest \
  --platform managed \
  --region $GOOGLE_CLOUD_REGION \
  --allow-unauthenticated

gcloud run deploy backend \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/backend:latest \
  --platform managed \
  --region $GOOGLE_CLOUD_REGION \
  --allow-unauthenticated

echo "Deployment complete!"
