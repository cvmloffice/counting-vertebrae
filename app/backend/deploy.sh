 gcloud builds submit --tag gcr.io/counting-vertebrae-003/vcounter
 gcloud run deploy \
    --image gcr.io/counting-vertebrae-003/vcounter \
    --memory 2Gi \
    --min-instances 1 \
    --region us-central1 \
    --allow-unauthenticated \
    --port 80
