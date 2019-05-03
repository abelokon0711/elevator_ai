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
    sleep(0.5)

try:
    while running:
        env.tick()

        if ENABLE_GRAPHICS:
            if not t.is_alive():
                running = False
                break
            gra.tick()

        sleep(0.5)

except KeyboardInterrupt:
    print("")
finally:
    print("Ended")
