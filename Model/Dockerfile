# Use the official lightweight Python image
FROM python:3.9-slim

# Set environment variable to prevent buffering
ENV PYTHONUNBUFFERED=True

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Run the Flask app
CMD ["gunicorn", "-b", ":8080", "app:app"]