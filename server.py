import random
import socket
import json
import time


class Server:
    """
        This class is a server that can work as a sender or a receiver or repeater

    """

    def __init__(self, host, port, router_table, server_type=0, expected_time=4):
        """
        This method initialize the server with the following parameters
        :param host: The host of the server (localhost)
        :param port: The port of the server (10000)
        :param router_table: The router table of the server (10001, 10002)
        :param server_type: The type of the server (1, 2)
        :param expected_time: The expected time to receive the message, only for the sender server
        """
        self.last_item_window = None
        self.window_size = None
        self.list_messages = None
        self.counted_window = 0
        self.expected_window = 0
        self.expected_time = expected_time
        self.max_window_size = 16

        self.host = host
        self.port = port
        self.sock = None
        self.router_table = list(router_table)
        self.data_to_return = None
        self.messages = []
        self.server_type = server_type

        if server_type == 1:
            print("This is a sender server")
            print(f"Answer time: {self.expected_time}")
            self.configure_sender()
        if server_type == 2:
            print("This is a receiver server")

        self.transmission_flag = False
        self.initial_time = 0
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (host, port)
        print('starting up on {} port {}'.format(*self.server_address))
        print(f'Router table {self.router_table}')
        self.sock.bind(self.server_address)

    def select_delay(self):
        """
        This method select a random delay between 0 and 2 seconds
        :return:
        """
        # Select delay between 0 and 2 seconds with seconds precision
        time.sleep(random.randint(0, 2))

    def send(self, socket_t, data, dest):
        """
        This method send a message to the next server on the router table or to the first server on the router table
        :param socket_t: The socket to send the message
        :param data: The data to send
        :param dest: The destination of the message (number in the router table)
        :return: None
        """

        if data['type'] == 1:
            # print blue color
            print(f'\033[94m        Answer {data["number"]} to {self.router_table[dest]}\033[0m')
        else:
            # print yellow color
            print(f'\033[93m        Sending {data["number"]} to {self.router_table[dest]}\033[0m')

        socket_t.connect(('localhost', int(self.router_table[dest])))
        socket_t.sendall(json.dumps(data).encode('utf-8'))
        socket_t.close()

    def configure_sender(self):
        """
        This method configure the sender server creating a list of messages and the window size
        :return: None
        """
        self.list_messages = [
            {
                'message': f'Hello {i}',
                'number': i,
                'sender': 10000,
                'receiver': 10003,
                'window_size': -1,
                'type': 0
            }
            for i in range(48)
        ]
        self.window_size = 1

    def run(self):
        """
        This method run the server and handle the incoming connections and server type
        :return: None
        """
        print("Listen for incoming connections")
        # Listen for incoming connections
        self.sock.listen(10)
        while True:
            connection, client_address = self.sock.accept()
            self.select_delay()
            try:
                while True:
                    # Receive the data in small chunks
                    data = connection.recv(128)

                    # If the data is not empty then print the data and append the data to the messages list
                    if data:
                        print(f'\033[92mReceived {data} from {client_address}\033[0m')
                        self.messages.append(data)
                        connection.sendall('Ok'.encode('utf-8'))
                    else:
                        break

                # sending data to the next server
                if self.messages:
                    data_to_send = json.loads(self.messages.pop())
                    # If the message is for this server
                    if data_to_send["number"] - 1 == self.last_item_window:
                        print(f'\033[91m        The last package ({data_to_send["number"] - 1}) was received\033[0m')
                        # Finish the answer time
                        time_result = time.time() - self.initial_time
                        print(f'The time was {time_result} seconds')
                        self.transmission_flag = True

                        # Increase or decrease the window size depending on the time result
                        if time_result > self.expected_time:
                            if self.window_size // 2 > 0:
                                self.window_size = self.window_size // 2
                        else:
                            if self.window_size * 2 < self.max_window_size:
                                self.window_size = self.window_size * 2

                    else:
                        self.transmission_flag = False

                    # If the message is for this server and the server is a sender
                    if data_to_send["number"] == -1 or self.transmission_flag:
                        if data_to_send["number"] != -1:
                            last_window = self.list_messages[0]["window_size"]
                            # Delete the messages that was sent in the last window
                            for i in range(last_window):
                                self.list_messages.pop(0)
                        print(f"The window size is {self.window_size}")

                        # If the window size is bigger than the list of messages then the window size is the length of the list
                        if self.window_size > len(self.list_messages):
                            self.window_size = len(self.list_messages)
                            print("len list messages", len(self.list_messages))

                        # If the list of messages is not empty then send the messages in the window size
                        if len(self.list_messages) > 0:
                            self.list_messages[0]['window_size'] = self.window_size
                            self.last_item_window = self.list_messages[0]["number"]
                            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            self.send(s2, self.list_messages[0], 1)

                            for i in range(1, self.window_size):
                                if len(self.list_messages) > 0:
                                    self.last_item_window = self.list_messages[i]["number"]
                                    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    self.send(s2, self.list_messages[i], 1)
                            # print in pink color
                            print(f'\033[95m The last package ({self.last_item_window}) was sent\033[0m')
                            self.initial_time = time.time()
                        # If all the messages was sent then print a message
                        else:
                            print(f'\033[91m        All message was sent \033[0m')
                    # If the message is not for this server then send the message to the next server or to the first server
                    else:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        if data_to_send['window_size'] != -1 and data_to_send['receiver'] == self.port and data_to_send[
                            'type'] == 0:
                            self.expected_window = data_to_send['window_size']
                            self.counted_window += 1
                            print(f"Expected window: {self.expected_window} and Count {self.counted_window}")
                        # if the message is for this server and the server is a receiver
                        if data_to_send['receiver'] == self.port:
                            if self.expected_window == self.counted_window:
                                self.data_to_return = {
                                    'message': f'message received {data_to_send["number"]}',
                                    'sender': self.port,
                                    'number': data_to_send['number'] + 1,
                                    'receiver': data_to_send['sender'],
                                    'type': 1,
                                    'window_size': self.expected_window
                                }
                                self.expected_window = 0
                                self.counted_window = 0
                                # return message to the sender
                                if not self.router_table[0] == 0:
                                    print("This is the last server")
                                    self.send(s2, self.data_to_return, 0)
                            else:
                                self.counted_window += 1
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
