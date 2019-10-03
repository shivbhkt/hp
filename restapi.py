#import json
import xlrd
#from collections import OrderedDict
import os
from flask import Flask,flash, request, render_template, redirect, url_for, jsonify, make_response
import requests
from werkzeug import secure_filename
import pandas as pd
import json
from projectvalidation import signupSchema
from jsonschema import validate
from jsonschema.exceptions import ValidationError

app = Flask(__name__) 

UPLOAD_FOLDER=r'C:\Users\argautam\Environment\project\content'
ALLOWED_EXTENSIONS = {'txt', 'xlsx', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 
@app.route('/upload')  
def starting():  
    return render_template("upload.html") 


@app.route('/myapi', methods=['POST'])
def post():
    values = request.json
    
    if validate(instance=values, schema=signupSchema):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status" : ValidationError})

    


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
   
    
        # check if the post request has the file part
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            myfile = os.path.join(app.config['UPLOAD_FOLDER'])+ "\\" +filename
            in_df = pd.read_excel(myfile)
            df_mapping = pd.read_excel(r'C:\Users\argautam\Environment\project\mapping.xlsx')
            in_df['Output'] = df_mapping['Output']
            raw = in_df.to_dict(orient='records')
            #data = json.dumps(raw)
            
            return make_response(jsonify({"raw":raw, "stats" : "here is the json"},200))
            
            
            
                

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
      
if __name__ == '__main__':  
   app.run(debug = True)