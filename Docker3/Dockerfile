# Usa una imagen base de python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY app.py requirements.txt hosts.ini playbook.yml ./

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["python", "app.py"]

