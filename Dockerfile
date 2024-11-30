FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python script and requirements
COPY fake_temparatures.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose MQTT port (optional for external communication)
EXPOSE 1883

# Run the Python script
CMD ["python", "fake_temparatures.py"]
