# Monitor Brightness API

控制显示器亮度 / Control Monitor Brightness

A cross-platform REST API for controlling monitor brightness levels. Supports Windows, Linux, and macOS.

## Features

- 🌐 REST API for easy integration
- 🖥️ Cross-platform support (Windows, Linux, macOS)
- 📊 Get current brightness level
- ⚙️ Set brightness level (0-100)
- 📋 List available monitors
- 🔍 Health check endpoint

## Installation

### Requirements

- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/fschenkun22/monitor_bright.git
cd monitor_bright
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Platform-specific Requirements

**Windows:**
- WMI and pywin32 are automatically installed from requirements.txt
- Administrator privileges may be required

**Linux:**
- xrandr (usually pre-installed)
- Or sysfs backlight interface access

**macOS:**
- `brightness` command-line tool (install with `brew install brightness`)

## Usage

### Start the Server

```bash
python app.py
```

By default, the server runs on `http://0.0.0.0:5000`

#### Command Line Options

```bash
python app.py --port=8080 --host=127.0.0.1 --debug
```

Options:
- `--port=PORT`: Specify port number (default: 5000)
- `--host=HOST`: Specify host (default: 0.0.0.0)
- `--debug`: Enable debug mode

## API Endpoints

### 1. Get API Documentation

```http
GET /
```

Returns information about available endpoints.

**Example:**
```bash
curl http://localhost:5000/
```

### 2. Health Check

```http
GET /api/health
```

Returns server health status and platform information.

**Example:**
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "platform": "Linux"
}
```

### 3. Get Current Brightness

```http
GET /api/brightness
```

Returns the current brightness level (0-100).

**Example:**
```bash
curl http://localhost:5000/api/brightness
```

**Response:**
```json
{
  "success": true,
  "brightness": 75
}
```

### 4. Set Brightness

```http
POST /api/brightness
Content-Type: application/json
```

Sets the brightness level to a value between 0 and 100.

**Request Body:**
```json
{
  "brightness": 50
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 50}'
```

**Response:**
```json
{
  "success": true,
  "brightness": 50,
  "message": "Brightness set to 50%"
}
```

### 5. List Monitors

```http
GET /api/monitors
```

Returns a list of available monitors.

**Example:**
```bash
curl http://localhost:5000/api/monitors
```

**Response:**
```json
{
  "success": true,
  "monitors": [
    {
      "id": 0,
      "name": "Monitor 0",
      "current_brightness": 75
    }
  ],
  "count": 1
}
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

- `200 OK`: Success
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Server or platform error

**Error Response Format:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Examples

### Python Client Example

```python
import requests

# Get current brightness
response = requests.get('http://localhost:5000/api/brightness')
print(response.json())

# Set brightness to 80%
response = requests.post(
    'http://localhost:5000/api/brightness',
    json={'brightness': 80}
)
print(response.json())

# List monitors
response = requests.get('http://localhost:5000/api/monitors')
print(response.json())
```

### JavaScript Client Example

```javascript
// Get current brightness
fetch('http://localhost:5000/api/brightness')
  .then(response => response.json())
  .then(data => console.log(data));

// Set brightness to 80%
fetch('http://localhost:5000/api/brightness', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ brightness: 80 }),
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Troubleshooting

### Windows
- If you get permission errors, try running as Administrator
- Ensure WMI service is running

### Linux
- If xrandr doesn't work, check if your system uses sysfs backlight interface
- You may need sudo access for sysfs brightness control

### macOS
- Install brightness tool: `brew install brightness`
- Check if the tool is in your PATH

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
