from flask import Flask, render_template, request
from numpy import Inf
from src import models,predict
import os 

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

model_name = models.Models()

model = predict.Model(name=model_name.default)
test = model.infer('uploads/730394.jpg')
print(test)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/infer', methods=['POST'])
def success():
    if request.method == 'POST':
        try:
            f = request.files['file']
            saveLocation = f.filename
            f.save(saveLocation)
            print(saveLocation)
            inference  = model.infer(saveLocation)
            print(inference)
            # make a percentage with 2 decimal points

            # delete file after making an inference
            #os.remove(saveLocation)
            # respond with the inference
            return render_template('inference.html', name=round(float(inference[0][1]),2), confidence=round(float(inference[0][0]),2))
        except:
            return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=False)