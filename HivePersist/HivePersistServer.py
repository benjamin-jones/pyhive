import logging
import threading
import BaseHTTPServer
import Queue
g_storeq = []
g_servq = []

class HPServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(s):
        """ Response to a POST request - We expect the body to be JSON"""
        global g_storeq
        content_len = int(s.headers.getheader('content-length', 0))
        post_body = s.rfile.read(content_len)
        g_storeq.put(('post', (s.path, post_body)))

        response = g_servq.get()
 
        s.send_response(200)
        s.end_headers() 
        s.wfile.write(response)

    def do_GET(s):
        global g_storeq
        
        g_storeq.put(('get', s.path))

        response = g_servq.get()
 
        s.send_response(200)
        s.end_headers()
        s.wfile.write(response)


class HPServer(threading.Thread):
    def __init__(self, logger, port, storeq, servq):
        global g_storeq
        global g_servq

        super(HPServer, self).__init__()
        self.logger = logger
        self.port = port
        g_storeq = storeq
        g_servq = servq

        self.stopped = False
        logger.info('Starting Server...')

    def run(self):
        self.logger.info('Running...')

        httpObj = BaseHTTPServer.HTTPServer
        httpd = httpObj(('127.0.0.1', self.port), HPServerHandler)

        self.logger.info("Service listening on %s:%d" % ('127.0.0.1',self.port))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            self.logger.warn("Server is going down because Ctrl+C")
            pass
