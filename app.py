from flask import Flask, render_template, request
from numpy import Inf
from src import models,predict
import os 
import shutil

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

model_name = models.Models()

model = predict.Model(name=model_name.default)
test = model.infer('samples/730394.jpg')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/infer', methods=['POST','GET'])
def success():
    if request.method == 'POST':
        try:
            f = request.files['file']
            saveLocation = f.filename
            f.save(saveLocation)
     
            inference  = model.infer(saveLocation)
   
            # make a percentage with 2 decimal points

            # delete file after making an inference
            im_PATH = model.wd/'saved_images'
            im_PATH = im_PATH/saveLocation
        
            shutil.move(saveLocation, im_PATH)
            # respond with the inference
            return render_template('inference.html', name=round(float(inference[0][1]),2), confidence=round(float(inference[0][0]),2))
        except:
            return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)