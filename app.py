from flask import Flask, request, jsonify
from rembg import remove
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        # Get image data from POST request
        image_data = request.files['image'].read()
        
        # Remove background
        output = remove(image_data)
        
        # Convert to base64 for returning to frontend
        buffered = BytesIO()
        Image.open(BytesIO(output)).save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'result': img_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
