import pymysql, os


def sql_connection():
    '''Function to store user input in a Google Cloud MySQL Database
    The conditionals check whether our app is running on app engine or localhost'''

    if os.environ.get('GAE_ENV') == 'standard':
        db_user = 'root'
        db_password = 'HathLagaKDikha'
        db_name = 'pehla'
        db_connection_name = 'duranzwebsite:asia-south1:duranzwebsitesdb'
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        conn = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
        c = conn.cursor()
    else:
        conn = pymysql.connect(user='root', password='password', db='pehla', host='localhost')
        c = conn.cursor()
    return conn, c
