# ---------- STAGE 1: Build ----------
FROM maven:3.9.7-eclipse-temurin-17-alpine AS builder

WORKDIR /build

# Copiar pom y dependencias primero (cachear)
COPY pom.xml .
COPY src ./src

# Build (ajusta si tienes configuración especial)
RUN mvn clean package -DskipTests

# ---------- STAGE 2: Run ----------
FROM eclipse-temurin:17-jre-alpine

# Crear un usuario sin privilegios (seguridad)
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

WORKDIR /app

# Copia el JAR desde la imagen builder
COPY --from=builder /build/target/*.jar app.jar

# Permisos seguros
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]