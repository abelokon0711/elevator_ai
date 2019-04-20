from environment import Environment

env = Environment()

try:
    while True:
        env.tick()
except KeyboardInterrupt:
    print("STATISTACS SKR SKR SKAA")
    print("FIREABEND")
