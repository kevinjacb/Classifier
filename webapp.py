from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import os
predictor = load_model('/Users/athuls/Desktop/chakka manga classifier/model')
classes = {0:'Mango',1:'Jack Fruit'}

app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('web_app.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
       try:
           f = request.files['file']
           f.save(secure_filename(f.filename))
           img = Image.open(f)
           os.remove(f.filename)
           img = img.resize((28,28))
           img_array = np.array(img).reshape((1,28,28,3))
           img_array = img_array/255
           prediction = predictor.predict(img_array)
           
           if prediction <= 0.5: return 'You have Uploaded an Mango Image'
           else: return 'You have uploaded an Jack Fruit Image'

       except:
           return 'Error Occured'
if __name__ == '__main__':
   app.run(debug = True)