import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, safe_join, jsonify
from werkzeug.utils import secure_filename
from passporteye import read_mrz
import country_converter as coco
import datetime
import json
from PIL import Image
import numpy as np
# from flask_dropzone import Dropzone

# UPLOAD_FOLDER stores uploaded files
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app = Flask(__name__)
app.secret_key = "ETYTEYVSG%^@%&!*|}|}|}|||}"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

now = datetime.datetime.now()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
'''
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file. browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # secure_filename secures a filename before storing it directly to the filesystem.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # redirect() returns a response object and redirects the user to another target location with specified status code.
            filename1 = safe_join(app.config['UPLOAD_FOLDER'], filename)
            mrz1 = read_mrz(filename1)
            mrz = mrz1.to_dict()
            #return redirect(url_for('mrz', filename=filename))
            return render_template('test.html', mrz=mrz)

    
    #file = request.files['file']
    #f = file.filename
    
    # x = file1.filename
    # f = uploaded_file(file)
    # f = send_from_directory(app.config['UPLOAD_FOLDER'], file)
    # mrz1 = read_mrz(f)
    # mrz = mrz1.to_dict()
    print(mrz)
    #return render_template('upload.html')
    return mrz

'''
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/uploadajax', methods=[ "GET", 'POST'])
def load_file():
    # file_val = request.files.get('file')
    #read_mrz(file_val)
    #if request.method == 'POST':
        # print(read_mrz(file_val))
    # print(read_mrz(file_val))
    # return render_template('tests.html')
    # return file_val
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file. browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # secure_filename secures a filename before storing it directly to the filesystem.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # redirect() returns a response object and redirects the user to another target location with specified status code.
            filename1 = safe_join(app.config['UPLOAD_FOLDER'], filename)
            mrz1 = read_mrz(filename1, save_roi=True)
            mrz = mrz1.to_dict()
            
            # Converting sex output
            if mrz['sex'] == 'F':
                mrz['sex'] = 'Female'
            elif mrz['sex'] == 'M':
                mrz['sex'] = 'Male'
            else:
                mrz['sex'] = 'Unknown'
            
            # Converting country output
            if coco.convert(names=mrz['country'], to='name_short') == 'not found':
                mrz['country'] = mrz['country']
            else:
                mrz['country'] = coco.convert(names=mrz['country'], to='name_short')
            
            # Converting nationality output
            if coco.convert(names=mrz['nationality'], to='name_short') == 'not found':
                mrz['nationality'] = mrz['nationality']
            else:
                mrz['nationality'] = coco.convert(names=mrz['nationality'], to='name_short')
            
            # Converting date of birth output
            try:
                dd = datetime.datetime.strptime(mrz['date_of_birth'],'%y%m%d').date()
                if dd.year > now.year:
                    mrz['date_of_birth'] = dd.replace(year=dd.year-100)
                else:
                    mrz['date_of_birth'] = dd
                    print(dd)
            except ValueError:
                mrz['date_of_birth'] = 'Unknown'                
            
            # Converting expiration output
            try:
                dd = datetime.datetime.strptime(mrz['expiration_date'],'%y%m%d').date()
                if dd.year > now.year:
                    mrz['expiration_date'] = dd
                else:
                    mrz['expiration_date'] = dd
                    print(dd)
            except ValueError:
                mrz['expiration_date'] = 'Unknown'

            print(mrz['date_of_birth'])    

            return jsonify(mrz)


if __name__ == '__main__':
    app.run(debug=True)


