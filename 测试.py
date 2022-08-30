import os
import threading
file = open("path.txt", "r")
paths = file.readlines()
file.close()
# print(path)


def run(p):
    os.system(p)


for path in paths:
    p = path.replace("\n", "")
    print(p)
    threading.Thread(target=run, args=(p,)).start()
