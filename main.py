"""
REQUIREMENTS:
python3 -m pip install fastapi[standard]

USAGE:
uv run fastapi dev
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel

from chempy.conf import read_conf
from chempy.files import (
    file_read,
    file_safe_write,
    dir_contents
)


app = FastAPI()

## Configure App
APP_HOST_DEFAULT = 'localhost'
APP_PORT_DEFAULT = '8000'
APP_HOST = APP_HOST_DEFAULT
APP_PORT = APP_HOST_DEFAULT
try:
    config = read_conf('./ai-toolkit-api.conf')
    if 'host' in config: APP_HOST = config['host']
    if 'port' in config: APP_PORT = config['port']
except:
    print('[WARN] Failed to load config file.')


class ATAFile(BaseModel):
    path: str
    contents:str


@app.get('/')
async def root():
    welcome_message = (
        "Welcome to AI Toolkit API! "
        "You can use this API to accomplish all sorts of tasks! "
        f"To see all the things you can do with this API, check out the documentation at http://{APP_HOST}:{APP_PORT}/docs."
    )
    help_message = (
        f"This is an API running on your local machine (http://{APP_HOST}:{APP_PORT}). "
        "You can visit the API URLs to complete tasks, such as reading files, saving files, etc. "
        "The list of tools you can use and how you can use those tools are documented at the 'documentation-url'."
    )
    return {
        'welcome_message': welcome_message,
        'documentation_url': f'http://{APP_HOST}:{APP_PORT}/docs',
        'help': help_message
    }


@app.get('/file/read/{path}', description='Read a file from the local system.')
async def read_file(path:str) -> str:
    try:
        contents = file_read(path)
        success = True
    except:
        contents = None
        success = False
    return {
        'success': success,
        'path': path,
        'contents': contents,
    }


@app.post('/file/save/', description='Save a file to the local system.')
async def save_file(file_details: ATAFile) -> bool:
    path = file_details.path
    contents = file_details.contents
    result = file_safe_write(path=path, contents=contents)
    if result:
        message = f'File saved to {path}'
    else:
        message = 'File failed to save!'
    return {
        'success': result,
        'path': path,
        'message': message,
    }


@app.get('/environment/working_directory', description='Get the current working directory.')
def get_working_directory():
    return os.getcwd()


@app.get('/file/directory_contents/{directory_path}', description='Recursively list the contents of a specified directory.')
def get_dir_contents(directory_path:str):
    contents = get_dir_contents(path=directory_path, recursive=True)
    return contents
