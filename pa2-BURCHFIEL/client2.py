import argparse
import logging
import socket

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def send_packet(sock, version, msg_type, message):
    msg_length = len(message)
    header = (
        version.to_bytes(4, 'big') +
        msg_type.to_bytes(4, 'big') +
        msg_length.to_bytes(4, 'big')
    )
    sock.sendall(header + message.encode('utf-8'))

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, required=True, help="Server IP")
    parser.add_argument("-p", type=int, required=True, help="Port")
    parser.add_argument("-l", type=str, required=True, help="Log file")
    parser.add_argument("-c", type=str, required=True, choices=["LIGHTON", "LIGHTOFF"], help="Command")
    args = parser.parse_args()

    logging.basicConfig(filename=args.l, level=logging.INFO, format='%(asctime)s - %(message)s')

    # Connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.s, args.p))
    logging.info(f"Connected to {args.s}:{args.p}")

    try:
        # Send HELLO (type 0)
        send_packet(sock, 17, 0, "HELLO")
        logging.info("Sent HELLO packet")
        
    
        # Wait for HELLO response
        header = recv_all(sock, 12)
        version = int.from_bytes(header[0:4], 'big')
        msg_type = int.from_bytes(header[4:8], 'big')
        length = int.from_bytes(header[8:12], 'big')
        message = recv_all(sock, length).decode('utf-8') if length > 0 else ""
        logging.info(f"Server response: {message}")

        # Send command (type 1 or 2)
        cmd_type = 1 if args.c == "LIGHTON" else 2
        send_packet(sock, 17, cmd_type, args.c)
        logging.info(f"Sent command: {args.c}")

        # Wait for SUCCESS response
        header = recv_all(sock, 12)
        version = int.from_bytes(header[0:4], 'big')
        msg_type = int.from_bytes(header[4:8], 'big')
        length = int.from_bytes(header[8:12], 'big')
        message = recv_all(sock, length).decode('utf-8') if length > 0 else ""
        logging.info(f"Command status: {message}")

    finally:
        sock.close()
        logging.info("Connection closed")

if __name__ == "__main__":
    client()
