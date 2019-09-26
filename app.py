from flask import Flask, url_for, send_from_directory, request,render_template,redirect
import logging, os
from werkzeug import secure_filename
import numpy as np
import pandas as pd
import pandas_profiling
from flask_wtf import FlaskForm
from wtforms.validators import (InputRequired, Length, DataRequired)
from wtforms import (StringField, PasswordField, SelectField)
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__,template_folder='templates')
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/fileupload')
def fileupload():
    return render_template('fileupload.html')


class CreateForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=35)]) # NOQA
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=80)]) # NOQA
    algo = SelectField('Algo Available', validators=[DataRequired()], choices=[("", ""), ("Linearregression", "linear regression"), ("Randomforest", "Random Forest")]) # NOQA
    data = SelectField('Algo Available', validators=[DataRequired()], choices=[("", ""), ("dataset", "Hackathon  AQI")]) # NOQA

@app.route('/upload', methods = ['POST'])
def api_root():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['file']:
    	app.logger.info(app.config['UPLOAD_FOLDER'])
    	csv = request.files['file']
    	csv_name = secure_filename(csv.filename)
    	create_new_folder(app.config['UPLOAD_FOLDER'])
    	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_name)
    	app.logger.info("saving {}".format(saved_path))
    	csv.save(saved_path)
    	return "Success"
    else:
    	return "Where is the image?"

def dataframe():
    files = []
    for i in os.listdir("./uploads"):
        if i.endswith('.csv'):
            files.append(i)
    app.logger.info("files {}".format(files))
    df = pd.read_csv("./uploads/"+files[0])
    return df

@app.route('/preview', methods=("POST", "GET"))
def html_table():

	df = dataframe()
	head = df.head(10)
	return render_template('preview.html',  tables=[head.to_html(classes='head')], titles=df.columns.values)

@app.route('/profile', methods=("POST", "GET"))
def profile():
    df = dataframe()
    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(output_file="output.html")
    return render_template("output.html")

@app.route('/experiments')
def experiments():
    return render_template('experiments.html')

@app.route('/createexp')
def createexperiments():
    return render_template('createExperiments.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    error = ''
    form = CreateForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, level=form.level.data) # NOQA
        
        return redirect(url_for('train'))
    else:
        if request.method == 'POST':
            error = 'Empty or not valid input'
        return render_template('createExperiments.html', form=form, error=error)
    return render_template('createExperiments.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)