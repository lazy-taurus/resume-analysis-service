# Dockerfile

# 1. Base Image: Use a minimal Python image
FROM python:3.10-slim

# 2. Set Working Directory inside the container
WORKDIR /app

# 3. Copy dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Expose the port where the API will run
EXPOSE 8000

# 6. Command to run the application (Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
