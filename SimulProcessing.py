from multiprocessing import Process
import time
import os


def acquire_data(arg):
    for i in range(5):
        print('acquiring data: {}'.format(i))
        time.sleep(1.1)

def capture_video():
    for i in range(5):
        print('capturing video')
        time.sleep(1)

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    p_data = Process(target=acquire_data, args=('foo',))
    p_video = Process(target=capture_video)
    p_data.start()
    p_video.start()
    p_data.join()  # wait until acquire_data is done
    p_video.join()  # wait also until capture_video is done

    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()