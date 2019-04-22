from environment import Environment
from graphics import Graphics
import time
import threading

env = Environment()
t = threading.Thread(target=Graphics.start)
t.start()


try:
    while True:
        time.sleep(1)
        env.tick()
        Graphics.tick()
except KeyboardInterrupt:
    print("STATISTACS SKR SKR SKAA")
    print("FIREABEND")



