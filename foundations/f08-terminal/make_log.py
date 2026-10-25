"""F8: writes a fake application log, one line every half second, so you can watch it with tail -f.

Run:  python3 foundations/f08-terminal/make_log.py > app.log &   then   tail -f app.log
"""

import os
import random
import time
from datetime import datetime

if "SEED" in os.environ:          # same "random" log every time, handy for demos
    random.seed(int(os.environ["SEED"]))
service = os.environ.get("SERVICE_NAME", "demo-service")
events = ["INFO request served in 120 ms", "INFO request served in 95 ms",
          "WARNING slow response: 2100 ms", "ERROR upstream timeout after 5000 ms"]
for _ in range(int(os.environ.get("LINES", "20"))):
    print(f"{datetime.now():%H:%M:%S} {service} {random.choices(events, weights=[5, 5, 2, 1])[0]}", flush=True)
    time.sleep(float(os.environ.get("DELAY", "0.5")))
