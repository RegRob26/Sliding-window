import socket
import sys
import json


class Client:
    def __init__(self, server_host, server_port, client_name):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # Connect the socket to the port where the server is listening
        self.server_address = (server_host, server_port)
        print('connecting to {} port {}'.format(*self.server_address))
        self.sock.connect(self.server_address)
        self.client_name = client_name

    def send(self, data):
        try:
            # Send data
            print('sending {!r}'.format(data))

            self.sock.sendall(data)

            # Look for the response
            amount_received = 0
            amount_expected = len(data)
            data_block = b''
            while data_block != b'Ok':
                data_block = self.sock.recv(128)
                amount_received += len(data_block)
                print('received {!r}'.format(data_block))


        finally:
            print('closing socket')
            self.sock.close()
