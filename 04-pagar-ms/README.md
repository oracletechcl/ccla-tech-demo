

# pagar-ms — Payment Microservice

**Language:** Java (Spring Boot)
**Deployed at:** Kubernetes (OKE) + Docker
**Swagger:** /swagger-ui/index.html (if enabled in deployment)

## Functionality Summary
This microservice manages user debts and payments. It provides endpoints to list debts, process payments, and monitor service health. Designed for scalable deployment in Kubernetes environments.

## Detailed Functionality
- List all debts for a user
- Process a payment for a specific debt
- Store and update debt/payment status in a relational database
- Healthcheck endpoint for monitoring
- (Optional) Expose Swagger/OpenAPI documentation for all endpoints

## Returned Endpoints
| Method | Endpoint            | Description                        |
|--------|--------------------|------------------------------------|
| GET    | /deudas            | List all debts for the user        |
| POST   | /pagar             | Process a payment for a debt       |
| GET    | /health            | Healthcheck endpoint               |
| GET    | /swagger-ui/index.html | Swagger/OpenAPI documentation |