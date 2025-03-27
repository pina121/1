import io
from rembg import remove
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            try:
                input_image = file.read()
                output = remove(input_image)
                return send_file(io.BytesIO(output), mimetype='image/png', as_attachment=True, download_name='output.png')
            except Exception as e:
                return f"An error occurred: {str(e)}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
