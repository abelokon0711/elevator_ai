from passenger import Passenger


class Generator:

    def __init__(self, environment):
        self.environment = environment

    def tick(self):
        if self.environment.get_clock() % self.environment.TICKS_NEEDED_TO_GENERATE_PASSENGER == 0:
            for i in range(self.environment.PASSENGERS_TO_BE_GENERATED):
                # GET ID FROM ENVIRONMENT PASSENGER LIST
                i + 0  # HACK: fix unused variable warning
                p = Passenger(self.environment)
                self.environment.add_passenger(p)
