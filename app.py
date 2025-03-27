from flask import Flask, request, render_template, send_file
from rembg import remove
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = 'output.png'
        
        file.save(input_path)
        
        with open(input_path, 'rb') as i:
            input_image = i.read()
            output = remove(input_image)
            
        with open(output_path, 'wb') as o:
            o.write(output)
        
        return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
