from client import Client
from server import Server
import json

"""
    Execute this file after running all the servers
    This script will send a message to the first server to start the communication
"""
if __name__ == '__main__':

    messages = {
        'message': 'First message',
        'number': -1,
        'sender': 10000,
        'receiver': 10003,
        'type': 0
    }

    # Create a TCP/IP socket
    # The second argument is the port of the server
    client = Client('localhost', 10000, 'client1')
    data = json.dumps(messages).encode('utf-8')
    client.send(data)
