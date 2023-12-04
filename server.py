import random
import socket
import json
import time


class Server:
    def __init__(self, host, port, router_table, server_type=0):
        self.window_buffer = None
        self.window_size = None
        self.list_messages = None

        self.host = host
        self.port = port
        self.sock = None
        self.router_table = list(router_table)
        self.data_to_return = None
        self.messages = []
        self.server_type = server_type

        if server_type == 1:
            print("This is a sender server")
            self.configure_sender()

        self.transmission_flag = False

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (host, port)
        print('starting up on {} port {}'.format(*self.server_address))
        print(f'Router table {self.router_table}')
        self.sock.bind(self.server_address)

    def select_delay(self):
        # Select delay between 0 and 5 seconds with seconds precision
        time.sleep(random.randint(0, 2))

    def send(self, socket_t, data, dest):
        if data['type'] == 1:
            # print blue color
            print(f'\033[94m        Sending to {self.router_table[dest]}\033[0m')
        else:
            # print yellow color
            print(f'\033[93m        Sending to {self.router_table[dest]}\033[0m')

        socket_t.connect(('localhost', int(self.router_table[dest])))
        socket_t.sendall(json.dumps(data).encode('utf-8'))
        socket_t.close()

    def configure_sender(self):
        self.list_messages = [
            {
                'message': f'Hello {i}',
                'number': i,
                'sender': 10000,
                'receiver': 10003,
                'type': 0
            }
            for i in range(48)
        ]
        self.window_size = 1
        self.window_buffer = []

    def run(self):
        # print("Listen for incoming connections")
        # Listen for incoming connections
        self.sock.listen(10)
        # self.sock.setblocking(False)
        while True:
            # Wait for a connection
            # print('waiting for a connection')
            connection, client_address = self.sock.accept()
            self.select_delay()
            try:
                # print in green color
                # print(f'\033[92mConnection from {client_address}\033[0m')
                # print('connection from', client_address)
                while True:
                    # Receive the data in small chunks and retransmit it

                    # Testing that when the servers are the first sender of the message

                    data = connection.recv(128)
                    # print in ger color

                    print(f'\033[92mReceived {data} from {client_address}\033[0m')

                    # print('received {!r}'.format(data))
                    if data:
                        # print('waiting for more data')
                        self.messages.append(data)
                        connection.sendall('Ok'.encode('utf-8'))
                    else:
                        # print('no data from', client_address)
                        break

                # sending data to the next server
                if self.messages:
                    data_to_send = json.loads(self.messages.pop())
                    # print(f'Message received: {data_to_send}')

                    # If the message is for this server
                    if data_to_send["number"] == -1 or self.transmission_flag:
                        if data_to_send["number"] != -1:
                            self.list_messages.pop(0)
                            self.window_buffer.remove(int(data_to_send["number"] - 1))
                            # print in white color
                            print(f'\033[97m Window buffer {self.window_buffer}\033[0m')
                            if not self.window_size + 1 > 11:
                                self.window_size += 1

                        # the server work as a sender\
                        self.transmission_flag = True
                        if self.window_size > len(self.list_messages):
                            self.window_size = len(self.list_messages)
                            print("len list messages", len(self.list_messages))

                        if len(self.list_messages) > 0:
                            for i in range(0, self.window_size):
                                if len(self.list_messages) > 0 and self.list_messages[i]["number"] not in self.window_buffer:
                                    self.window_buffer.append(self.list_messages[i]["number"])
                                    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    # print(f'Sending package {self.list_messages[i]["number"]} to {
                                    # self.router_table[1]}')
                                    self.send(s2, self.list_messages[i], 1)
                        else:
                            # print in red all message was sent
                            print(f'\033[91m        All message was sent \033[0m')
                    else:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                        if data_to_send['receiver'] == self.port:
                            self.data_to_return = {
                                'message': f'message received {data_to_send["number"]}',
                                'sender': self.port,
                                'number': data_to_send['number'] + 1,
                                'receiver': data_to_send['sender'],
                                'type': 1
                            }
                            # return message to the sender
                            if not self.router_table[0] == 0:
                                print("This is the last server")
                                self.send(s2, self.data_to_return, 0)
                        else:
                            # if the message is an answer
                            if data_to_send['type'] == 1:
                                self.send(s2, data_to_send, 0)
                            # if the message is a request or a message
                            else:
                                self.send(s2, data_to_send, 1)
            finally:
                # Clean up the connection
                self.messages = []
                connection.close()
