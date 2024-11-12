# Use a base image with LibreOffice
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y libreoffice python3 python3-pip python3-venv && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Create and activate a virtual environment, and install Python dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the application using the virtual environment
CMD ["/app/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
