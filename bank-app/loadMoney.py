from tkinter import *
from tkinter.font import *


def loadMoneyWindow():
    loadMoneyWindow = Tk(className='Swift app - Load Money')
    loadMoneyWindow.geometry("450x350")
    com15 = Font(family="Comic Sans", size=15, weight="bold")

    def checkered(canvas, line_distance):
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, canvas_width, line_distance):
            canvas.create_line(x, 0, x, canvas_height, fill="dark green")
        canvas.create_line(600, 0, 600, canvas_height, fill="dark green")
        # horiz. lines at an interval of "line_distance" pixel
        for y in range(line_distance, canvas_height, line_distance):
            canvas.create_line(0, y, canvas_width, y, fill="dark green")
        canvas.create_line(0, 160, canvas_width, 160, fill="dark green")

    canvas_width = 500
    canvas_height = 350
    w = Canvas(loadMoneyWindow,
               width=canvas_width,
               height=canvas_height)
    w.pack()

    checkered(w, 20)

    userLabel = Label(loadMoneyWindow, text="Your Transaction ID:",
                      background='light yellow', font=com15)
    userLabel.place(x=110, y=120)
    userLabel = Label(loadMoneyWindow, text="IBAN: 682734598269 ",
                      background='powder blue', font=com15)
    userLabel.place(x=110, y=160)

    loadMoneyWindow.mainloop()
