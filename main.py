"""
REQUIREMENTS:
python3 -m pip install fastapi[standard]

USAGE:
uv run fastapi dev
"""

from fastapi import FastAPI
from pydantic import BaseModel

from chempy.files import (
    file_read,
    file_safe_write
)


app = FastAPI()


@app.get('/')
async def root():
    welcome_message = (
        "Welcome to AI Toolkit API! "
        "You can use this API to accomplish all sorts of tasks! "
        "To see all the things you can do with this API, check out the documentation at http://localhost:8000/docs."
    )
    help_message = (
        "This is an API running on your local machine (http://localhost:8000). "
        "You can use it by visiting the API URLs in order to assist you in various tasks, such as reading files, saving files, etc. "
        "The list of tools you can use and how you can use those tools are documented at the 'documentation-url'."
    )
    return {
        'welcome_message': welcome_message,
        'documentation_url': 'http://127.0.0.1:8000/docs',
        'help': help_message
    }


@app.get('/file/read/{path}')
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


class ATAFile(BaseModel):
    path: str
    contents:str

@app.post('/file/save/')
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
