from flask import Flask
from logging.handlers import RotatingFileHandler
import os, logging
import flask_monitoringdashboard as dashboard

#logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = Flask(__name__)

dashboard.bind(app)

app.config['SECRET_KEY'] = 'alasdf234dfg23'
app.config['UPLOAD_FOLDER'] = 'uploaded_files'


if not app.debug:

    if not os.path.exists('seed/logs'):
        os.mkdir('seed/logs')
    file_handler = RotatingFileHandler('seed/logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ineuronInternship_keys.json"


from seed import routes