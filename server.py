"""
http://localhost:80
"""

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

    now = datetime.datetime.now()
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type = "text/html"
    server_name = "SelfMadeServer v0.0.1"

    response_headers = {
        "Date": date,
        "Content-Type": content_type,
        "Server": server_name,
        "Content-Length": content_length,
        "Connection": "close"
    }

    headers_str = ""
    for header_name, header_value in response_headers.items():
        headers_str += f"{header_name}: {header_value}\r\n"

    response = response_status + headers_str + "\r\n" + content.decode("utf-8")

    conn.send(response.encode())

    conn.close()


# Create a socket and bind to the specified port
sock = socket.socket()
try:
    sock.bind(('', port))
    print(f"Using port {port}")
except OSError:
    print(f"Port {port} is already in use")
    exit()

sock.listen(5)

while True:
    conn, addr = sock.accept()
    print("Connected", addr)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
