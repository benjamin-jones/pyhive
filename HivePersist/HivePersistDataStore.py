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
        jsonData = fd.read()

        return json.loads(jsonData)

    def get_fs_data(self):
        global g_store
        self.logger.info('Checking persistent datastore')
        rootdir = '../../data/'
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                key = subdir.strip("../../data/")
                self.logger.debug('Found file %s' % os.path.join(key, file))

                g_store[os.path.join(key, file)] = self.dict_from_file(os.path.join(subdir, file))


    def __init__(self, logger, storeq, servq):
        super(HPDataStore, self).__init__()
        self.logger = logger
        self.storeq = storeq
        self.servq = servq
        self.running = True
        logger.info('Starting DataStore...')

    def run(self):
        global g_store
        self.logger.info('Running...')
        self.get_fs_data()        
        myQ = self.storeq
        while self.running:
            request = ""
            try:
                action, request = myQ.get(block=True,timeout=1)
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
            
            self.servq.push(response)

    def busy_work(self):
        self.logger.info('Doing some work, store=%d' % len(g_store))
        self.logger.info(g_store)
        time.sleep(5)
                   
        
