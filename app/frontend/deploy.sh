 gcloud builds submit --tag gcr.io/counting-vertebrae-003/vcounter
 gcloud run deploy --image gcr.io/counting-vertebrae/vcounter:latest --memory 2Gi