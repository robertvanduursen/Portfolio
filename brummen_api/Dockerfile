# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy the Flask application code into the image
COPY . .

# Install dependencies (if any)
RUN pip install -r requirements.txt

# Expose the port that the Flask server is listening on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
