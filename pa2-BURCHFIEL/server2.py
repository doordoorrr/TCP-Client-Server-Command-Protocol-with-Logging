import argparse
import logging
import socket
import signal
import sys
from threading import Thread

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(client_socket, addr, logfile):
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(message)s')
    try:
        while True:
            # Receive header (12 bytes)
            header = recv_all(client_socket, 12)
            if not header:
                break

            version = int.from_bytes(header[0:4], 'big')
            msg_type = int.from_bytes(header[4:8], 'big')
            length = int.from_bytes(header[8:12], 'big')
            logging.info(f"Received Data: version: {version}, message_type: {msg_type}, length: {length}")

            if version != 17:
                logging.error("VERSION MISMATCH")
                continue

            # Receive message (if length > 0)
            message = ""
            if length > 0:
                message_data = recv_all(client_socket, min(length, 8))
                if message_data:
                    message = message_data.decode('utf-8')\
      # Handle HELLO (type 0)
            if msg_type == 0:
                logging.info("Received HELLO")
                response = "HELLO"
                resp_type = 0
            # Handle LIGHTON/LIGHTOFF
            elif msg_type in (1, 2):
                cmd = "LIGHTON" if msg_type == 1 else "LIGHTOFF"
                logging.info(f"EXECUTING SUPPORTED COMMAND: {cmd}")
                response = "SUCCESS"
                resp_type = 3  # Dedicated SUCCESS type
            else:
                logging.info(f"Ignoring unknown command: {msg_type}")
                response = "UNKNOWN COMMAND"
                resp_type = 3

            # Send response
            version = 17
            resp_length = len(response)
            header = (
                version.to_bytes(4, 'big') +
                resp_type.to_bytes(4, 'big') +
                resp_length.to_bytes(4, 'big')
            )
            client_socket.sendall(header + response.encode('utf-8'))
            logging.info(f"Sent response: {response}")

    finally:
        client_socket.close()

def server(port, logfile):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(f"Server started on port {port}")

    # Graceful shutdown handler
    def signal_handler(sig, frame):
        server_socket.close()
        sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    while True:
        client_socket, addr = server_socket.accept()
        logging.info(f"Received connection from {addr}")
        Thread(target=handle_client, args=(client_socket, addr, logfile)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Port")
    parser.add_argument("-l", type=str, required=True, help="Log file")
    args = parser.parse_args()
    server(args.p, args.l)
