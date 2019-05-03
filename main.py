from environment import Environment
from graphics import Graphics
from time import sleep
from threading import Thread

ENABLE_GRAPHICS = True
running = True

env = Environment()

if ENABLE_GRAPHICS:
    gra = Graphics(env)
    t = Thread(target=gra.start)
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
