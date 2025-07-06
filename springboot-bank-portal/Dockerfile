# --- 1. Build React Frontend ---
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# --- 2. Build Spring Boot Backend and integrate React build ---
FROM maven:3.9-eclipse-temurin-17-alpine AS backend-builder
WORKDIR /app
COPY pom.xml ./
COPY src ./src
COPY --from=frontend-builder /frontend/build ./src/main/resources/static
RUN mvn clean package -DskipTests

# --- 3. Package minimal runtime image ---
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=backend-builder /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
