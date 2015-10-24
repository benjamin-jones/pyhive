import shelve
import os
from mod_python import apache

def try_data_store(path):
    true_path = os.path.dirname(os.path.realpath(__file__)) + "/../data" + path
    return os.path.isdir(true_path)
        

class ModelRetrieve:
    
    def go(path):
        response = "ModelRetrieve: Getting " + path + "..."
        
        if try_data_store(path):
            response += "\n\tFound data store"
        else:
            response += "\n\tData store not found"
            response += ": " + path 
        return response
    go = staticmethod(go)

class ModelUpdate:
    
    def go(path):
        response = "ModelUpdate: Setting " + path + "..."
        if try_data_store(path):
            response += "\n\tFound data store"
        else:
            response += "\n\tData store not found"
            response += ": " + path 
        return response
    go = staticmethod(go)

