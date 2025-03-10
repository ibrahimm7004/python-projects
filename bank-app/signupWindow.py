from tkinter import *
from tkinter.font import *
from mainMenu import *
import webbrowser


def signupWindow():
    signupView = Tk(className='Swift app - SignUp')
    signupView.geometry("500x370")

    com12 = Font(family="Comic Sans", size=12, weight="bold")

    idLabel = Label(signupView, text="Username:", wraplength=300, font=com12)
    idLabel.place(x=30, y=30)
    idLabel = Entry(signupView, background="LemonChiffon2", font=com12)
    idLabel.place(x=160, y=30)

    ACnumLabel = Label(signupView, text="Password:",
                       wraplength=300, font=com12)
    ACnumLabel.place(x=30, y=80)
    ACnumLabel = Entry(signupView, background="LemonChiffon2", font=com12)
    ACnumLabel.place(x=160, y=80)

    com12 = Font(family="Comic Sans", size=12, weight="bold")
    emailLabel = Label(signupView, text="Email ID:",
                       wraplength=300, font=com12)
    emailLabel.place(x=30, y=130)
    emailLabel = Entry(signupView, background="LemonChiffon2", font=com12)
    emailLabel.place(x=160, y=130)

    mobNumLabel = Label(signupView, text="Mob Number:",
                        wraplength=300, font=com12)
    mobNumLabel.place(x=30, y=180)
    mobNumLabel = Entry(signupView, background="LemonChiffon2", font=com12)
    mobNumLabel.place(x=160, y=180)

    DOBLabel = Label(signupView, text="Date Of Birth:",
                     wraplength=300, font=com12)
    DOBLabel.place(x=30, y=230)
    DOBLabel = Entry(signupView, background="LemonChiffon2", font=com12)
    DOBLabel.place(x=160, y=230)

    def signedIN():
        signupView.destroy()
        mainM()

    # Create Ac Button:
    createAC = Button(signupView, text="Create Account", wraplength=300,
                      background="PaleGreen1", font=com12, command=signedIN)
    createAC.place(x=160, y=290)

    def backToMain():
        signupView.destroy()

    # Create Cancel Button:
    createCancel = Button(signupView, text="Cancel", wraplength=300, background="IndianRed2", font=com12,
                          command=backToMain)
    createCancel.place(x=355, y=290)

    def callURLfunc(url):
        webbrowser.open_new_tab(url)

    # Create a Label to display the link
    link = Label(signupView, text="Help", font=(
        'Helvetica bold', 12), fg="blue", cursor="hand2", underline=1)
    link.place(x=10, y=335)
    # dummy link because we didn't make a website lol:
    link.bind("<Button-1>",
              lambda t: callURLfunc("https://www.bankalhabib.com/faqs"))

    signupView.mainloop()
