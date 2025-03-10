from tkinter import *
from tkinter.font import *
from loginWindow import *
from signupWindow import *


def close():
    welcomeWindow.destroy()
    # OR use welcomeWindow.quit()


def login():
    welcomeWindow.destroy()
    loginWindow()


def signup():
    welcomeWindow.destroy()
    signupWindow()


# welcomeWindow is an object of tkinter class
welcomeWindow = Tk(className='Swift app - Welcome')


def checkered(canvas, line_distance):
    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance, canvas_width, line_distance):
        canvas.create_line(x, 0, x, canvas_height, fill="dark green")
    canvas.create_line(600, 0, 600, canvas_height, fill="dark green")
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance, canvas_height, line_distance):
        canvas.create_line(0, y, canvas_width, y, fill="dark green")
    canvas.create_line(0, 160, canvas_width, 160, fill="dark green")


canvas_width = 500
canvas_height = 350
w = Canvas(welcomeWindow,
           width=canvas_width,
           height=canvas_height)
w.pack()

checkered(w, 40)

luc45 = Font(family="Lucida Console", size=25,
             weight="normal")  # defining a font to use

welcomeWindow.geometry("400x350")  # setting the dimensions of this window

bankTitle = Label(welcomeWindow, text="Welcome to SWIFT", font=luc45,
                  wraplength=320)  # bankTitle is an object of class Label
bankTitle.place(x=50, y=50)  # Used to add a widget(Label) to a window
bankTitle = Label(welcomeWindow, text="Mobile Banking", font=('Lucida Console', 25, 'bold'),
                  wraplength=300)
bankTitle.place(x=50, y=100)

# Fonts:
mon25 = Font(family="Montserrat", size=25, weight="bold")
mon15 = Font(family="Montserrat", size=15, weight="bold")

exitButton = Button(welcomeWindow, background='light green',
                    text="Exit", font=mon15, command=close)
LoginButton = Button(welcomeWindow, background='linen',
                     text="Login", font=mon25, command=login)
SignupButton = Button(welcomeWindow, background='RosyBrown1',
                      text="Sign Up", font=mon15, command=signup)


def callURLfunc(url):
    webbrowser.open_new_tab(url)


# Create a Label to display the link
link = Label(welcomeWindow, text="About", font=(
    'Helvetica bold', 15), fg="blue", cursor="hand2", underline=1)
link.place(x=10, y=310)
link.bind("<Button-1>", lambda r: callURLfunc("https://www.bankalfalah.com/about/"))

exitButton.place(x=730, y=435)
LoginButton.place(x=140, y=190)
SignupButton.place(x=155, y=270)

welcomeWindow.mainloop()
