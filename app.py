from flask import Flask, request, jsonify, send_file
import base64
import io
import os
from rembg import remove
from PIL import Image
import uuid

app = Flask(__name__, static_folder='.', static_url_path='')

# Create a temporary directory for storing processed images
TEMP_DIR = 'temp'
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Get the image file from the request
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})
        
        file = request.files['image']
        
        # Read the image
        input_image = file.read()
        
        # Process the image with rembg
        output = remove(input_image)
        
        # Convert to base64 for sending back to client
        output_base64 = base64.b64encode(output).decode('utf-8')
        
        # Generate a unique ID for this processed image
        image_id = str(uuid.uuid4())
        
        # Save the processed image temporarily
        output_path = os.path.join(TEMP_DIR, f'{image_id}.png')
        with open(output_path, 'wb') as f:
            f.write(output)
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{output_base64}',
            'image_id': image_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download-image', methods=['POST'])
def download_image():
    try:
        data = request.json
        
        # Check if we're getting a data URL or an image ID
        if 'image' in data and data['image'].startswith('data:image/'):
            # Extract the base64 data from the data URL
            image_data = data['image'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            # Create a BytesIO object for sending the file
            img_io = io.BytesIO(image_bytes)
            img_io.seek(0)
            
            return send_file(
                img_io,
                mimetype='image/png',
                as_attachment=True,
                download_name='background-removed.png'
            )
        
        elif 'image_id' in data:
            # Get the image from the temp directory
            image_path = os.path.join(TEMP_DIR, f"{data['image_id']}.png")
            
            if not os.path.exists(image_path):
                return jsonify({'success': False, 'error': 'Image not found'})
            
            return send_file(
                image_path,
                mimetype='image/png',
                as_attachment=True,
                download_name='background-removed.png'
            )
        
        else:
            return jsonify({'success': False, 'error': 'Invalid request'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
