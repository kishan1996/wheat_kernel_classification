from flask import request
import pickle, os
import pandas as pd


def dataframe_creation(f_name):
    '''This function takes uploaded file name and creates a pandas DataFrame.
    Storing the bucket name in bucket variable.
    Check extension of the uploaded file and reading with suitable Pandas function'''

    bucket = "gs://ineuroninternship.appspot.com/"
    extensions = zip(['xlsx','sql','html','txt','csv','json'],
                     [pd.read_excel, pd.read_sql, pd.read_html, pd.read_csv, pd.read_csv, pd.read_json])
    for ext, func in extensions:
        if f_name.endswith(ext): 
            df = func(bucket+f_name)
            break
    return df 
   

def model_creation():
    '''User have two options to select from for making Predictions. 
    Extracting values from HTML form and predicting from selected model'''
    # model_path = os.path.dirname(os.path.abspath(__file__))+'/trained_models/'
    model_path = 'seed/trained_models/'
    if request.form.get('file_model') == 'DT': model = pickle.load(open(model_path+'dt_model.pkl', 'rb'))
    else: model = pickle.load(open(model_path+'xgb_model.pkl', 'rb'))
    return model
    

# def pca(data):
#     from sklearn.decomposition import PCA
#     from sklearn.preprocessing import StandardScaler 
#     scalar = StandardScaler()
#     x_transform = scalar.fit_transform(data)




    
def feature_selection(df):
    columns = df.columns 
    return columns 
    
    
# def eda(df):
#     df.plot().savefig('static/images/image.png') 


