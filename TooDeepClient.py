#-*-coding:utf-8-*-
import sys
from baseClass.Client import Client
from TooDeepParser import TooDeepParser 

# server HOST and PORT#
HOST = '104.199.218.103'
# localhost for testing
#HOST = '127.0.0.1'
PORT = 9001

client = Client()
if client.connect_server(HOST, PORT) == False:
    print '서버 연결오류'
    sys.exit()

#Your AI
myAI = TooDeepParser()

client.set_parser(myAI)

#Client Loop
client.client_run()
