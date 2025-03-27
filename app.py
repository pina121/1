import os
from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # Process the image
    input_image = file.read()
    try:
        # Remove background
        output = remove(input_image)
        
        # Return the processed image
        return send_file(
            BytesIO(output),
            mimetype='image/png',
            as_attachment=True,
            download_name='output.png'
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
