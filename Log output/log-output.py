from random import choices
import string
from datetime import datetime
import time

random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase, k=32))
timestamp = datetime.now().isoformat()

while True:
    timestamp = datetime.now().isoformat()
    print(str(timestamp)+random_string)
    time.sleep(5)