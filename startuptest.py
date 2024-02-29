# testing running python on startup
import time
from time import strftime

while True:
    time.sleep(1)  # sleep 1 second
    print(strftime("%S"))
