"""
This module provides API endpoints for managing counter states.
"""
import os

from flask import Flask, abort

app = Flask(__name__)

@app.route('/counter_state/<int:pid>', methods=['GET'])
def counter_state(pid):
    """
    API endpoint for reading the information of a process.
    """
    FILE_PATH = os.environ.get('FILE_PATH', '/proc/%i/io')
    try:
        file_name = FILE_PATH % pid
        state = read_counter_state(file_name)
    except KeyError as e:
        abort(422, description=f"Key {e} not found in file content")
    except ValueError:
        abort(422, description=f"Invalid content in /proc/{pid}/io")
    except FileNotFoundError:
        abort(404, description=f"/proc/{pid}/io not found")
    except PermissionError:
        abort(403, description=f"Permission denied to /proc/{pid}/io")
    return state

class IOFile:
    """ Class to represent the number of bytes read and written by a process
    """
    def __init__(self, write_bytes: int, read_bytes: int):
        self.write_bytes = write_bytes
        self.read_bytes = read_bytes

    def to_dict(self):
        """ Convert the IOFile object to a dictionary
        """
        return {'write_bytes': self.write_bytes, 'read_bytes': self.read_bytes}

def format_content(content: str) -> dict:
    """ Format the content of the file
    """
    lines = content.split('\n')
    line_collection = [line.split(':') for line in lines if line]
    content = {line[0].strip(): int(line[1].strip()) for line in line_collection}
    return content

def read_counter_state(file_name: str) -> dict:
    """ Read the number of bytes read and written by a process
    """
    with open(file_name, 'r', encoding="utf-8") as file:
        content = file.read()
    content_dict = format_content(content)
    io_file = IOFile(write_bytes=content_dict['write_bytes'], read_bytes=content_dict['read_bytes'])
    return io_file.to_dict()

if __name__ == '__main__':
    app.run()
