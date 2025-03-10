from tkinter import *
from tkinter.font import *
from mainMenu import *


def loginWindow():
    loginView = Tk(className='Swift app - Login')
    loginView.geometry("400x250")

    com15 = Font(family="Comic Sans", size=15, weight="bold")

    userLabel = Label(loginView, text="Username:", wraplength=300, font=com15)
    userLabel.place(x=30, y=60)
    userEntry = Entry(loginView, background="LemonChiffon2", font=com15)
    userEntry.place(x=140, y=60)

    passLabel = Label(loginView, text="Password:", wraplength=300, font=com15)
    passLabel.place(x=30, y=110)
    passEntry = Entry(loginView, background="LemonChiffon2", font=com15)
    passEntry.place(x=140, y=110)

    def sent():
        loginView.destroy()

    def send():
        loginView.destroy()
        mainM()

    def resetPass():
        forgotPass.destroy()
        passLabel.destroy()
        passEntry.destroy()
        userLabel.destroy()
        userEntry.destroy()
        loginButton.destroy()
        linkLine = Label(loginView, text="Enter your email to receive reset link: ", font=("Comic Sans", 15))
        linkLine.place(x=20, y=60)
        resetLink = Entry(loginView, background="LemonChiffon2", font=("Comic Sans", 18))
        resetLink.place(x=50, y=110)
        sendLink = Button(loginView, text="Send", font=("Comic Sans", 12), command=sent)
        sendLink.place(x=50, y=150)

    forgotPass = Button(loginView, text="Forgot Password?", wraplength=300, font=("Comic Sans", 12), command=resetPass)
    forgotPass.place(x=140, y=160)

    loginButton = Button(loginView, text="Login",background='PaleGreen1', wraplength=300, font=("Comic Sans", 12), command=send)
    loginButton.place(x=60, y=160)

    loginView.mainloop()
