import urllib2
import requests
from mod_python import apache

def get_data_store(path):
    return urllib2.urlopen("http://localhost:1337/" + path).read()  
def put_data_store(path, pdata):
    data = requests.post("http://localhost:1337/" + path, data=pdata)

    return data.text

class ModelRetrieve:
    
    def go(path):
        response = get_data_store(path) 
        return response
    go = staticmethod(go)

class ModelUpdate:
    
    def go(path, data):
        response = put_data_store(path, data)
        return response
    go = staticmethod(go)

