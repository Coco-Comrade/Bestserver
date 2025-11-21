import socket
import logging
import os
from Protocol import recv, send
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
LOG_FILE = os.path.join(os.path.dirname(__file__), 'clients.log')
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

        while True:
            cmd = input("Enter command: (TIME, NAME, RAND, EXIT): ").strip().upper()
            if not cmd:
                print("Empty command, please try again.")
                logging.warning("Empty command.")
                continue

            client_socket.send(cmd.encode())


            response = client_socket.recv(MAX_PACKET).decode()
            print("Server:" + response)
            logging.info(response)

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
