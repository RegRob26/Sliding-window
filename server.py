import json
import socket
import sys
import json
import time


class Server:
    def __init__(self, host, port, router_table):
        self.host = host
        self.port = port
        self.sock = None
        self.router_table = list(router_table)
        self.data_to_return = None
        self.messages = []
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (host, port)
        print('starting up on {} port {}'.format(*self.server_address))
        print(f'Router table {self.router_table}')
        self.sock.bind(self.server_address)

    def run(self):
        print("Listen for incoming connections")
        # Listen for incoming connections
        self.sock.listen(1)
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
            time.sleep(5)
            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(128)
                    print('received {!r}'.format(data))
                    if data:
                        print('waiting for more data')
                        self.messages.append(data)
                        connection.sendall('Ok'.encode('utf-8'))

                    else:
                        print('no data from', client_address)
                        break

                print(f'All data received {self.messages}')
                # sending data to the next server
                if self.messages:
                    data_to_send = json.loads(self.messages.pop())
                    print(f'Popped data {data_to_send}, receiver {data_to_send["receiver"]}')

                    if data_to_send['receiver'] == self.port:
                        print(f'Message received: {data_to_send}')
                        self.data_to_return = {
                            'message': 'Thanks for the message',
                            'sender': self.port,
                            'receiver': data_to_send['sender'],
                            'type': 1
                        }
                        # return message to the sender
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        if not self.router_table[0] == 0:
                            print(f'Returning data to {self.router_table[0]}')
                            s2.connect(('localhost', int(self.router_table[0])))
                            s2.sendall(json.dumps(self.data_to_return).encode('utf-8'))
                            s2.close()
                    else:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        if data_to_send['type'] == 1:
                            print(f'Returning 1 data to {self.router_table[0]}')
                            print(f'Returning this data {data_to_send}')
                            s2.connect(('localhost', int(self.router_table[0])))
                            s2.sendall(json.dumps(data_to_send).encode('utf-8'))
                            s2.close()

                        else:
                            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            print(f'Resending data to {self.router_table[1]}')
                            s2.connect(('localhost', int(self.router_table[1])))
                            s2.sendall(json.dumps(data_to_send).encode('utf-8'))
                            s2.close()

            finally:
                # Clean up the connection
                self.messages = []
                connection.close()
