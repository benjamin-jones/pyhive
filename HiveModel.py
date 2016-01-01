import json
import hashlib
from mod_python import apache
from pymongo import MongoClient

def get_secret():
    client = MongoClient()
    db = client.pyhive

    cursor = db.secrets.find()

    for document in cursor:
        if document["secret"] != None:
            return document["secret"]
    return None

def get_articles():
    client = MongoClient()
    db = client.pyhive

    cursor = db.articles.find().sort("date",-1)

    return cursor

def put_article(title, date, markdown):
    client = MongoClient()
    db = client.pyhive

    artObj = {}

    artObj["title"] = title
    artObj["date"] = date
    artObj["markdown"] = markdown

    result = db.articles.insert_one(artObj)


def get_data_store(path, req):
    if path == "ip":
        return req.get_remote_host(apache.REMOTE_NOLOOKUP)

    if path == "articles":
        articles = get_articles()
        response = []
        for document in articles:
            article = {}
            article["title"] = document["title"]
            article["date"] = document["date"]
            article["markdown"] = document["markdown"]
            response.append(article)
        jsonObj = {}
        jsonObj["articles"] = response

        response = json.dumps(jsonObj)

        return response

    return path
def put_data_store(path, pdata, req):
    jsonObj = json.loads(pdata)
    if path == "articles":
        secret = get_secret()
        
        if secret == None:
            return "{ \"result\" : false }"

        token = str(jsonObj["token"])
        time = str(jsonObj["time"])
        ip = str(req.get_remote_host(apache.REMOTE_NOLOOKUP))

        my_token = hashlib.sha256(secret + ip + time).hexdigest()

        if my_token == token:
            markdown = str(jsonObj["markdown"])
            date = str(jsonObj["date"])
            title = str(jsonObj["title"])

            put_article(title, date, markdown)

            return "{ \"result\" : true }"
        
        return "{ \"result\" : false }"

    return path

class ModelRetrieve:
    
    def go(path, req):
        response = get_data_store(path, req) 
        return response
    go = staticmethod(go)

class ModelUpdate:
    
    def go(path, data, req):
        response = put_data_store(path, data, req)
        return response
    go = staticmethod(go)

