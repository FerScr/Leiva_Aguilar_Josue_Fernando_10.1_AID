# Usa una imagen base de Python
FROM python:3.9-slim

# Selecciona el directorio
WORKDIR /app

#
COPY . /app

# Instala los requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instala Ansible y SSH
RUN apt-get update && \
    apt-get install -y ansible openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Genera la clave SSH y ajusta los permisos
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -N ''

# Copia los playbooks en el contenedor
COPY playbooks /app/playbooks

# Expone el puerto 5000
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=app.py

# Ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]
