# TCP-Client-Server-Command-Protocol-with-Logging
## TCP Client-Server Communication System with Command Handling and Logging in Python

This project implements a client-server communication system where the client sends specific commands (such as "LIGHTON" or "LIGHTOFF") to the server. The server processes these commands and responds with status messages. The system uses a custom protocol, logging for tracking activities, and multi-threading to handle multiple client connections concurrently.

## Project Details:
- Client-Side: The client connects to the server, sends a command (e.g., "HELLO", "LIGHTON", "LIGHTOFF"), and waits for the server's response. It also logs the communication events for traceability.

- Server-Side: The server accepts incoming client connections, processes the messages based on the custom protocol, and sends appropriate responses back to the client. It logs all interactions, including received data, commands, and responses.

- Protocol: The communication protocol consists of a 12-byte header (including version, message type, and payload length), followed by the payload (message).

- Multi-threading: The server is designed to handle multiple client connections concurrently by using separate threads for each client.

- Logging: Both the client and server have logging set up to track sent and received messages, errors, and the status of operations.
