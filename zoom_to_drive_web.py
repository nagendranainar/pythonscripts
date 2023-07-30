from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    script = request.form['kathak_upload.py']
    output = subprocess.check_output(['python', '-c', script])
    return render_template('index.html', output=output.decode())

if __name__ == '__main__':
    app.run(debug=True)
