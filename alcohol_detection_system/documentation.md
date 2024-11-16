# Alcohol Detection System API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

### Register User

Create a new user account.

```http
POST /auth/register
Content-Type: application/json

{
    "username": "string",
    "password": "string",
    "email": "string",
    "full_name": "string",
    "role": "admin|officer|user"
}
```

**Response Success (201)**

```json
{
  "success": true,
  "message": "User created successfully"
}
```

**Response Error (400)**

```json
{
  "success": false,
  "message": "Username already exists"
}
```

### Login

Authenticate user and receive access token.

```http
POST /auth/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

**Response Success (200)**

```json
{
  "success": true,
  "data": {
    "access_token": "string",
    "user_role": "string",
    "user_id": 1
  }
}
```

**Response Error (401)**

```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

## Devices

### Register Device

Register a new alcohol detection device.

```http
POST /devices/register
Authorization: Bearer <token>
Content-Type: application/json

{
    "device_id": "",
    "name": "string",
    "model": "string"
}
```

**Response Success (201)**

```json
{
  "success": true,
  "message": "Device registered successfully",
  "data": {
    "device_id": "string"
  }
}
```

### Check Device

Check device status and information.

```http
GET /devices/check/{device_id}
Authorization: Bearer <token>
```

**Response Success (200)**

```json
{
  "success": true,
  "data": {
    "exists": true,
    "device_name": "string",
    "status": "active|inactive|maintenance"
  }
}
```

### Update Device Status

PUT /api/devices/{device_id}/status
Request Body:

```json
{
  "status": "active|inactive|maintenance"
}
```

### Update Device Calibration

POST /api/devices/{device_id}/calibration

### Get Devices Needing Calibration

GET /api/devices/calibration/needed

### Get Device Statistics

GET /api/devices/statistics

### Delete Device

DELETE /api/devices/{device_id}

### Update Device

PUT /api/devices/{device_id}
Request Body:

```json
{
  "name": "string",
  "model": "string",
  "status": "string"
}
```

### Get Device Details

GET /api/devices/{device_id}

### Get All Devices

GET /api/devices

Query Parameters:

- status (optional): Filter by device status (active/inactive/maintenance)
- search (optional): Search term for device name or ID
- page (optional): Page number for pagination (default: 1)
- per_page (optional): Number of items per page (default: 10)

Response Success (200):

```json
{
  "success": true,
  "data": {
  "devices": [
          {
            "id": integer,
            "device_id": string,
            "name": string,
            "model": string,
            "status": string,
            "last_calibration": datetime,
            "next_calibration": datetime,
            "registered_by": integer,
            "created_at": datetime
          }
        ],
        "pagination": {
            "total_items": integer,
            "total_pages": integer,
            "current_page": integer,
            "per_page": integer,
            "has_next": boolean,
            "has_prev": boolean
        }
  }
}
```

Response Error (400):

```json
{
  "success": false,
  "message": string
}
```

## Measurements

### Create Measurement

Create a new alcohol measurement record.

```http
POST /measurements
Authorization: Bearer <token>
Content-Type: application/json

{
    "device_id": "integer",
    "subject_name": "string",
    "subject_id": "string",
    "subject_age": integer,
    "alcohol_level": float,
    "location": "string",
    "location_coordinates": "string" (optional)
}
```

**Response Success (201)**

```json
{
    "success": true,
    "message": "Measurement recorded successfully",
    "data": {
        "id": integer,
        "violation_level": "none|low|high",
        "violation": {
            "level": "string",
            "fine_amount": float
        }
    }
}
```

### Get Measurements

Get list of measurements.

```http
GET /measurements
Authorization: Bearer <token>
```

**Response Success (200)**

```json
{
    "success": true,
    "data": [
        {
            "id": integer,
            "device_id": "string",
            "subject_name": "string",
            "alcohol_level": float,
            "violation_level": "string",
            "test_time": "datetime",
            "location": "string"
        }
    ]
}
```

## Statistics

### Get Overall Statistics

Get system statistics.

```http
GET /statistics
Authorization: Bearer <token>
Query Parameters:
  - range: "week|month|year" (default: week)
```

**Response Success (200)**

```json
{
    "success": true,
    "data": {
        "total_tests": integer,
        "total_violations": integer,
        "violation_levels": {
            "none": integer,
            "low": integer,
            "high": integer
        },
        "total_fines": float,
        "paid_fines": float,
        "age_distribution": {
            "18-25": integer,
            "26-35": integer,
            "36-45": integer,
            "46-55": integer,
            "55+": integer
        },
        "time_distribution": {
            "morning": integer,
            "afternoon": integer,
            "evening": integer,
            "night": integer
        }
    }
}
```

### Get Violation Statistics

Get detailed violation statistics.

```http
GET /statistics/violations
Authorization: Bearer <token>
Query Parameters:
  - start_date: "YYYY-MM-DD" (optional)
  - end_date: "YYYY-MM-DD" (optional)
```

**Response Success (200)**

```json
{
    "success": true,
    "data": {
        "total": integer,
        "by_level": {
            "low": integer,
            "high": integer
        },
        "total_fines": float,
        "paid_fines": float
    }
}
```

## Error Responses

### Common Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

### Error Response Format

```json
{
  "success": false,
  "message": "Error description"
}
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require JWT authentication.

Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Rate Limits

- Authentication endpoints: 5 requests per minute
- Other endpoints: 60 requests per minute per user

## Data Constraints

### User Roles

- admin: Full system access
- officer: Can create measurements and view statistics
- user: Limited access (view only)

### Violation Levels

- none: alcohol_level < 0.2
- low: 0.2 ≤ alcohol_level ≤ 0.4
- high: alcohol_level > 0.4

### Fine Amounts

- low violation: 2,500,000 VND
- high violation: 5,000,000 VND

## Examples

### Register User Example

```bash
curl -X POST http://localhost:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
    "username": "officer1",
    "password": "Officer123!",
    "email": "officer@example.com",
    "full_name": "Test Officer",
    "role": "officer"
}'
```

### Create Measurement Example

```bash
curl -X POST http://localhost:5000/api/measurements \
-H "Authorization: Bearer <your_token>" \
-H "Content-Type: application/json" \
-d '{
    "device_id": "DEV-001",
    "subject_name": "Nguyen Van A",
    "subject_id": "123456789",
    "subject_age": 30,
    "alcohol_level": 0.35,
    "location": "Ha Noi"
}'
```
