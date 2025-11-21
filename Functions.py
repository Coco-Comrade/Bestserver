import os
import glob
import shutil
import logging
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
        return "Changed directory: " + current_dir
    except Exception as e:
        logging.error(e)
        return "Error changing directory: " + current_dir
    except FileNotFoundError:
        logging.error("No such file or directory")
        return "No such file or directory"
def list(pattern):
    try:
        files = glob.glob(pattern)
        if not files:
            logging.error("No such file or directory")
        else:
            return "\n".join(files)
    except Exception as e:
        logging.error(e)
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
        shutil.copy(target)
        return "Copied file: " + target
    except FileNotFoundError as f:
        logging.error("No such file or directory")
    except Exception as e:
        logging.error(e)
        return "Error copying file: " + target
