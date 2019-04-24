from environment import Environment
from graphics import Graphics
import time
import threading
import sys

ENABLE_GRAPHICS = True
running = True

env = Environment()

if ENABLE_GRAPHICS :
    gra = Graphics(env)
    t = threading.Thread(target=gra.start)
    t.start()

try:
    while running:
        if ENABLE_GRAPHICS: 
            if not t.is_alive():
                running = False
                sys.exit(0)
                break
                
        time.sleep(0.5)
        env.tick()
        if ENABLE_GRAPHICS:
            gra.tick()
except KeyboardInterrupt:
    print("STATISTACS SKR SKR SKAA")
finally:
    print("FIREABEND")

