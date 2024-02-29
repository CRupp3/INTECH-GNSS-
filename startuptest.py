# testing running python on startup
import time
from time import strftime

for i in range(30):
    time.sleep(1)  # sleep 1 second
    print(strftime("%S"))
