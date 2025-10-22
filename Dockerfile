# Imagen base ligera
FROM python:3.10-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Instala solo las dependencias necesarias para OpenCV y DeepFace en CPU
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Establece directorio de trabajo
WORKDIR /app

# Copia solo lo necesario primero para aprovechar cache
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . /app

# Copia los pesos de DeepFace si los tienes predescargados
COPY .deepface/weights /root/.deepface/weights

# Script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]
