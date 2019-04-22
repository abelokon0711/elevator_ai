from tkinter import *

 
class Graphics:


    def start():
        master = Tk()

        canvas_width = 500
        canvas_height = 500
        w = Canvas(master, 
                   width=canvas_width,
                   height=canvas_height)
        w.pack()

        y = int(canvas_height / 2)
        w.create_line(0, y, canvas_width, y, fill="#476042")


        mainloop()

    def tick():
        pass