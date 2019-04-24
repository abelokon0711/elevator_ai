from environment import Environment
from graphics import Graphics
import time
import threading

env = Environment()
gra = Graphics(env)
t = threading.Thread(target=gra.start)
t.start()
running = True

try:
    while running:
        if not t.is_alive():
            running = False
            break
            
        time.sleep(0.5)
        env.tick()
        gra.tick()
except KeyboardInterrupt:
    print("STATISTACS SKR SKR SKAA")
finally:
    print("FIREABEND")

