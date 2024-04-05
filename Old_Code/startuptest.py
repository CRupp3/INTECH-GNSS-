# testing running python on startup
import time
from time import strftime

for i in range(10):
    time.sleep(1)  # sleep 1 second
    print(strftime("%S"))

file1 = open("write.txt", "a")
file1.write('hello world')
file1.close()
