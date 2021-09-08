from seed import app
from wsgiref import simple_server
import os
if __name__ == "__main__":
    #clApp = ClientApp()
    port = int(os.getenv("PORT"))
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host,port=port, app=app)
    httpd.serve_forever()
    
    
    
  
