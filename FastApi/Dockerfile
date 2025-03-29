# Etapa 1: Construcción
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependencias necesarias para compilar paquetes
RUN apt-get update && apt-get install -y build-essential

# Copiar archivos de requerimientos e instalar dependencias en un venv
COPY **/requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Etapa 2: Imagen final optimizada
FROM python:3.11-slim

WORKDIR /app

# Copiar solo el entorno virtual desde la imagen builder
COPY --from=builder /opt/venv /opt/venv

# Copiar código fuente
COPY . .

# Usar el entorno virtual como predeterminado
ENV PATH="/opt/venv/bin:$PATH"

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]