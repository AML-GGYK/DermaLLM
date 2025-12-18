# Use a slim Python image to keep it small and fast
FROM python:3.10-slim

WORKDIR /app

# Install system tools needed for some python packages
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL your code + the faiss_index folder
COPY . .

# Allow FAISS to load the pickle file (safe since you created it)
ENV ALLOW_DANGEROUS_DESERIALIZATION=True

# Expose the port
EXPOSE 8080

# Run the app using Gunicorn (Production server)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "120", "main:app"]