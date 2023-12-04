from client import Client
from server import Server
import json
if __name__ == '__main__':

    window_size = 8
    window_buffer = []

    messages = {
        'message': 'First message',
        'number': -1,
        'sender': 10000,
        'receiver': 10003,
        'type': 0
    }

    # Create a TCP/IP socket
    # parser = argparse.ArgumentParser()
    client = Client('localhost', 10000, 'client1')

    data = json.dumps(messages).encode('utf-8')
    client.send(data)

    # client = Client('localhost', 10001, 'client2')
