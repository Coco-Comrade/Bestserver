import os
import glob
import shlex
import shutil
import logging
import pyautogui
import io
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
def DR(path)->str:
    """
    Writes all the files inside of the given directory
    :param path:
    :return:
    """""
    try:
        matches = glob.glob(path)
        if not matches:
            logging.error('No matches found')
            return "No file found"
        os.chdir(matches[0])
        current_dir = os.getcwd()
        return "Changed Directory to: " + current_dir +" Here are extra options: " + list(path)
    except Exception as e:
        logging.error(e)
        return "Error with changing directory"


def list(pattern)->str:
    """
    Kind of a useless function I kept around it lists all of the files in a given directory
    :param pattern:
    :return:
    """""
    try:
        files = os.listdir(pattern)
        if not files:
            logging.error("No such file or directory")
        else:
            return "\n".join(files)
    except Exception as e:
        logging.error(e)
        return "No such file or directory"


def DEL(target)->str:
    """
    Deletes the given file in the path.
    :param target:
    :return:
    """
    try:
        os.remove(target)
        return"Removed file: " + target
    except FileNotFoundError:
        logging.error("No such file or directory")
        return "No such file or directory"
    except Exception as e:
        logging.error(e)
        return "Error removing file: " + target

def Clean(p)->str:
    return p.strip('"').strip("'")
def copy(target):
    """
    Copies the given file to the given destination.
    :param target:
    :return:
    """
    try:
        parts = target.strip().split(",", 1)
        if len(parts) != 2:
            return "COPY requires two arguments"

        source = Clean(parts[0])
        destination = Clean(parts[1])

        source = os.path.normpath(source)
        destination = os.path.normpath(destination)

        shutil.copy(source, destination)
        return f"Copied {source} to {destination}"
    except FileNotFoundError:
        return f"Source file does not exist: {source}"
    except PermissionError:
        return "Permission denied"
    except Exception as e:
        return f"Copy failed: {e}"

def EXEC(target)->str:
    """
    Executes the application (needs the full path to the application)
    :param target:
    :return:
    """
    try:
        args = shlex.split(target)
        subprocess.run(args)
        return "Executed " + target
    except Exception as e:
        logging.error(e)
        return "Error executing command: " + target
def EXIT():
    return "Thank you for executing your command"

def Screeen_Shot()-> bytes:
    """
    Takes a screenshot of your current screen
    :return: 
    """
    try:
        screenshot = pyautogui.screenshot()
        buf = io.BytesIO()
        screenshot.save(buf, format = "PNG")
        img_bytes = buf.getvalue()
        return img_bytes
    except Exception as e:
        logging.error(e)
        return b"Error getting screenshot"