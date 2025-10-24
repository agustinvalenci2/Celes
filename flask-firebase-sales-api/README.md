# Flask Firebase Sales API

This project is a Flask application integrated with Firebase to manage and consult sales data. It provides various endpoints to retrieve sales information based on different criteria, including employee, product, and store. Additionally, it includes JWT authentication for secure access to the API.

## Features

- Consult sales in a specified period by employee.
- Consult sales in a specified period by product.
- Consult sales in a specified period by store.
- Retrieve total and average sales by store.
- Retrieve total and average sales by product.
- Retrieve total and average sales by employee.
- JWT authentication for secure API access.

## Project Structure

```
flask-firebase-sales-api
├── src
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── sales_routes.py
│   │   └── auth_routes.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── sales_controller.py
│   │   └── auth_controller.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── firebase_service.py
│   │   └── jwt_service.py
│   ├── middleware
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── tests
│   ├── __init__.py
│   ├── test_sales_routes.py
│   ├── test_auth_routes.py
│   └── test_firebase_service.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-firebase-sales-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Copy `.env.example` to `.env` and fill in the necessary values for your Firebase and JWT configurations.

## Usage

To run the application, execute the following command:
```
python src/app.py
```

The API will be available at `http://localhost:5000`.

### Authentication

First, obtain a JWT token by logging in:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpassword"}'
```

Use the returned token in the Authorization header for all subsequent requests:
```
Authorization: Bearer <your_jwt_token>
```

### API Endpoints

All sales endpoints require authentication and accept the following query parameters:
- `key`: Employee/Product identifier
- `start`: Start date (YYYY-MM-DD format)
- `end`: End date (YYYY-MM-DD format)

#### Employee Sales Endpoints

**Get employee sales data:**
```
GET http://localhost:5000/api/sales/employee?key=118355&start=2023-01-01&end=2023-12-31
```

**Get employee sales metrics (totals and averages):**
```
GET http://localhost:5000/api/sales/employee/metrics?key=118355&start=2023-01-01&end=2023-12-31
```

#### Product Sales Endpoints

**Get product sales data:**
```
GET http://localhost:5000/api/sales/product?key=1|023&start=2000-01-01&end=2025-12-31
```

**Get product sales metrics (totals and averages):**
```
GET http://localhost:5000/api/sales/product/metrics?key=1|023&start=2000-01-01&end=2025-12-31
```

#### Example using curl:

```bash
# 1. Login to get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpassword"}' | jq -r '.token')

# 2. Get employee sales
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5000/api/sales/employee?key=118355&start=2023-01-01&end=2023-12-31"

# 3. Get employee metrics
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5000/api/sales/employee/metrics?key=118355&start=2023-01-01&end=2023-12-31"
```

#### Example using PowerShell:

```powershell
# 1. Login to get token
$loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" -Method POST -ContentType "application/json" -Body '{"username":"testuser","password":"testpassword"}'
$token = $loginResponse.token

# 2. Set authorization header
$headers = @{ "Authorization" = "Bearer $token" }

# 3. Get employee sales
Invoke-RestMethod -Uri "http://localhost:5000/api/sales/employee?key=118355&start=2023-01-01&end=2023-12-31" -Headers $headers

# 4. Get product metrics
Invoke-RestMethod -Uri "http://localhost:5000/api/sales/product/metrics?key=1|023&start=2000-01-01&end=2025-12-31" -Headers $headers
```

## Testing

To run the unit tests, use:
```
pytest tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.