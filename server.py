import socket
import os
import configparser
import datetime
import threading

# Check if the configuration file exists
if not os.path.exists('server.conf'):
    print("Configuration file 'server.conf' not found. Sending 404 error.")
    exit()

# Load server configuration from server.conf
config = configparser.ConfigParser()
config.read('server.conf')

port = int(config.get('server configuration', 'port'))
work_dir = config.get('server configuration', 'work_dir')
max_request_size = int(config.get('server configuration', 'max_request_size'))


def handle_client(conn, addr):
    data = conn.recv(max_request_size)
    msg = data.decode()

    print(f"Request from {addr}:")
    print(msg)

    request_parts = msg.split()
    resource = request_parts[1].lstrip("/")
    if not resource:
        resource = "index.html"

    filename = os.path.join(work_dir, resource)

    if not os.path.exists(filename):
        content = b"File not found"
        response_status = "HTTP/1.1 404 Not Found\r\n"
        content_length = len(content)
    else:
        try:
            with open(filename, "rb") as file:
                content = file.read()
                response_status = "HTTP/1.1 200 OK\r\n"
                content_length = len(content)
        except FileNotFoundError:
            content = b"File not found"
            response_status = "HTTP/1.1 404 Not Found\r\n"
            content_length = len(content)

sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()

print(msg)

resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

Hello, webworld!"""

conn.send(resp.encode())

conn.close()