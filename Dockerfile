FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python script and requirements
COPY fake_motion_sensor.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python3", "fake_motion_sensor.py"]
