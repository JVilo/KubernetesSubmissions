import sys
import time
import uuid
from datetime import datetime, UTC

random_string = str(uuid.uuid4())

while True:
    timestamp = datetime.now(UTC).isoformat(timespec='milliseconds')
    print(f"{timestamp}: {random_string}")
    sys.stdout.flush()
    time.sleep(5)

