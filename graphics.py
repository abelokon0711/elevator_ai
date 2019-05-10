from tkinter import Tk, Canvas


class Graphics:

    def __init__(self, env):
        self.running = True
        self.environment = env
        self.cv_width = 600
        self.cv_height = 600
        self.padding = 100
        self.floor_margin = (
                (self.cv_height-self.padding)
                / self.environment.number_of_floors)
        self.floor_pos = []

    def start(self):
        self.master = Tk()
        self.master.title("AI elevator simulation")

        self.c = Canvas(
                self.master,
                width=self.cv_width,
                height=self.cv_height)
        self.c.pack()

        self.generate_floors()
        self.floor_pos.reverse()
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.mainloop()

    def on_closing(self):
        self.master.destroy()

    def tick(self):
        if not self.running:
            return
        self.c.delete("all")
        self.draw_environment()

    def generate_floors(self):
        """This will create the coordinates of the floor lines and add them
        to the floor_pos array in the form of x1, y1, x2, y2 where y1 and y2
        are the same values"""
        for i in range(self.environment.number_of_floors):
            self.floor_pos.append(
                    [self.cv_width / 2,
                        self.padding + self.floor_margin * i,
                        self.cv_width,
                        self.padding + self.floor_margin * i])

    def draw_environment(self):
        # Draw Floors
        for i in range(len(self.floor_pos)):
            self.c.create_line(
                    self.floor_pos[i][0],
                    self.floor_pos[i][1],
                    self.floor_pos[i][2],
                    self.floor_pos[i][3],
                    fill="white")
            self.c.create_text(
                    self.floor_pos[i][0] - 20,
                    self.floor_pos[i][1],
                    fill="black",
                    font="Times 16 italic bold",
                    text=str(i))  # Floor Number Text
            self.c.create_text(
                    self.floor_pos[i][0] - 180,
                    self.floor_pos[i][1] - 50,
                    fill="black",
                    font="Times 15 italic bold",
                    text="Waiting persons: "
                    + str(len(self.environment.floors[i].waiting_queue)))

        # Draw Elevators
        for i, elevator in enumerate(self.environment.elevators):
            x1 = self.floor_pos[elevator.current_floor][0] + i*60 + 10
            x2 = x1 + 50
            y2 = self.floor_pos[elevator.current_floor][1]
            y1 = y2 - (self.floor_margin / 2)

            my = y2 - 25
            mx = x2 - 25

            self.c.create_rectangle(x1, y1, x2, y2, fill="red")
            self.c.create_text(
                    mx,
                    my,
                    fill="white",
                    font="Times 10 italic bold",
                    text="{}/{}".format(
                        len(elevator.passenger_in_elevator),
                        elevator.capacity)
                    )
