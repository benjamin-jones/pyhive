#!/usr/bin/env python

import sys
import logging
import Queue
from HivePersistServer import HPServer as hpServer
from HivePersistDataStore import HPDataStore as hpData

def print_banner(port, logfile):
    response =  "  # \n"
    response += " # #\n"
    response += "# ^ #    HivePersist - Port: " + str(port) + " |  Logfile: " + logfile +"\n"
    response += " # #\n"
    response += "  #\n"

    print(response)

def print_usage():
    print(".\HivePersist.py <port> <logfile>")

def parse_args(args):
    if len(args) != 3:
        print_usage()
        raise TypeError
    args = args[1:]

    port, logfile = int(args[0]), str(args[1])

    return port, logfile

def main():
    args = sys.argv

    try:
        port, logfile = parse_args(args)
    except TypeError:
        print("Error configuring HivePersist, exiting...")
        exit(0)

    print_banner(port, logfile)    

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=logfile,
                        filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

    # tell the handler to use this format
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # Now, we can log to the root logger, or any other logger. First the root...
    logging.info('Starting logger...')

    # Now, define a couple of other loggers which might represent areas in your
    # application:

    loggerData = logging.getLogger('DataStore')
    loggerServer = logging.getLogger('Server')

    storeMsgQ = Queue.Queue()
    servMsgQ = Queue.Queue()

    hpD = hpData(loggerData, storeMsgQ, servMsgQ)
    hpS = hpServer(loggerServer, port, storeMsgQ, servMsgQ)

    hpD.start()
    hpS.start()

    hpD.join()
    hpS.join()

    logging.info('HivePersist stopping...')
    
if __name__=="__main__":
    main()
