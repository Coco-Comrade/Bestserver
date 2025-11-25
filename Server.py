import socket
import logging
import os
from operator import truediv

from Protocol import send, recv
import Functions
"""
Server Project-
Made: 2025
By: Omer Attia

This program opens a TCP server waits for a client and only allows up to 4 byte words to enter.
The server will have 4 outputs available:
1. Current time
2.  random number
3. The name of the device the server is hosted on
4. A command that allows the client to disconnect from the server
All logs will be put in 'serverpys.log'
"""
SERVER_NAME = socket.gethostname() #I made it so the server sent the host device name. I did this because it felt right and cooler hope you like it!!!! :)
IP = "0.0.0.0"
PORT = 8820
QUEUE_LEN = 1
MAX_PACKET = 1024
LOG_PATH = os.path.join(os.path.dirname(__file__), 'serverpys.log')
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
def Handle_command(command):
    command1 = command.split(" ",1)
    cmd = command1[0]
    cmd = cmd.upper()
    try:
        if cmd == "DIR":
            response = Functions.DR(command1[1])
        elif cmd == "LIST":
            response = Functions.list(command1[1])
        elif cmd == "DEL":
            response = Functions.DEL(command1[1])
        elif cmd == "COPY":
            response = Functions.copy(command1[1])
        elif cmd == "EXEC":
            Functions.EXEC(command1[1])
            response = "Executed " + command1[1]
    except Exception as error:
        logging.error(error)
        response = "Error"
    return response


def Handle_Exit(command)->bool:
    command1 = command.split(" ",1)
    cmd = command1[0]
    if cmd == "EXIT":
        return True
    else:
        return False



def main():
    logging.info('Server started')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(QUEUE_LEN)

    logging.info(f'Server listening on port: {PORT}')
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info('Client connected')
            buffer = b""
            try:
                while True:
                    try:
                        msg, buffer = recv(client_socket, buffer)
                    except Exception as e:
                        logging.error(e)
                        break
                    try:
                        if Handle_Exit(msg) == True:

                            response = "Disconnected Have a nice day!"
                            send(client_socket, response)
                            client_socket.close()
                            logging.info('Client has requested EXIT')
                        response = Handle_command(msg)
                    except Exception as e:
                        logging.error(f"Exception raised: {e}")
                        response = "ERROR"
                    try:
                        send(client_socket, response)
                    except Exception as e:
                        logging.error(f"Exception raised: {e}")
            finally:
                client_socket.close()
    finally:
        server_socket.close()
        logging.info('Server closed')
if __name__ == "__main__":
    main()