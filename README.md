gcloud container clusters create dwk-cluster \
  --zone=europe-north1-b \
  --cluster-version=1.32 \
  --disk-size=32 \
  --num-nodes=1 \
  --machine-type=e2-medium

(I had issues with --machine-type=e2-micro so I changed to medium)

kubectl apply -k .
