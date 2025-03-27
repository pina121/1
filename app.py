import io
from rembg import remove
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None  # Initialize error message

    if request.method == 'POST':
        if 'file' not in request.files:
            error_message = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                error_message = 'No selected file'
            else:
                try:
                    input_image = file.read()
                    output = remove(input_image)
                    return send_file(io.BytesIO(output), mimetype='image/png', as_attachment=True, download_name='output.png')
                except Exception as e:
                    error_message = f"Failed to remove background. Please try again. Error: {str(e)}"

    return render_template('index.html', error=error_message) # Pass error message to template

if __name__ == '__main__':
    app.run(debug=True)
