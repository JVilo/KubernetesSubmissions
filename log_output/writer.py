import time
import uuid
from datetime import datetime, timezone

random_string = str(uuid.uuid4())
file_path = "/shared/log.txt"

while True:
    now = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    with open(file_path, "a") as f:
        f.write(f"{now}: {random_string}\n")
    time.sleep(5)
