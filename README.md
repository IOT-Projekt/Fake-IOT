# Fake IoT Device Simulator

The Fake IoT Device Simulator is a tool designed to emulate IoT device data for simulations and analyses. This project is ideal for testing data pipelines, training machine learning models, and learning about IoT systems without access to physical hardware.

## Features

- Generates simulated IoT data.
- Sends data using the **MQTT** protocol.

## Project Structure

- **`src/`**: Contains Python scripts.
- **`config/`**: Configuration file for project settings.

## Requirements

- Docker 

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Ziggyyy92/fake-iot-project.git
   cd fake-iot-project

2. Run the Docker container:
   ```bash
   docker run -e BROKER_IP=YOURIPHERE iot-temperature-simulator
   
Replace YOURIPHERE with the IP address of your MQTT broker.
   
# Multiple Instances with Docker Compose

1. Edit the **`docker-compose.yml`** file:

- Set the desired number of containers.
- Specify the BROKER_IP environment variable.

2. Start the containers:
   ```bash
   docker compose up -d

This will run the specified number of IoT device simulators as defined in the docker-compose.yml file.
