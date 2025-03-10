from tkinter import *
from tkinter.font import *
import webbrowser


def orderWindow():
    orderScreen = Tk(className='Swift app - Order')
    orderScreen.geometry("500x400")

    com12 = Font(family="Comic Sans", size=12, weight="bold")
    welcomeMessage = Label(orderScreen, text="Choose from the following options:", wraplength=300, font=com12)
    welcomeMessage.place(x=20, y=20)

    com10 = Font(family="Comic Sans", size=10, weight="bold")
    def radioPrompt1():
        enterPrice = Label(orderScreen, text="Price: 2000 PKR", background='Plum1',wraplength=300, font=com10)
        enterPrice.place(x=150, y=60)

    def radioPrompt2():
        enterPrice = Label(orderScreen, text="Price: 3000 PKR", background='Plum1',wraplength=300, font=com10)
        enterPrice.place(x=150, y=100)

    var = IntVar()
    R1 = Radiobutton(orderScreen, text="Debit Card", variable=var, value=1, font=com10, command=radioPrompt1)
    R1.place(x=20, y=60)

    R2 = Radiobutton(orderScreen, text="Credit Card", variable=var, value=2,font=com10,command=radioPrompt2)
    R2.place(x=20, y=100)


    numEntry = Label(orderScreen,text='Phone#', font=com10)
    numEntry.place(x=20, y=170)
    numEntry = Entry(orderScreen, background="snow", font=com10)
    numEntry.place(x=150, y=170)

    postalCode = Label(orderScreen,text='Postal Code: ', font=com10)
    postalCode.place(x=20, y=210)
    postalCode = Entry(orderScreen, background="snow", font=com10)
    postalCode.place(x=150, y=210)

    address = Label(orderScreen,text='Address: ', font=com10)
    address.place(x=20, y=250)
    address = Entry(orderScreen, background="snow", font=com10)
    address.place(x=150, y=250)

    # Radio Buttons:
    var = IntVar()
    R1 = Radiobutton(orderScreen, text="Cash On Delivery", variable=var, value=2,indicator=0,font=com10,background="light blue")
    R1.place(x=30, y=325)

    R2 = Radiobutton(orderScreen, text="Online Banking", variable=var, value=1, indicator=0, font=com10, background="light blue")
    R2.place(x=30, y=300)

    R3 = Radiobutton(orderScreen, text="Wire Transfer", variable=var, value=3,indicator=0,font=com10,background="light blue")
    R3.place(x=30, y=350)

    def submitPress():
        orderScreen.destroy()

    # Submit Button:
    submit = Button(orderScreen,text='Submit',background='PaleGreen1',
                    font=('Comic Sans',15), command=submitPress)
    submit.place(x=350, y=310)

    orderScreen.mainloop()
