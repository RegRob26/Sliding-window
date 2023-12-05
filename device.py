"""
This file is used to run and configure the server from the command line-args
"""
from server import Server
import sys
import argparse

parser = argparse.ArgumentParser()


parser.add_argument('--host', type=str)
parser.add_argument('--port', type=str)
parser.add_argument('--type', type=int)
parser.add_argument('--time', type=int, default=4.1)
parser.add_argument('--table', nargs='*', type=int)

args = parser.parse_args()
print(f'Host: {args.host}, Port: {args.port}, Table: {args.table}')
server = Server(args.host, int(args.port), args.table, int(args.type), args.time)
server.run()

