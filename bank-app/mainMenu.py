from tkinter import *
from tkinter.font import *
from sendMoneyWindow import *
from orderWindow import *
from loadMoney import *
import webbrowser

def mainM():
    mainMenu = Tk(className='Swift app - Main Menu')
    mainMenu.geometry("500x350")
    # mainMenu.configure(bg='light blue')

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
    w = Canvas(mainMenu,
               width=canvas_width,
               height=canvas_height)
    w.pack()

    checkered(w, 40)

    com40 = Font(family="Comic Sans", size=40, weight="bold")
    welcomeMessage = Label(mainMenu, text="Welcome User!", wraplength=300, background="light green", font=com40)
    welcomeMessage.place(x=20, y=20)

    def showBalance():
        hiddenBalance.destroy()
        newLabel = Label(mainMenu, text="Rs. 65326", wraplength=300,background='powder blue', font=('Helvetica Bold', 25))
        newLabel.place(x=305, y=95)

    com15 = Font(family="Comic Sans", size=15, weight="bold")
    displayBalance = Button(mainMenu, text="Display Balance", wraplength=300, background="LemonChiffon2", font=com15,command=showBalance)
    displayBalance.place(x=300, y=40)

    hiddenBalance = Label(mainMenu, text="Rs. ******", wraplength=300, font=('Helvetica Bold', 25))
    hiddenBalance.place(x=310, y=95)

    def sendMoney():
        mainMenu.destroy()
        sendMoneyWindow()

    def ldMoney():
        mainMenu.destroy()
        loadMoneyWindow()

    sendMoney = Button(mainMenu, text="Send Money", wraplength=300, background="light yellow", font=com15, command=sendMoney)
    sendMoney.place(x=20, y=200)

    loadMoney = Button(mainMenu, text="Load Money", wraplength=300, background="light pink", font=com15, command=ldMoney)
    loadMoney.place(x=20, y=260)

    # transactionHistory = Button(mainMenu, text="Transaction History", wraplength=300, background="Lavender", font=com15)
    # transactionHistory.place(x=20, y=320)


    def cardOrder():
        mainMenu.destroy()
        orderWindow()


    # com10 = Font(family="Comic Sans", size=10, weight="bold")
    # card = Button(mainMenu, text="Order Card", background="LightCyan2", font=com10, command=cardOrder)
    # card.place(x=300, y=200)


    com10 = Font(family="Comic Sans", size=15, weight="bold")
    card = Button(mainMenu, text="Order Card", background="LightCyan2", font=com10, command=cardOrder)
    card.place(x=320, y=200)

    def callURLfunc(url):
        webbrowser.open_new_tab(url)


    def chatButton():
        liveChat.bind("<Button-1>", lambda r: callURLfunc("https://chat.meezanbank.com/Chat"))


    liveChat = Button(mainMenu, text="Live Chat", background="LightCyan2", font=com10, command=chatButton)
    liveChat.place(x=320, y=270)

    # background_image = PhotoImage(file='a.png')
    # Label(mainMenu,image=background_image).place(x=0,y=0)

    # progress = Progressbar(mainMenu, orient = HORIZONTAL,
    #               length = 100, mode = 'determinate')
    # progress.pack(pady = 10)


    mainMenu.mainloop()
