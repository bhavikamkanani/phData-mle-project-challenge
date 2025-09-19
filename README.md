# House Price Prediction – Deployment Documentation

### Approach Summary

I have implemented a full workflow to deploy ML model, and test a house price prediction model. The solution was designed with real-world scalability in mind using Kubernetes.

- **1. REST API Service**
	-	Built a FastAPI application to serve predictions.
	-	Endpoints implemented:
	    -	/health → Health check.
	    -	/predict → only requires the subset of sales features (no demographics).

    **Sample curl request**

    ```bash 
    curl -s -X POST http://127.0.0.1:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"bedrooms": 3, "bathrooms": 2, "sqft_living": 1800,
         "sqft_lot": 5000, "floors": 2, "sqft_above": 1800,
         "sqft_basement": 0, "zipcode": "98103"}' 
    ```
    
    **Response**
    ```
    {
    "prediction": 523421.5,
    "model_version": "v1"
    }
    ```

- **2. Build and Push Docker Image**
    - Build Docker image
        - ```docker build -t bhavika123/house-price-service:v2 .  ```
    - Push image to Docker Hub
        - ```docker push bhavika123/house-price-service:v2 ```
    - Update Kubernetes Deployment
        - ```kubectl set image deployment/house-price-deployment house-price=bhavika123/house-price-service:v2 -n ml-dev ```

- **3.  Deployment on Kubernetes**
    - Packaged the API in a Docker container.
	- Created Kubernetes manifests:
	    - Deployment (2 replicas for scaling).
	    - Service (ClusterIP for internal access).
        - Horizontal Pod Autoscaler for dynamic scaling
	-   Model versioning:
	    -   New versions of the model can be deployed by updating the container image → rolling update ensures zero downtime.

- **4. Test Script**
	-  Added deploy.sh script to automate:
	    -   Deploying manifests (optional, based on user prompt).
	    -   Port-forwarding the service to localhost:8080.
		-   Running health check and test prediction via curl.

- **5. How to Run**
    - **Prerequisite:** Kubernetes cluster (minikube, GKE, 
    EKS, etc.).
    - Run ```sh deploy.sh```

- **6. Alternative Deployment: AWS SageMaker Real-Time Endpoint**
    - Step 1: Prepare the model
        - ```tar -czvf house-price-model.tar.gz model.pkl model_features.json```
    - Step 2: Upload package to S3
    - Step 3: Create a SageMaker Model
    - Step 4: Create a Real-Time Endpoint
    - Step 5: Invoke the Endpoint
