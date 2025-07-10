
# tech-microservices-demo

This repository contains a suite of backend microservices for a modern banking portal technical demo, developed for Caja Los Andes. The system demonstrates cloud-native, microservice-based architecture, with each service implemented in a different language and deployed to Oracle Cloud Infrastructure (OCI) using a variety of technologies (Container Instance, Functions, OKE/Kubernetes, Docker, etc).

## What does this repository do?

This repository provides a reference implementation for:
- User authentication and JWT-based security
- Appointment scheduling and management
- Insurance product quotation and management
- Payment and debt management
- Account and transaction movement queries

Each microservice is self-contained, exposes a RESTful API (with Swagger/OpenAPI documentation where possible), and is ready for deployment in OCI or similar cloud environments. The project is ideal for learning, demos, and as a starting point for real-world banking microservices.

## Microservice Overview

| Name                    | Language         | Deployed at                | Details & Docs                                  |
|-------------------------|------------------|----------------------------|-------------------------------------------------|
| login-ms                | Node.js (Express)| OCI Container Instance     | [login-ms/README.md](01-login-ms/README.md)     |
| agendar-ms              | Python (Fn)      | Oracle Cloud Functions     | [agendar-ms/README.md](02-agendar-ms/README.md) |
| cotizar-ms              | Python (FastAPI) | Docker/Kubernetes (OKE)    | [cotizar-ms/README.md](03-cotizar-ms/README.md) |
| pagar-ms                | Java (Spring Boot)| Kubernetes (OKE)          | [pagar-ms/README.md](04-pagar-ms/README.md)     |
| movimientos-ms          | Python (FastAPI) | Kubernetes (OKE)           | [movimientos-ms/README.md](05-movimientos-ms/README.md) |
| cc-movimientos-ms       | Python (FastAPI) | Docker/Kubernetes (OKE)    | [06-cc-movimientos-ms/README.md](06-cc-movimientos-ms/README.md) |

> For setup, deployment, and API details, see the README.md in each microservice's directory.
