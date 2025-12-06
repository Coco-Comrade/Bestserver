import socket
import logging
import os
from operator import truediv

from Protocol import send, recv, Send_Bin
import Functions
"""
Server Project 2.7-
Made: 2025
By: Omer Attia

This program opens a TCP server waits for a client and only allows up to 4 byte words to enter.
The server will have 4 outputs available:
1. DIR: Changes directory.
2. EXEC: Executes the given program.
3. SCREENSHOT: Takes a screenshot of your current screen!
4. COPY: Copies a file onto onto another source:destination
5. DEL: Deletes the given file path.

All logs will be put in 'serverpys.log'
"""
SERVER_NAME = socket.gethostname() #I made it so the server sent the host device name. I did this because it felt right and cooler hope you like it!!!! :)
IP = "0.0.0.0"
PORT = 8820
QUEUE_LEN = 1
LOG_PATH = os.path.join(os.path.dirname(__file__), 'serverpys.log')
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
def Handle_command(command,client):
    """
    This function handles the command sent by the client and sends it to the server after proccessing it with
    Functions.py there it handles the commands with the nessacery functions.
    :param command:
    :param client:
    :return: server response
    """
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
        elif cmd == "SCREENSHOT":
            img_bytes = Functions.Screeen_Shot()
            if bytes is None:
                logging.error("screenshot failed")
                return "Screenshot failed"
            Send_Bin(client,img_bytes)
            logging.info("Screenshot succeeded")
            return None
    except Exception as error:
        logging.error(error)
        response = "Error"
    return response


def Handle_Exit(command)->bool:
    """
    This functions ensures that the client wants to exit the server and responses with True or False
    accordingly.
    :param command:
    :return:
    """
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
                        response = Handle_command(msg,client_socket)
                    except Exception as e:
                        logging.error(f"Exception raised: {e}")
                        response = "ERROR"
                    try:
                        if response is not None:
                            send(client_socket, response)
                        else:
                            send(client_socket, b"")
                    except Exception as e:
                        logging.error(f"Exception raised: {e}")
            finally:
                client_socket.close()
    finally:
        server_socket.close()
        logging.info('Server closed')
if __name__ == "__main__":
    main()
    assert isinstance(IP, str) and IP != "", "IP must be a string"
    assert isinstance(PORT, int) and PORT > 0, "PORT must be a positive integer"
    assert isinstance(QUEUE_LEN, int), "QUEUE_LEN must be a positive integer"
    assert isinstance(LOG_PATH, str) and LOG_PATH.endswith(".log"), "LOG_PATH must be a string and must end with .log"

    assert callable(Handle_command), "Handle_command must be a callable"
    assert callable(Handle_Exit), "Handle_Exit must be a callable"
    assert callable(Functions.list), "Functions.list must be a callable"
    assert callable(Functions.DEL), "Functions.DEL must be a callable"
    assert callable(Functions.copy), "Functions.copy must be a callable"
    assert callable(Functions.EXEC), "Functions.EXEC must be a callable"
    assert callable(Functions.Screeen_Shot), "Functions.Screeen_Shot must be a callable"
    assert callable(send), "send must be a callable"
    assert callable(recv), "recv must be a callable"
    assert callable(Send_Bin), "Send_Bin must be a callable"

    needed_functions = ["DR", "list", "DEL", "copy", "EXEC", "Screen_Shot"]
    for fn in needed_functions:
        assert hasattr(Functions, fn) and callable(getattr(Functions,fn)),f"{fn}" "missing in Functions module"

    assert hasattr(logging, "info"), "Log must be an instance of logging.ERROR"
