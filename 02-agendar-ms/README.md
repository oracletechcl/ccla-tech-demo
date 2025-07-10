

# agendar-ms — Appointment Scheduling Microservice

**Language:** Python (Oracle Functions)
**Deployed at:** Oracle Cloud Functions (Fn Project)
**Swagger:** Not available (function-based deployment)

## Functionality Summary
This microservice allows authenticated users to create, list, and delete appointment reservations. It is designed for serverless deployment and integration with banking or enterprise portals.

## Detailed Functionality
- Create a new appointment reservation for a user
- List all reservations for the authenticated user
- Delete a reservation by ID
- Enforce authentication for all operations
- Designed for stateless, event-driven execution in Oracle Cloud Functions

## Returned Endpoints
| Function Name            | Method | Description                                 |
|-------------------------|--------|---------------------------------------------|
| crear-reserva           | POST   | Create a new appointment reservation         |
| obtener-reservas-usuario| GET    | List all reservations for the user          |
| eliminar-reserva        | DELETE | Delete a reservation by ID                  |

> Note: Endpoints are invoked as Oracle Functions, not as traditional REST URLs. See Fn Project documentation for invocation details.