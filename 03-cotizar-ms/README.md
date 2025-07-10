
# cotizar-ms — Insurance Quotation Microservice

**Language:** Python (FastAPI)
**Deployed at:** Docker (see Dockerfile), compatible with Kubernetes/OKE
**Swagger:** /swagger-ui/index.html (served by FastAPI)

## Functionality Summary
This microservice provides endpoints to create and manage insurance quotations for users. It supports product-based quoting, stores quotes in a relational database, and exposes endpoints for CRUD operations on quotes and insurance products.

## Detailed Functionality
- Create a new insurance quote for a user, referencing a product and term
- List all quotes for the authenticated user
- Retrieve details of a specific quote
- List available insurance products
- Healthcheck endpoint for monitoring
- Interactive API documentation via Swagger UI

## Returned Endpoints
| Method | Endpoint                | Description                                 |
|--------|------------------------|---------------------------------------------|
| POST   | /cotizacion            | Create a new insurance quote                |
| GET    | /cotizacion            | List all quotes for the authenticated user  |
| GET    | /cotizacion/{id}       | Get details of a specific quote             |
| GET    | /productos             | List available insurance products           |
| GET    | /cotizacion/health     | Healthcheck endpoint                        |
| GET    | /swagger-ui/index.html | Swagger/OpenAPI documentation               |
