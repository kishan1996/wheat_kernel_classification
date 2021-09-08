from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.utils import secure_filename
from seed.forms.forms import DataUpload
import random, os, json
# from io import TextIOWrapper
import pandas as pd
import logging 
from seed.database.cloud_sql import  sql_connection
from seed.eda.eda_funcs import (model_creation,feature_selection, dataframe_creation)
from seed import app
from seed.googlecloudmethods.gcloud_upload import upload_cloud


@app.route('/', methods=['GET','POST'])
def home():
    '''
    Two sections for single and multiple class classification
    Case1 - User provide array of values and prediction is made.
    Case2 - User Uploads file (Handled with flask-wtf) and EDA and Prediction is done 
    '''
    form = DataUpload()
    if form.validate_on_submit():
        uploaded_dataset = form.dataset.data

        # Writing Uploaded file to the server 
        '''f_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_dataset.filename)
        with open(f_path, 'wb') as file:
            file.write(uploaded_dataset.read())'''
        
        # Uploading files to the Google Cloud Storage
        f_path = uploaded_dataset.filename
        try:
            upload_cloud(uploaded_dataset)
            app.logger.info('File "{}" Uploaded to Cloud'.format(f_path))
            return redirect(url_for('summary', f_path=f_path))
        except Exception as e:
            flash('Make sure you are connected to the Internet and Try again', 'info')
            flash(str(e), 'info')
            app.logger.info('File "{}" Upload to Cloud Failed'.format(f_path))
            app.logger.info('Error Occured "{}" While uploading {} to Cloud'.format(str(e), f_path))
        
    elif request.method == 'POST':
        form_input = request.form
        # fetching values from the single sample form
        # name of the input field
        form_keys = ['area', 'perimeter', 'compactness', 'length', 'width', 'asymmetry', 'groove']
        try:
            array = [float(form_input.get(name)) for name in form_keys]
        except ValueError as e:
            flash(f"Please Enter Comma Separated Intergers ( Error => {str(e)} )" , 'danger')
            app.logger.info('Value Error {}'.format(str(e)))
        except Exception as e:
            flash("Something Went Wrong Please try again" + str(e), 'danger')
            app.logger.info('Exception occured {}'.format(str(e)))
        else:
            try:
                model = model_creation()
                y_pred = model.predict([array])
                #logging.info(str(y_pred))
                # conn, c = sql_connection()
                # c.execute("INSERT INTO singlesample (sample, prediction) VALUES ('{}', '{}')".format(array,y_pred))
                # conn.commit()
                # conn.close()
                # c.close()
                app.logger.info('Prediction are {} for values {}'.format(y_pred, array))
                return redirect(url_for('output', predictions=y_pred))
            except Exception as e:
                flash(f"Some Error Occured ( Error => {str(e)} )" , 'danger')
                app.logger.info('Exception occured {}'.format(str(e)))
            #flash("Your Predictions: Catergory - "+str(y_pred[0]), 'success')
    return render_template('index.html', form=form)

    
@app.route('/output')
def output():
    '''
    Prediction are returned on this page
    '''
    pred = request.args.getlist('predictions')
    return render_template('output.html', predictions=pred)
    
'''    
# Function to accept dataset url 
@app.route('/checker', methods=['GET','POST'])
def checker():
    if request.method == 'POST':
        url = request.form.get('url')
        df = pd.read_json(url)
        flash(df.shape,'info')
        columns = list(feature_selection(df))
        return render_template('checker.html', columns=columns)
    return render_template('checker.html')
'''

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    '''Information about DataFrame like: Missing values, Memory, No. of columns'''
    f_path = request.args.get('f_path')
    dataframe = dataframe_creation(f_path)
    profile = profiling(dataframe)
    features =  dataframe.columns
    if request.method == 'POST':
        target = request.form.get('target')
        model = model_creation()
        if target == 'None':
            try:
                predictions = model.predict(dataframe)
            except Exception as e:
                flash('Some Error Occured =>' + str(e), 'danger')
                app.logger.info('Exception occured {}'.format(str(e)))
            else:
                def storing_file_prediction_db(f_name, prediction):                    
                    conn, c = sql_connection()
                    c.execute("INSERT INTO bulk (fileName, predictions) VALUES ({}, {})".format(f_name, prediction))
                    conn.commit()
                    conn.close()
                    c.close()
                    # storing_file_prediction_db(f_name, prediction)
                app.logger.info('Prediction made for filename "{}" are {}'.format(f_path, list(predictions)))
                return redirect(url_for('output', predictions=list(predictions)))
        else:
            try:
                dataframe = dataframe.drop(columns=target)          
                predictions = model.predict(dataframe)
            except Exception as e:
                flash('Some Error Occured =>' + str(e), 'danger') 
                app.logger.info('Exception occured {}'.format(str(e))) 
            else:
                # storing_file_prediction_db(f_name, prediction)
                app.logger.info('Prediction made for filename "{}" are {}'.format(f_path, list(predictions)))
                return redirect(url_for('output', predictions=list(predictions)))
    return render_template('eda.html', features=list(features),profile=profile)


def profiling(df):
    ''' Input is dataframe. Returns Dictionary with Information about the DataFrame.'''


    foo = {}
    foo['no of rows'] = df.shape[0]
    foo['columns'] = df.shape[1]
    foo['missing'] = df.isnull().sum()
    foo['total_missing'] = [df.isnull().sum().sum() if df.isnull().sum().sum() else 'No missing Values']
    foo['numerical_columns'] = [col for col in df.columns if df[col].dtype != 'O']
    foo['categorical_columns'] = [col for col in df.columns if df[col].dtype == 'O']
    foo['duplicated_rows'] = df.duplicated().sum()
    foo['memory_usage'] = str(df.memory_usage(deep=True).sum() / 1000)+" Kb"
    return foo


# Documentation moved to Google Slides File attached to the application.

# @app.route('/documentation')
# def documentation():
#     '''Tech Specification / Architecture Document'''

#     return render_template('documentation.html')


@app.route('/about')
def about():
    '''Information about the creators of this application.Their challenges and learnings.'''
    return render_template('about.html')