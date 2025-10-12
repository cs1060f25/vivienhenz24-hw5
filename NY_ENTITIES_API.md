# New York Entities API Documentation

## Overview
The HTTP server has been extended to support filing and retrieving New York State corporations and LLCs.

## Authentication
All endpoints require HTTP Basic Authentication with username and password (default: `admin:admin`).

## Endpoints

### General
- **GET /** - Health check endpoint, returns `success`

### Corporations

#### File a Corporation
- **POST /file/corporation**
- Files a new Certificate of Incorporation under Section 402 of the Business Corporation Law
- **Request Body (JSON):**
  ```json
  {
    "name": "Company Name",
    "county": "COUNTY NAME",
    "address": "Full registered address",
    "incorporator": "Incorporator Name",
    "incorporator_address": "Incorporator address (optional, defaults to company address)",
    "shares": 1000,
    "par_value": "0.01",
    "purpose": "Business purpose (optional)"
  }
  ```
- **Response:** Returns the filed certificate with filing date and status

#### List All Corporations
- **GET /corporations**
- Returns a list of all filed corporation names and count

#### Get Corporation Details
- **GET /corporation/{name}**
- Returns the complete certificate for a specific corporation
- URL encode the company name (e.g., `Test%20Company`)

### Limited Liability Companies (LLCs)

#### File an LLC
- **POST /file/llc**
- Files new Articles of Organization under Section 203 of the Limited Liability Company Law
- **Request Body (JSON):**
  ```json
  {
    "name": "Company Name",
    "county": "COUNTY NAME",
    "address": "Full registered address",
    "organizer": "Organizer Name",
    "organizer_address": "Organizer address (optional, defaults to company address)",
    "email": "contact@example.com (optional)"
  }
  ```
- **Response:** Returns the filed articles with filing date and status

#### List All LLCs
- **GET /llcs**
- Returns a list of all filed LLC names and count

#### Get LLC Details
- **GET /llc/{name}**
- Returns the complete articles for a specific LLC
- URL encode the company name (e.g., `Test%20Company`)

## Example Usage

### Start the Server
```bash
cd hw5_server
python3 http_server.py --port 8080 --username admin --password admin
```

### File a Corporation
```bash
curl -u admin:admin -X POST \
  -H "Content-Type: application/json" \
  -d @example_corporation.json \
  http://localhost:8080/file/corporation
```

### File an LLC
```bash
curl -u admin:admin -X POST \
  -H "Content-Type: application/json" \
  -d @example_llc.json \
  http://localhost:8080/file/llc
```

### List All Corporations
```bash
curl -u admin:admin http://localhost:8080/corporations
```

### Get Specific Corporation
```bash
curl -u admin:admin "http://localhost:8080/corporation/Test%20Company"
```

### List All LLCs
```bash
curl -u admin:admin http://localhost:8080/llcs
```

### Get Specific LLC
```bash
curl -u admin:admin "http://localhost:8080/llc/Test%20Company"
```

## Certificate Structure

### Corporation Certificate
Based on NY DOS Form 1239-f (Certificate of Incorporation):
- Document Type: CERTIFICATE OF INCORPORATION
- Law Section: Section 402 of the Business Corporation Law
- Fields: name, purpose, county, shares, par_value, registered_agent, address, incorporator, incorporator_address, filed_date, status

### LLC Articles
Based on NY DOS Form 1336-f (Articles of Organization):
- Document Type: ARTICLES OF ORGANIZATION
- Law Section: Section 203 of the Limited Liability Company Law
- Fields: name, county, registered_agent, address, organizer, organizer_address, email, filed_date, status

## Data Storage
All entities are stored in-memory and will be lost when the server restarts. This is a prototype implementation suitable for testing and development.

## Error Handling
- **400 Bad Request**: Missing required fields or invalid JSON
- **401 Unauthorized**: Invalid or missing authentication
- **404 Not Found**: Entity not found or invalid endpoint
- **201 Created**: Entity successfully filed

## Legal References
- [NY Business Corporation Law Section 402](https://dos.ny.gov)
- [NY Limited Liability Company Law Section 203](https://dos.ny.gov)
- NY DOS Form 1239-f: Certificate of Incorporation
- NY DOS Form 1336-f: Articles of Organization

