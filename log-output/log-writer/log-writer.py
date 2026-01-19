from random import choices
import string
from datetime import datetime
import os
import time

directory = os.path.join('files')
filePath = os.path.join(directory, 'log.txt')
os.makedirs(directory, exist_ok=True)

random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase, k=32))

while True:
    time_stamp = str(datetime.now().isoformat())
    content = f'{time_stamp}: {random_string}'

    with open(filePath, "w") as f:
            f.write(content)
            
    time.sleep(5)