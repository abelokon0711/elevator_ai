from environment import Environment
from graphics import Graphics
import time
import threading

env = Environment()
gra = Graphics(env)
t = threading.Thread(target=gra.start)
t.start()


try:
    while True:
        time.sleep(0.5)
        env.tick()
        gra.tick()

        if not t.is_alive():
            break
except KeyboardInterrupt:
    print("STATISTACS SKR SKR SKAA")
finally:
    print("FIREABEND")

