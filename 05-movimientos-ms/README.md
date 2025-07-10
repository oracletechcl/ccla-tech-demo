

# movimientos-ms — Account Movements Microservice

**Language:** Python (FastAPI)
**Deployed at:** Kubernetes (OKE) + Docker
**Swagger:** http://portalbancario.alquinta.xyz/movimientos/swagger-ui/index.html

## Functionality Summary
This microservice exposes endpoints to query account movements and transactions for users. It is designed for scalable, cloud-native deployments and easy integration with banking portals.

## Detailed Functionality
- List all account movements for a user
- Healthcheck endpoint for monitoring
- Expose Swagger/OpenAPI documentation for all endpoints

## Returned Endpoints
| Method | Endpoint                | Description                                 |
|--------|------------------------|---------------------------------------------|
| GET    | /movimientos           | List all account movements for the user     |
| GET    | /health                | Healthcheck endpoint                        |
| GET    | /swagger-ui/index.html | Swagger/OpenAPI documentation               |