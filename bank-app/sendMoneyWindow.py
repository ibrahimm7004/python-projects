from tkinter import *
from tkinter.font import *


def sendMoneyWindow():
    sendMoneyWindow = Tk(className='Swift app - Transfer Money')
    sendMoneyWindow.geometry("450x350")
    com15 = Font(family="Comic Sans", size=15, weight="bold")

    userLabel = Label(
        sendMoneyWindow, text="Enter Recipient Username: ", font=com15)
    userLabel.place(x=40, y=25)
    userLabel = Entry(sendMoneyWindow, font=com15)
    userLabel.place(x=45, y=60)

    amtLabel = Label(sendMoneyWindow, text="Enter Amount: ", font=com15)
    amtLabel.place(x=40, y=100)
    amtLabel = Entry(sendMoneyWindow, font=com15)
    amtLabel.place(x=45, y=135)

    displayBalance = Label(sendMoneyWindow, text="Current Balance:", wraplength=300, background="dark sea green",
                           font=('Comic Sans', 16, 'bold'))
    displayBalance.place(x=40, y=230)
    displayBalance = Label(sendMoneyWindow, text="Rs. 432534", wraplength=300, background="LemonChiffon2",
                           font=('Comic Sans', 24, 'bold'))
    displayBalance.place(x=40, y=260)

    transfer = Button(sendMoneyWindow, text="Transfer", background="Light Blue",
                      wraplength=150, font=('Comic Sans', 17, 'bold'))
    transfer.place(x=300, y=140)

    limitLabel = Label(sendMoneyWindow, text="Remaining Daily Limit:", background="Light Blue", wraplength=150,
                       font=('Comic Sans', 17, 'bold'))
    limitLabel.place(x=280, y=210)
    limitLabel = Label(sendMoneyWindow, text="Rs. 47400/50000", background="LemonChiffon2", wraplength=150,
                       font=('Comic Sans', 17, 'bold'))
    limitLabel.place(x=280, y=270)

    sendMoneyWindow.mainloop()
