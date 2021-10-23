
#Import Packages

import os
from flask import Flask, render_template, request
from google.cloud.vision import Image, ImageAnnotatorClient
import io

#Service Account file in json(API KEY)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'SERVICE ACCOUNT API KEY '

#Initializing Flask app
app = Flask(__name__)

#Define allowed extensions
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Create path to stock images uploaded
path = os.getcwd()

UPLOAD_FOLDER = './uploads'
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def detect_text():
    
    
    #"""Detects text in the file."""
    
    client = ImageAnnotatorClient()
    
    #Check if the request method is post
    if request.method == 'POST':
        #Check if the files are selected
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']

    #Check if the files are uploaded
    if file.filename == '':
        return render_template('index.html', msg='No file')

    # [START vision_python_migration_text_detection]
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        with io.open(app.config['UPLOAD_FOLDER'] + file.filename, 'rb') as image_file:    
            content = image_file.read()
        

        image = Image(content=content)

        response = client.text_detection(image=image)

        extracted = ''
        for text in response.text_annotations:
            extracted = extracted + ' ' +text.description
    
        return render_template('index.html',
                               msg='OCR completed',
                               img_src=UPLOAD_FOLDER + file.filename)
    else:
        return render_template('index.html')

    
if __name__ == "__main__":
    

    app.run("localhost", 5000, threaded=True, debug=True)
