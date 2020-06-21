from os import path
import logging
from pathlib import Path

import re
import json
import base64

from models import Resource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

root_folder = Path(__file__).parent.parent.absolute()

data_directory = path.join(
    root_folder, 'resources/har_files')
destination_directory = path.join(
    root_folder, 'dist')


def touch_file(filename):
    """Ensures the given file exists.
    """
    tokens = filename.split('/')
    folders = tokens[:-1]

    folder = '/'.join(folders)
    local_path = Path(filename)

    Path(folder).mkdir(parents=True, exist_ok=True)

    local_path.touch(exist_ok=True)


def export_har_file(filename: str) -> None:
    with open(filename, 'r') as file:
        data = file.read()

    resources = json.loads(data)

    for entry in resources["log"]["entries"]:
        resource = Resource(entry)

        if resource.is_image():
            fullpath = resource.get_fullpath()
            final_path = re.sub('(\?.*)',
                              '',
                              path.join(destination_directory, fullpath))

            content = resource.get_content()
            bytes = base64.b64decode(content['text'])

            touch_file(final_path)

            with open(final_path, 'wb') as f:
                f.write(bytes)

def export_har_files():
    files = Path(data_directory).rglob("*.har.json")
    for file in files:
        export_har_file(file)
    

if __name__ == "__main__":
    export_har_files()
