"""
Monitor Brightness API Server
REST API for controlling monitor brightness
"""
from flask import Flask, jsonify, request
from brightness_controller import BrightnessController

app = Flask(__name__)
controller = BrightnessController()


@app.route('/api/brightness', methods=['GET'])
def get_brightness():
    """
    Get current monitor brightness level
    Returns: JSON with brightness level (0-100) or error
    """
    try:
        brightness = controller.get_brightness()
        if brightness is None:
            return jsonify({
                'success': False,
                'error': 'Unable to get brightness level'
            }), 500
        
        return jsonify({
            'success': True,
            'brightness': brightness
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/brightness', methods=['POST'])
def set_brightness():
    """
    Set monitor brightness level
    Request body: {"brightness": 0-100}
    Returns: JSON with success status
    """
    try:
        data = request.get_json()
        if not data or 'brightness' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing brightness parameter'
            }), 400
        
        brightness = data['brightness']
        
        # Validate brightness value
        try:
            brightness = float(brightness)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Brightness must be a number'
            }), 400
        
        if brightness < 0 or brightness > 100:
            return jsonify({
                'success': False,
                'error': 'Brightness must be between 0 and 100'
            }), 400
        
        # Set brightness
        result = controller.set_brightness(brightness)
        if not result:
            return jsonify({
                'success': False,
                'error': 'Failed to set brightness'
            }), 500
        
        return jsonify({
            'success': True,
            'brightness': brightness,
            'message': f'Brightness set to {brightness}%'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/monitors', methods=['GET'])
def list_monitors():
    """
    List available monitors
    Returns: JSON with list of monitors
    """
    try:
        monitors = controller.list_monitors()
        return jsonify({
            'success': True,
            'monitors': monitors,
            'count': len(monitors)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Returns: JSON with server status
    """
    return jsonify({
        'success': True,
        'status': 'healthy',
        'platform': controller.system
    }), 200


@app.route('/', methods=['GET'])
def index():
    """
    API documentation endpoint
    Returns: JSON with available endpoints
    """
    return jsonify({
        'name': 'Monitor Brightness API',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'API documentation',
            'GET /api/health': 'Health check',
            'GET /api/brightness': 'Get current brightness level',
            'POST /api/brightness': 'Set brightness level (body: {"brightness": 0-100})',
            'GET /api/monitors': 'List available monitors'
        }
    }), 200


if __name__ == '__main__':
    import sys
    
    # Default configuration
    host = '0.0.0.0'
    port = 5000
    debug = False
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--port='):
                port = int(arg.split('=')[1])
            elif arg.startswith('--host='):
                host = arg.split('=')[1]
            elif arg == '--debug':
                debug = True
    
    print(f"Starting Monitor Brightness API Server on {host}:{port}")
    print(f"Platform: {controller.system}")
    print(f"API documentation: http://{host}:{port}/")
    
    app.run(host=host, port=port, debug=debug)
