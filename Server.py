import socket
import logging
import os
import glob
import shutil
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



def handle_command(command: str) -> str:
    """
       Takes the clients input(command) and compares it to existing responses RAND, TIME, ETC.
       then it returns the adjacent response.
       :param command: The client's input as a string.
       :return: The adjacent response as a string.
       """
    assert isinstance(command, str),"Command must be a string"
    if command.startswith("CD "):
        path = command[3: ].strip()
        try:
            os.chdir(path)
            current_dir = os.getcwd()
            return "Changed directory: " + current_dir
        except Exception as e:
            logging.error(e)
            return "Error changing directory: " + current_dir
        except FileNotFoundError:
            logging.error("No such file or directory")
            return "No such file or directory"
    elif command.startswith("LS "):
            pattern = command[2:].strip()
            try:
                files = glob.glob(pattern)
                if not files:
                    logging.error("No such file or directory")
                else:
                    return "\n".join(files)
            except Exception as e:
                logging.error(e)
    elif command.upper().startswith("DEL "):
        target = command[4:].strip()
        try:
            os.remove(target)
            return "Removed file: " + target
        except FileNotFoundError:
            logging.error("No such file or directory")
            return "No such file or directory"
        except Exception as e:
            logging.error(e)
            return "Error removing file: " + target
    elif command.upper().startswith("COPY "):
        target = command[5:].strip()
        try:
            shutil.copy(target)
            return "Copied file: " + target
        except FileNotFoundError as f:
            logging.error("No such file or directory")
        except Exception as e:
            logging.error(e)
            return "Error copying file: " + target





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

            try:
                while True:
                    try:
                        data = client_socket.recv(MAX_PACKET).decode().strip()
                    except socket.error as err:
                        logging.error(f"Socket error: {err}")
                        break
                    if not data:
                        logging.info('Client disconnected')
                    logging.info(f"Data received: {data}")
                    try:
                        response = handle_command(data)
                        client_socket.send(response.encode())
                    except AssertionError as e:
                        logging.error(f"Exception raised: {e}")

                    if data == 'EXIT':
                        logging.info('Client disconnected')
                        client_socket.close()
            finally:
                client_socket.close()
    finally:
        server_socket.close()
        logging.info('Server closed')
if __name__ == "__main__":
    main()