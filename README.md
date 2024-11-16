# README.md

# Alcohol Detection System Backend

## Overview

Backend system for managing alcohol detection devices and processing measurement data. This system provides REST APIs for device management, measurement processing, and statistical analysis.

## Features

- User Authentication and Authorization
- Device Management
- Alcohol Measurement Processing
- Violation Recording
- Statistical Analysis
- Real-time Device Communication

## Technology Stack

- Python 3.8+
- Flask Framework
- PostgreSQL Database
- JWT Authentication
- SQLAlchemy ORM
- Flask-Migrate for Database Migrations

## Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Virtual Environment (recommended)

## Installation

1. Clone the repository:

   ```bash
   https://github.com/SleepsOne/alcohol_service.git
   cd alcohol-detection-system
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your configurations

5. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:

   ```bash
   python run.py
   ```

## API Documentation

### Authentication

- POST /api/auth/register - Register new user
- POST /api/auth/login - User login

### Devices

- POST /api/devices/register - Register new device
- GET /api/devices - List all devices
- GET /api/devices/{device_id} - Get device details
- PUT /api/devices/{device_id}/status - Update Device Status
- POST /api/devices/{device_id}/calibration - Update Device Calibration
- GET /api/devices/calibration/needed - Get Devices Needing Calibration
- GET /api/devices/statistics - Get Device Statistics
- PUT /api/devices/{device_id} - Update Device
- DELETE /api/devices/{device_id} - Delete Device

### Measurements

- POST /api/measurements - Create new measurement
- GET /api/measurements - List measurements
- GET /api/measurements/<id> - Get measurement details

### Statistics

- GET /api/statistics - Get general statistics
- GET /api/statistics/violations - Get violation statistics

## Testing

Run tests using:

```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
