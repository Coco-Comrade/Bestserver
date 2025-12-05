import socket
import logging
import os
from Protocol import recv, send, Recv_Bin
"""
Server Project-
Made: 2025
By: Omer Attia

This is the client side program it has its own log and will ensure no unkown
 commands are inputted into the server. Also ensures the client disconnects properly\
 log file: clients.log
"""
MAX_PACKET = 1024
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8820
LOG_FILE = os.path.join(os.path.dirname(__file__), 'clienwaitr ts.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Client started")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        logging.info("Client connected to server" + SERVER_IP + ":" + str(SERVER_PORT))
        buffer = b""
        while True:
            cmd = input("Enter command: (LIST,DIR,DEL,COPY): ").strip().upper()
            if not cmd:
                print("Empty command, please try again.")
                logging.warning("Empty command.")
                continue

            send(client_socket, cmd)


            response, buffer = recv(client_socket, buffer)
            if response is None and buffer and buffer.startswith(b'BINARY:'):
                header_end = buffer.find(b'#')
                header = buffer[:header_end].decode()
                size = int(header.split(":")[1])
                buffer = buffer[header_end+1:]
                data = buffer[:size]
                buffer = buffer[size:]
                while len(data) < size:
                    chunk = client_socket.recv(size - len(data))
                    if not chunk:
                        logging.warning("Binary recv failed.")
                        break
                    data += chunk
                with open("Screenshot.png", "wb") as f:
                    f.write(data)
                print("screenshot saved to screenshot.png")
                continue
            if response is None:
                print("Server disconnected.")
                break
            print("Server response: " + response)

            if cmd == "EXIT":
                logging.info("Server exited.")
                break
    except AssertionError as e:
        logging.error(e)
    except socket.error as err:
        logging.error(err)
    finally:
        client_socket.close()
if __name__ == "__main__":
    main()
