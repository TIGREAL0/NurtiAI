
# NurtiLens Backend (Inference service)

This lightweight Flask app provides a heuristic inference endpoint at POST /api/infer.
It accepts JSON: { image_base64: '<base64 data>' } and returns detected items and calories.

## Run locally with Docker
1. docker-compose up --build
2. The service will be available at http://localhost:5000/api/infer

## Deploy to Render / Cloud Run
- Render (web service):
  1. Create a new service, connect repo, set Docker build, and deploy.
  2. Expose port 5000.
- Google Cloud Run:
  1. Build an image and push to Container Registry / Artifact Registry.
  2. Deploy the container to Cloud Run and allow unauthenticated invocations.
  3. Use the resulting URL in the Expo app (replace http://localhost:5000 in ScannerScreen).

Notes: This is a heuristic demo service. For production, replace with a real CV model (PyTorch / ONNX) and secure the endpoint with authentication and rate limits.
