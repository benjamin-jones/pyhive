from mod_python import apache
from HiveModel import ModelRetrieve as mr
from HiveModel import ModelUpdate as mu

def uri_parser(uri):
    if uri.startswith("/api.py"):
        path = uri.split("/api.py")
        if len(path) == 2:
            return path[1]
    return None
        

class HiveRouter:
    def factory(req):
        method = req.method
        if method == "GET":
            return HiveGet(req)
        elif method == "POST":
            return HivePost(req)
    factory = staticmethod(factory)

class HiveGet(HiveRouter):
    def __init__(self, req):
        self.req = req

    def output(self):
        uri = self.req.uri
        path = uri_parser(uri)
        if not path:
            response = "Nothing to get..."
        else:
            model_response = mr.go(path)
            response = str(model_response)

        return apache.OK, response 

class HivePost(HiveRouter):
    def __init__(self, req):
        self.req = req

    def output(self):
        uri = self.req.uri
        path = uri_parser(uri)
        if not path:
            response = "Nothing to get..."
        else:
            model_response = mu.go(path, self.req.read())
            response = str(model_response)

        return apache.OK, response

