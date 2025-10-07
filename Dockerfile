FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the app code
COPY ./app /app 

# Expose the app port
EXPOSE 8000

# Start FastAPI using uvicorn
# - host 0.0.0.0 to listen in container
# - port 8000 to match compose mapping
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
