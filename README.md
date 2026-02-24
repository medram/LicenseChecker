# License Checker

A Django-based license validation system with Envato integration. This application provides a REST API for validating software licenses, managing domains, and tracking license usage.

## Features

- 🔐 **License Validation**: Verify software licenses through Envato API integration
- 🌐 **Domain Management**: Track and manage licensed domains
- 📊 **Usage Analytics**: Monitor license checks and usage statistics
- 🔑 **API Key Authentication**: Secure API endpoints with key-based authentication
- 🎯 **Multiple License Types**: Support for Regular and Extended licenses
- ⚙️ **Flexible License Control**: Force override option for custom licenses
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📈 **Admin Interface**: Django admin panel for license management

## Requirements

- Python 3.8+
- Django 4.0+
- Docker (optional, for containerized deployment)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/medram/LicenseChecker.git
cd LicenseChecker
```

2. Copy the environment file and configure it:
```bash
cp .env.example .env
```

3. Edit `.env` file with your settings:
```env
DEBUG=0
ALLOWED_HOSTS="*"
CSRF_TRUSTED_ORIGINS=
ENVATO_TOKEN=your_envato_token_here
```

4. Build and run with Docker:
```bash
docker build -t license-checker .
docker run -p 8000:80 -v $(pwd):/app license-checker
```

Or use Docker Compose for development:
```bash
docker-compose -f docker-compose.dev.yml up
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/medram/LicenseChecker.git
cd LicenseChecker
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Configuration

### Environment Variables

- `DEBUG`: Enable/disable debug mode (0 or 1)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins for CSRF
- `ENVATO_TOKEN`: Your Envato API token for license verification

### Getting an Envato Token

1. Log in to your Envato account
2. Go to Settings → API Keys
3. Create a new token with the necessary permissions
4. Add the token to your `.env` file

## Usage

### Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to manage:
- Applications (with API keys and Envato App IDs)
- Licenses (license codes, types, and statuses)
- Domains (licensed domains and their usage)

### API Endpoints

#### Check License

**Endpoint**: `POST /api/check_license/`

**Authentication**: Requires API key in the request header

**Request Headers**:
```
X-API-Key: your_api_key_here
```

**Request Body** (JSON or Form Data):
```json
{
  "license_code": "your-license-code-here",
  "host": "example.com"
}
```

**Success Response** (200 OK):
```json
{
  "status": "ACTIVE",
  "license_type": "REGULAR LICENSE",
  "message": "This license code is valid",
  "hash": "random_hash_here"
}
```

**Error Response** (403 Forbidden):
```json
{
  "status": "INACTIVE",
  "message": "Invalid License, please ensure you've inserted a correct license code, or contact the support for help.",
  "hash": "random_hash_here"
}
```

**Banned License Response**:
```json
{
  "status": "BANNED",
  "license_type": "REGULAR LICENSE",
  "message": "Invalid License, probably has been blacklisted!, for more info please contact the support.",
  "hash": "random_hash_here"
}
```

#### Health Check

**Endpoint**: `GET /api/is_up/`

**Response**:
```json
{
  "is_up": true
}
```

### Example Usage

#### Python
```python
import requests

url = "http://localhost:8000/api/check_license/"
headers = {"X-API-Key": "your_api_key"}
data = {
    "license_code": "your-license-code",
    "host": "example.com"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### cURL
```bash
curl -X POST http://localhost:8000/api/check_license/ \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"license_code": "your-license-code", "host": "example.com"}'
```

#### JavaScript (Fetch API)
```javascript
const checkLicense = async (licenseCode, host) => {
  const response = await fetch('http://localhost:8000/api/check_license/', {
    method: 'POST',
    headers: {
      'X-API-Key': 'your_api_key',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      license_code: licenseCode,
      host: host
    })
  });
  
  return await response.json();
};
```

## License Status

The system supports three license statuses:
- **ACTIVE**: License is valid and can be used
- **INACTIVE**: License is not active or invalid
- **BANNED**: License has been blacklisted

## License Types

- **Regular License**: Standard license for single use
- **Extended License**: Extended license with additional rights

## Docker Deployment

### Production Deployment

The application includes a production-ready Dockerfile with:
- Python 3.8 slim base image
- Gunicorn WSGI server
- Health check endpoint
- Volume support for persistent data
- Non-root user execution

**Environment Variables for Docker**:
- `WORKERS`: Number of Gunicorn workers (default: 3)
- `PORT`: Application port (default: 80)

### Health Check

The Docker container includes a health check that monitors the admin login page:
```bash
curl -fsSLI http://127.0.0.1:80/admin/login/
```

## Development

### Project Structure

```
LicenseChecker/
├── app/                    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── license_checker/        # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── admin.py           # Admin configuration
│   ├── decorators.py      # Custom decorators
│   └── common.py          # Utility functions
├── Dockerfile             # Docker configuration
├── docker-compose.dev.yml # Docker Compose for development
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── .env.example          # Environment variables template
```

### Models

- **App**: Application model with API key and Envato app ID
- **License**: License model with code, type, status, and tracking
- **Domain**: Domain model linked to licenses for domain tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/medram/LicenseChecker).

## License

This project is available under the MIT License or as specified by the repository owner.
