#!/bin/bash
set -e

echo "Do you want to deploy manifests? (yes/no)"
read DEPLOY_CHOICE

if [[ "$DEPLOY_CHOICE" == "yes" || "$DEPLOY_CHOICE" == "y" ]]; then
    echo "[info] Creating deployment..."
    kubectl apply -f deployment.yaml

    echo "[info] Waiting for pods to be ready..."
    kubectl rollout status deployment/house-price-deployment -n ml-dev
else
    echo "[info] Skipping deployment. Using existing resources in namespace ml-dev"
fi

echo "[info] Port-forwarding service to localhost:8080"
kubectl port-forward svc/house-price-svc 8080:80 -n ml-dev &
PF_PID=$!
sleep 5

echo "\n[info] Testing health endpoint..."
curl -s http://127.0.0.1:8080/health

echo "\n\n[info] Testing prediction..."
curl -s -X POST http://127.0.0.1:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"bedrooms": 3, "bathrooms": 2, "sqft_living": 1800,
         "sqft_lot": 5000, "floors": 2, "sqft_above": 1800,
         "sqft_basement": 0, "zipcode": "98103"}' | jq .

kill $PF_PID
echo "\nDone."