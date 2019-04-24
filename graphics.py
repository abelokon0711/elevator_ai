from tkinter import *
 
class Graphics:

    def __init__(self, env):
        self.master = None
        self.c = None
        self.environment = env
        self.cv_width = 600
        self.cv_height = 800
        self.padding = 100
        self.floor_margin = (self.cv_height-self.padding) / self.environment.number_of_floors
        self.floor_pos = []

    def start(self):
        self.master = Tk()
        self.master.title("Aufzug AI Simulation")

        self.c = Canvas(self.master, 
                   width=self.cv_width,
                   height=self.cv_height)
        self.c.pack()

        self.generate_floors()
        self.floor_pos.reverse()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.mainloop()

    def on_closing(self):
        self.master.destroy()

    def tick(self):
        self.c.delete("all")
        self.draw_environment()

    
    def generate_floors(self):
        for x in range(self.environment.number_of_floors):
            self.floor_pos.append([self.cv_width / 2, self.padding + self.floor_margin * x, self.cv_width, self.padding + self.floor_margin * x])


    def draw_environment(self):
        # Draw Floors
        for x in range(len(self.floor_pos)):
            self.c.create_line(self.floor_pos[x][0], self.floor_pos[x][1], self.floor_pos[x][2], self.floor_pos[x][3], fill="#000000")
            self.c.create_text(self.floor_pos[x][0] - 20 , self.floor_pos[x][1], fill="black", font="Times 16 italic bold", text=str(x)) #Floor Number Text
            self.c.create_text(self.floor_pos[x][0] - 180 , self.floor_pos[x][1] - 50, fill="black", font="Times 15 italic bold", text="Wartende Personen: " + str(len(self.environment.floors[x].waiting_queue)))

        # Draw Elevators
        for x in range(len( self.environment.elevators)):
            x1 = self.floor_pos[self.environment.elevators[x].current_floor][0] + (x*60) + 10
            x2 = x1 + 50
            y2 = self.floor_pos[ self.environment.elevators[x].current_floor][1]
            y1 = y2 - (self.floor_margin / 2)
            
            my =  y2 - 25
            mx =  x2 - 25
           
            self.c.create_rectangle(x1,y1,x2,y2, fill="#ff0000") #create_rectangle(x0, y0, x1, y1, option, ...)
            self.c.create_text(mx,my, fill="white", font="Times 10 italic bold", text=str(len(self.environment.elevators[x].passenger_in_elevator)) + " / " + str(self.environment.elevators[x].capacity))

            

        