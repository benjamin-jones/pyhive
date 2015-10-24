import logging
import threading
import Queue
import time
import os
import json

g_store = {}

class HPDataStore(threading.Thread):

    def dict_from_file(self,filename):
        fd = open(filename, "r")

        if not fd:
            return None

        jsonData = fd.read()
        fd.close()

        return json.loads(jsonData)

    def get_fs_data(self, filename):
        global g_store
        self.logger.info('Checking persistent datastore')
        
        result = self.dict_from_file(self.rootdir+ filename)

        g_store[filename] = (time.time(), result)

        return result

    def put_data(self, request):
        global g_store
        path, data = request

        if len(data) == 0:
            return "{ response : \"No data sent\"}"
    
        try:
            g_store[path] = (time.time(), json.loads(data))
        except:
            return "{ response: \"Bad JSON format\"}" 

        return "{ response: True }"

    def get_data(self, request):
        global g_store
        path = request

        if path in g_store.keys():
            time, value = g_store[path]
            g_store[path] = (time.time(), value)

        else:
            value = self.get_fs_data(path)

            if value == None:
                return "{ response: False }"

        return json.dumps(value)
        

    def __init__(self, logger, storeq, servq):
        super(HPDataStore, self).__init__()
        self.logger = logger
        self.storeq = storeq
        self.servq = servq
        self.running = True
        self.rootdir = '../../data/'
        logger.info('Starting DataStore...')

    def run(self):
        global g_store
        self.logger.info('Running...')
        myQ = self.storeq
        while self.running:
            request = ""
            try:
                action, request = myQ.get(block=True,timeout=1)
                self.logger.info("Processing message: " + str(request))
            except Queue.Empty:
                self.busy_work()
                continue

            if not request:
                continue

            if action == "get":
                response = self.get_data(request)
            if action == "post":
                response = self.put_data(request)

            if not response:
                response = "{ response: False }"
            
            self.servq.put(response)

    def data_to_fs(self, key, data):
        path = self.rootdir + key 

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedir(directory)

        fp = open(path, "w")
        fp.write(json.dumps(data))
        fp.close()

    def flush(self):
        global g_store
    
        remove_list = []

        for key in g_store:
            created, data = g_store[key]

            if time.time() - created > 10:
                self.data_to_fs(key, data)
                remove_list.append(key)

        g_store = {key: value for key, value in g_store.items() if key not in remove_list}
            

    def busy_work(self):
        global g_store

        self.logger.info('Doing some work, store=%d' % len(g_store))
        self.logger.info(g_store)
        self.flush()
        time.sleep(0.1)           
        
