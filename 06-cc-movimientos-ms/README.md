
# cc-movimientos-ms — Current Account Movements Microservice

**Language:** Python (FastAPI)
**Deployed at:** Docker (see Dockerfile), compatible with Kubernetes/OKE
**Swagger:** /swagger-ui/index.html (if enabled)

## Functionality Summary
This microservice exposes endpoints to query current account movements for users. It is designed for scalable, containerized deployments and easy integration with banking platforms.

## Detailed Functionality
- List all current account movements for a user
- Healthcheck endpoint for monitoring
- Expose Swagger/OpenAPI documentation for all endpoints (if enabled)

## Returned Endpoints
| Method | Endpoint                | Description                                 |
|--------|------------------------|---------------------------------------------|
| GET    | /movimientos           | List all current account movements for user |
| GET    | /health                | Healthcheck endpoint                        |
| GET    | /swagger-ui/index.html | Swagger/OpenAPI documentation               |
