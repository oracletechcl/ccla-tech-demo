

# login-ms — Authentication Microservice

**Language:** Node.js (Express)
**Deployed at:** OCI Container Instance (Docker)
**Swagger:** http://192.18.141.177/api-docs/

## Functionality Summary
This microservice provides user authentication and user management for banking portal applications. It issues JWT tokens for secure access to protected endpoints and supports full CRUD operations for users. Designed for cloud-native deployments and integration with other microservices.

## Detailed Functionality
- Authenticate users via `/login` endpoint (returns JWT on success)
- Validate JWT tokens for protected endpoints
- Manage users (create, read, update, delete)
- Store user data in a MySQL database
- Expose OpenAPI/Swagger documentation for all endpoints
- Healthcheck endpoint for monitoring

## Returned Endpoints
| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| POST   | /login           | Authenticate user, returns JWT     |
| GET    | /usuarios        | List all users (protected)         |
| POST   | /usuarios        | Create a new user (protected)      |
| PUT    | /usuarios/:id    | Update user by ID (protected)      |
| DELETE | /usuarios/:id    | Delete user by ID (protected)      |
| GET    | /health          | Healthcheck endpoint               |
| GET    | /api-docs        | Swagger/OpenAPI documentation      |

