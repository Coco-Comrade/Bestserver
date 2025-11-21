import os
import glob
import shlex
import shutil
import logging
import subprocess
LOG_PATH = os.path.join(os.path.dirname(__file__), 'serverpys.log')
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
"""
Takes the clients input(command) and compares it to existing responses RAND, TIME, ETC.
then it returns the adjacent response.
:param command: The client's input as a string.
:return: The adjacent response as a string.
"""
def DR(path):
    try:
        os.chdir(path)
        current_dir = os.getcwd()
        return "Changed directory: " + os.getcwd()
    except Exception as e:
        logging.error(e)
        return "Error changing directory."
    except FileNotFoundError:
        logging.error("No such file or directory: " + str(path))
        return "No such file or directory"



def list(pattern):
    try:
        files = os.listdir(pattern)
        if not files:
            logging.error("No such file or directory")
        else:
            return "\n".join(files)
    except Exception as e:
        logging.error(e)
        return "No such file or directory"


def DEL(target):
    try:
        os.remove(target)
        print("Removed file: " + target)
    except FileNotFoundError:
        logging.error("No such file or directory")
        return "No such file or directory"
    except Exception as e:
        logging.error(e)
        return "Error removing file: " + target


def copy(target):
    try:
        parts = target.split(",",1)
        if len(parts) != 2:
            return "COPY requires two arguments"
        source = parts[0].strip().replace('"', "")
        destination = parts[1].strip().replace('"', "")
        shutil.copy(source, destination)
        return "Copied " + source + " to " + destination
    except FileNotFoundError as f:
        logging.error("No such file or directory")
    except Exception as e:
        logging.error(e)
        return "Error copying file: " + target


def EXEC(target):
    try:
        args = shlex.split(target)
        subprocess.run(args)
        return "Executed " + target
    except Exception as e:
        logging.error(e)
        return "Error executing command: " + target

