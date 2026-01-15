# Use an official Python runtime as a parent image
# Python 3.11 is chosen for strict typing improvements and stability
FROM python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for WeasyPrint (PDF generation) and general build tools
# libpango-1.0-0, libpangoft2-1.0-0: Required for font rendering in PDFs
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the file with the requirements to the container
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the backend application code
COPY . /code/

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the application
# --host 0.0.0.0 allows external access (required for Docker networking)
# --reload enables hot reloading for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]