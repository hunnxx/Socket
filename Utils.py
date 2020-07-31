import argparse
import logging
import os

parser = argparse.ArgumentParser(description='For Socket Connection')
parser.add_argument('--host', metavar='HOST', type=str, default='localhost', help='a string for a host address')
parser.add_argument('--port', metavar='PORT', type=int, default=9999, help='a integer for a port number')
parser.add_argument('--buff', metavar='BUFF', type=int, default=1024, help='a buffer size for a socket connection')
parser.add_argument('--path_home', metavar='PATH_HOME', type=str, default=os.getenv('HOME'), help='Path of the home directory')

logger = logging.getLogger('Socket Logger')
logger.setLevel(logging.DEBUG)  # DEBUG>INFO>WARNING>ERROR>CRITICAL
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s]: %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def get_parser():
    return parser.parse_args()

def get_logger():
    return logger