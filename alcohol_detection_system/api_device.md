# Device Management API Documentation

## Base URL

```
http://localhost:5000/api/devices
```

## Authentication

All endpoints require JWT Authentication:

```
Authorization: Bearer <token>
```

## Endpoints

### 1. Register Device

Create a new device in the system.

```http
POST /register
Content-Type: application/json
Authorization: Bearer <token>

Request Body:
{
    "device_id": "string",     // Required, unique identifier
    "name": "string",          // Required, device name
    "model": "string"          // Optional, device model
}

Response Success (201):
{
    "success": true,
    "message": "Device registered successfully",
    "data": {
        "device_id": "string",
        "name": "string"
    }
}

Response Error (400):
{
    "success": false,
    "message": "Device already registered"
}
```

### 2. Get All Devices

Retrieve a list of devices with filtering and pagination.

```http
GET /?status=string&search=string&page=number&per_page=number
Authorization: Bearer <token>

Query Parameters:
- status: Filter by device status (active|inactive|maintenance)
- search: Search in device name or device_id
- page: Page number (default: 1)
- per_page: Items per page (default: 10)

Response Success (200):
{
    "success": true,
    "data": {
        "devices": [
            {
                "id": number,
                "device_id": "string",
                "name": "string",
                "model": "string",
                "status": "string",
                "last_calibration": "datetime",
                "next_calibration": "datetime",
                "registered_by": number,
                "created_at": "datetime"
            }
        ],
        "pagination": {
            "total_items": number,
            "total_pages": number,
            "current_page": number,
            "per_page": number,
            "has_next": boolean,
            "has_prev": boolean
        }
    }
}
```

### 3. Check Device Status

Check status and information of a specific device.

```http
GET /check/{device_id}
Authorization: Bearer <token>

Response Success (200):
{
    "success": true,
    "data": {
        "exists": true,
        "device_id": "string",
        "device_name": "string",
        "status": "string",
        "last_calibration": "datetime",
        "next_calibration": "datetime"
    }
}

Response Error (404):
{
    "success": false,
    "data": {
        "exists": false
    }
}
```

### 4. Update Device Status

Update the status of a specific device.

```http
PUT /{device_id}/status
Content-Type: application/json
Authorization: Bearer <token>

Request Body:
{
    "status": "string"  // active|inactive|maintenance
}

Response Success (200):
{
    "success": true,
    "message": "Device status updated successfully",
    "data": {
        "device_id": "string",
        "status": "string",
        "updated_at": "datetime"
    }
}
```

### 5. Update Device Calibration

Update calibration information for a device.

```http
POST /{device_id}/calibration
Authorization: Bearer <token>

Response Success (200):
{
    "success": true,
    "message": "Device calibration updated successfully",
    "data": {
        "device_id": "string",
        "last_calibration": "datetime",
        "next_calibration": "datetime"
    }
}
```

### 6. Get Devices Needing Calibration

Get a list of devices that need calibration.

```http
GET /calibration/needed
Authorization: Bearer <token>

Response Success (200):
{
    "success": true,
    "data": [
        {
            "device_id": "string",
            "name": "string",
            "last_calibration": "datetime",
            "next_calibration": "datetime",
            "days_overdue": number
        }
    ]
}
```

### 7. Get Device Statistics

Get statistical information about devices.

```http
GET /statistics
Authorization: Bearer <token>

Response Success (200):
{
    "success": true,
    "data": {
        "total_devices": number,
        "active_devices": number,
        "maintenance_devices": number,
        "devices_need_calibration": number
    }
}
```

### 8. Update Device Information

Update general information of a device.

```http
PUT /{device_id}
Content-Type: application/json
Authorization: Bearer <token>

Request Body:
{
    "name": "string",
    "model": "string",
    "status": "string"
}

Response Success (200):
{
    "success": true,
    "message": "Device updated successfully",
    "data": {
        "device_id": "string",
        "name": "string",
        "model": "string",
        "status": "string",
        "updated_at": "datetime"
    }
}
```

### 9. Delete Device

Remove a device from the system.

```http
DELETE /{device_id}
Authorization: Bearer <token>

Response Success (200):
{
    "success": true,
    "message": "Device deleted successfully"
}
```

## Error Responses

All endpoints may return these common errors:

```http
401 Unauthorized:
{
    "success": false,
    "message": "Missing or invalid authentication token"
}

403 Forbidden:
{
    "success": false,
    "message": "Insufficient permissions"
}

404 Not Found:
{
    "success": false,
    "message": "Device not found"
}

500 Internal Server Error:
{
    "success": false,
    "message": "Internal server error message"
}
```

## Data Constraints

### Device Status Values

- `active`: Device is operational
- `inactive`: Device is not in use
- `maintenance`: Device is under maintenance

### Calibration

- Calibration period: 180 days
- Devices need calibration when current date > next_calibration date

### Pagination

- Default page size: 10 items
- Maximum page size: 100 items
- Page numbers start from 1

## Usage Examples

### Register a new device:

```bash
curl -X POST http://localhost:5000/api/devices/register \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
    "device_id": "DEV-001",
    "name": "Test Device 1",
    "model": "Model X1"
}'
```

### Get devices with filters:

```bash
curl -X GET "http://localhost:5000/api/devices?status=active&search=test&page=1" \
-H "Authorization: Bearer <token>"
```

### Update device status:

```bash
curl -X PUT http://localhost:5000/api/devices/DEV-001/status \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
    "status": "maintenance"
}'
```
