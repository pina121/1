from flask import Flask, request, send_file, render_template
from rembg import remove
from io import BytesIO
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    # Read and process the image
    input_image = file.read()
    output_image = remove(input_image)
    
    # Prepare the processed image for download
    output = BytesIO(output_image)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='image/png',
        as_attachment=True,
        download_name='output.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
