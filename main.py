from client import Client
from server import Server
import json
if __name__ == '__main__':

    client = Client('localhost', 10000, 'client1')
    data_to_send = {
        'message': 'Hello World',
        'sender': 10000,
        'receiver': 10003,
        'type': 0
    }
    data = json.dumps(data_to_send).encode('utf-8')
    client.send(data)

    # client = Client('localhost', 10001, 'client2')
