'''
Main application file for the BlackJack game.
This file contains the Application class for the BlackJack application.
'''
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from User import Users, User
from BlackJack import BlackJack
from random import shuffle

class Application:
    '''Main Tkinter Application class'''
    root = Tk()
    userlist = Users()

    def __init__(self) -> None:
        '''Initialize the application'''
        root = self.root
        root.title("Black Jack")
        root.geometry("800x600+300+50")
        root.minsize(800, 600)
        root.state('zoomed')

        # png icon for window
        root.iconbitmap('images/cards.ico')

        img = Image.open('images/background.png')
        img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.resizedBgImg = ImageTk.PhotoImage(img)
  
        img2 = Image.open('images/background2.png')
        img2 = img2.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.resizedBgImg2 = ImageTk.PhotoImage(img2)

        self.frames = [Frame(root) for i in range(5)]
        for frame in self.frames:
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame.pack_propagate(0)
        
        parent = self.frames[0]
        parent.tkraise()

        #background image on root
        Label(parent, image=self.resizedBgImg).place(relx=0, rely=0, relwidth=1, relheight=1)

        #button on top right corner for main menu
        self.mainMenuBtn = Button(parent, text='Main Menu', command=self.main_menu)
        self.mainMenuBtn.config(self.ButtonStyle(17, 2))
        self.mainMenuBtn.pack(anchor=NE, padx=50, pady=50)


        # Load all 54 card images
        specialCards = ['Ace', 'Jack', 'Queen', 'King']
        suits = ['spades', 'hearts', 'clubs', 'diamonds']
        
        self.outerCardList = []
        self.outerCardNames = []
        for suit in suits:

            for i in range(2, 11):
                img = Image.open(f'cards/{suit}/{i}.png').resize((104, 154))
                img = ImageTk.PhotoImage(img)
                self.outerCardList.append(img)
                self.outerCardNames.append((suit ,i))
          
            for card in specialCards:
                img = Image.open(f'cards/{suit}/{card}.png').resize((104, 154))
                img = ImageTk.PhotoImage(img)
                self.outerCardList.append(img)
                self.outerCardNames.append((suit, card))


        #Load inverted card image
        img = Image.open('cards/inverted.png').resize((104, 154))
        self.InvertedImg = ImageTk.PhotoImage(img)

        #load Rules image
        img = Image.open('images/Rules.png').resize((604, 604))
        self.RulesImg = ImageTk.PhotoImage(img)

        self.run()


    def ButtonStyle(self, width, height):
        '''Create a custom style for buttons'''
        # Global style for Buttons
        self.globalButtonStyle = {'font': ('Arial', 13, "bold"),
                            'bg': 'white', 'fg': 'red',
                            'relief': 'flat',
                            'cursor': 'hand2'
                            }

        buttonStyle = self.globalButtonStyle
        buttonStyle['width'] = width
        buttonStyle['height'] = height
        return buttonStyle


    def main_menu(self) -> None:
        '''Main menu screen'''

        parent = self.frames[1]
        parent.tkraise()

        #background image on root
        Label(parent, image=self.resizedBgImg2).pack(fill=BOTH, expand=True)

        #back Button
        self.backBtn = Button(parent, text='Back', command=self.frames[0].tkraise)
        self.backBtn.config(self.ButtonStyle(8, 2))
        self.backBtn.place(relx=0.04, rely=0.06)

        # four buttons for the main menu, named select username, History, Rules and Exit.
        selectUsernameBtn = Button(parent, text='Select Username', command = self.addUsername)
        selectUsernameBtn.place(relx=0.5, rely=0.3, anchor=CENTER)
        historyBtn = Button(parent, text='History', command=self.HistoryScreen)
        historyBtn.place(relx=0.5, rely=0.4, anchor=CENTER)
        rulesBtn = Button(parent, text='Rules', command=self.Rules)
        rulesBtn.place(relx=0.5, rely=0.5, anchor=CENTER)
        exitBtn = Button(parent, text='Exit', command=self.root.destroy)
        exitBtn.place(relx=0.5, rely=0.6, anchor=CENTER)

        #add styles to buttons
        selectUsernameBtn.config(self.ButtonStyle(18, 2))
        historyBtn.config(self.ButtonStyle(18, 2))
        rulesBtn.config(self.ButtonStyle(18, 2))
        exitBtn.config(self.ButtonStyle(18, 2))


    def addUsername(self) -> None:
        '''Add username popup'''
        root = Toplevel(self.root)
        root.title("Add New User")
        root.geometry("300x200+500+200")
        root.configure(bg='#4c7212')
        root.resizable(False, False)
        root.focus()
        root.iconbitmap('images/cards.ico')

        #Label and entry to enter username
        Label(root, text='Enter Username:', bg='#4c7212', fg='white',
               font=('Arial', 12, 'bold')).place(relx=0.1, rely=0.2)
        self.usernameEntry = Entry(root, font=('Arial', 12))
        self.usernameEntry.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.15)

        #Button to add username
        addBtn = Button(root, text='Add')
        addBtn.config(self.ButtonStyle(8, 2), command=lambda:self.addUser(root))
        addBtn.pack(side=BOTTOM, pady=20)


    def addUser(self, root) -> None:
        '''Add user to database'''
        username = self.usernameEntry.get()
        if username:
            self.user = User(username)
            for user in self.userlist.getUsers():
                if user.getName() == self.user.getName():
                    self.user.name = user.name
                    self.user.wins = user.wins
                    self.user.losses = user.losses
                    self.user.draws = user.draws
                    self.user.score = user.score
                    self.userlist.getUsers().remove(user)
            
            self.userlist.addUser(self.user)
            self.gameScreen()
            root.destroy()
        else:
            self.errorScreen('Please enter a username') 


    def HistoryScreen(self) -> None:
        '''Display History Screen'''
        root = Toplevel(self.root)
        root.title("User History")
        root.geometry("800x650+300+50")
        root.configure(bg='#4c7212')
        root.resizable(False, False)
        root.focus()
        root.iconbitmap('images/cards.ico')

        topFrame = Frame(root, bg='#4c7212')
        topFrame.pack(side=TOP, fill=X)

        #Label Named History
        Label(topFrame, text='User History', bg='#4c7212', fg='white',
                font=('Arial', 18, 'bold')).pack(side=TOP, pady=20)
        
       # treeview Frame
        midFrame = Frame(root, bg='#0f0f0f')
        midFrame.pack(side=TOP, fill=BOTH, expand=True, padx=20)

        # treeview
        self.tree = ttk.Treeview(midFrame, columns=(1, 2, 3, 4, 5), show='headings', height=20)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(midFrame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Configure columns
        self.tree.column(1, width=150, anchor='c')
        self.tree.column(2, width=120, anchor='c')
        self.tree.column(3, width=120, anchor='c')
        self.tree.column(4, width=120, anchor='c')
        self.tree.column(5, width=120, anchor='c')

        # Configure headings
        self.tree.heading(1, text='Username')
        self.tree.heading(2, text='Wins')
        self.tree.heading(3, text='Losses')
        self.tree.heading(4, text='Draws')
        self.tree.heading(5, text='Score')
    
        #configure reeview headings and text size seperately
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))
        style.configure('Treeview', font=('Arial', 12))

        #Insert Values in TreeView
        for user in self.userlist.getUsers():
            name = user.getName()
            wins = user.getWins()
            loses = user.getLosses()
            draws = user.getDraws()
            score = user.getScore()
            self.tree.insert('', 'end', values=(name, wins, loses, draws, score))
        
        # Write data to Users.json
        self.userlist.writeToFile()
    
        # Bottom Frame
        bottomFrame = Frame(root, bg='#4c7212')
        bottomFrame.pack(side=TOP, fill=BOTH, expand=True, pady=20)

        #Ok Button
        okBtn = Button(bottomFrame, text='OK', command=root.destroy)
        okBtn.pack(side=TOP, padx=10, pady=5, expand=True)
        okBtn.config(self.ButtonStyle(8, 2))

    def Rules(self) -> None:
        parent = self.frames[3]
        parent.config(bg='#4c7212')
        parent.tkraise()
        
        #show the Rules label
        Label(parent, text='Rules', font=('Arial', 18, 'bold'), bg='#4c7212', fg='white').pack(side=TOP, pady=30)

        #show the rules
        Label(parent, image=self.RulesImg).pack(side=TOP, pady=10)

        #back Button
        backBtn = Button(parent, text='Back', command=self.frames[1].tkraise)
        backBtn.config(self.ButtonStyle(8, 2))
        backBtn.place(relx=0.04, rely=0.06)


    def errorScreen(self, msg) -> None:
        '''Display Error Message'''

        root = Toplevel(self.root)
        root.focus()
        root.title("Error")
        root.geometry("300x250+550+200")    
        root.resizable(False, False)
        root.configure(background='#0f0f0f')

        root.iconbitmap('images/error.ico')

        Label(root, text='Message', font=('Arial', 18, 'bold'), bg='#0f0f0f', fg='white').pack(side=TOP, pady=20)
        Label(root, text=msg, font=('Arial', 13), bg='#0f0f0f', fg='white').pack(side=TOP, pady=10)

        # OK Button
        addButton = Button(root, text='Ok', command=root.destroy)
        addButton.pack(side=LEFT, padx=10, pady=10, expand=True)
        addButton.configure(self.ButtonStyle(15, 2))


    def showCard(self, cardIdx, coord, parent=0):      
        '''Show the card on the screen'''

        if cardIdx == 54:
            image = self.InvertedImg
        else:
            image = self.outerCardList[cardIdx]
        
        if(parent == 0):
            card1 = Label(self.frames[2])
        else:
            card1 = Label(parent)
        card1.config(width=100, height=150)
        card1.config(image=image)
        card1.place(x=coord[0], y=coord[1])
        #on hover mouse cursor changes to hand
        card1.bind('<Enter>', lambda event: card1.config(cursor='hand2'))
        return card1


    def gameScreen(self) -> None:
        '''Display Game Screen'''
        parent = self.frames[2]
        parent.tkraise()

        #background image on root
        Label(parent, image=self.resizedBgImg2).place(relx=0, rely=0, relwidth=1, relheight=1)

        #back Button
        backBtn = Button(parent, text='Back', command=self.frames[1].tkraise)
        backBtn.config(self.ButtonStyle(8, 2))
        backBtn.place(relx=0.04, rely=0.06)

        # Three Buttons for game, named Hit, Stand and Double.
        self.hitBtn = Button(parent, text='Hit')
        self.hitBtn.place(x=1000, y=250)
        self.standBtn = Button(parent, text='Stand')
        self.standBtn.place(x=1000, y=320)

        #add styles to buttons
        self.hitBtn.config(self.ButtonStyle(16, 2))
        self.standBtn.config(self.ButtonStyle(16, 2))

        #Disable buttons 
        self.hitBtn.config(state=DISABLED)
        self.standBtn.config(state=DISABLED)
    
        self.runGameEngine()
    
    def runGameEngine(self) -> None:
        '''Run the game engine'''

        parent = self.frames[2]

        self.gameEngine = BlackJack()
        self.cardList = [i for i in range(0, 52)]
        shuffle(self.cardList)

        #show deck of cards
        self.showDeck(parent)

        self.gameEngine.setDealerCards(self.cardList[0])
        self.gameEngine.setDealerCards(self.cardList[1])
        self.gameEngine.setUserCards(self.cardList[2])
        self.gameEngine.setUserCards(self.cardList[3])

        self.checkConditions()

    def checkConditions(self) -> None:
        '''Check for conditions'''
        condition = self.gameEngine.checkCards()
        if condition == 'draw':
            self.user.gameDraw(self.gameEngine.userScore)
            self.pauseGame("Match Drawn")
        elif condition == 'user':
            self.user.gameWon(self.gameEngine.userScore)
            self.pauseGame(f"{self.user.getName()} Won")
        elif condition == 'dealer':
            self.user.gameLost(self.gameEngine.userScore)
            self.pauseGame(f"{self.user.getName()} Lost")
        elif condition == 'continue':
            self.UserTurn()
            pass
    
    def pauseGame(self, condition):
        '''Pause the game when someone wins or draws'''
        #disable all bindings
        self.cardx.unbind('<Button>')
        self.hitBtn.config(state=DISABLED)
        self.standBtn.config(state=DISABLED)

        self.deckCard1.destroy()
        self.decCard2.destroy()
        self.cardx.destroy()

        #show the dealer's cards
        self.showCard(self.gameEngine.dealerCards[0], (530, 50))
        self.showCard(self.gameEngine.dealerCards[1], (640, 50))

        #show the user's cards
        self.showCard(self.gameEngine.userCards[0], (530, 520))
        self.showCard(self.gameEngine.userCards[1], (640, 520))

        #show the dealer's score
        Label(self.frames[2], text="Dealer Scores: "+str(self.gameEngine.dealerScore),
               font=('Arial', 20, 'bold'), bg='#4c7212', fg='white').place(x=530, y=250)

        #show the user's score
        Label(self.frames[2], text="User Scores: "+str(self.gameEngine.userScore),
               font=('Arial', 20, 'bold'), bg='#4c7212', fg='white').place(x=530, y=390)

        #show the result
        Label(self.frames[2], text=condition, font=('Arial', 20, 'bold'), bg='#4c7212',
               fg='white').place(x=530, y=320)
        

    def UserTurn(self):
        '''User's turn'''
      
        # Enable buttons
        self.hitBtn.config(state=NORMAL, command=self.hit)
        self.standBtn.config(state=NORMAL, command=self.stand)
        pass

    def hit(self):
        '''Hit button function'''
        self.gameEngine.setUserCards(self.cardList[0])
        self.cardList = self.cardList[1:]
        loc = len(self.gameEngine.userCards) - 1
        self.showCard(self.gameEngine.userCards[-1], (530+(loc*110), 520))
        self.checkConditions()
        pass

    def stand(self):
        '''Stand button function'''
        self.gameEngine.setDealerCards(self.cardList[0])
        self.cardList = self.cardList[1:]
        loc = len(self.gameEngine.dealerCards) - 1
        self.showCard(self.gameEngine.dealerCards[-1], (530+(loc*110), 50))
        if (self.gameEngine.dealerScore > 17):
            condition = self.gameEngine.checkDealerConditions()
           
            if condition == 'draw':
                self.user.gameDraw(self.gameEngine.userScore)
                self.pauseGame("Match Drawn")
            elif condition == 'user':
                self.user.gameWon(self.gameEngine.userScore)
                self.pauseGame(f"{self.user.getName()} Won")
            elif condition == 'dealer':
                self.user.gameLost(self.gameEngine.userScore)
                self.pauseGame(f"{self.user.getName()} Lost")
            return
        else:
            self.stand()


    def showDeck(self, parent):
        '''Show the deck of cards'''
        self.deckCard1 = self.showCard(54, (180, 280), parent)
        self.decCard2 = self.showCard(54, (170, 270), parent)
        self.cardx = self.showCard(54, (160, 260), parent)

        self.turnIndex = 1
        self.cardx.bind('<Button>', self.DistributeCards)

    def DistributeCards(self, event) -> None:
        '''Distribute Cards in the beginning'''
        if len(self.cardList) < 4:
            self.errorScreen('Not enough cards in the deck')
            return
        parent = self.frames[2]
        if self.turnIndex == 1:
            self.showCard(self.cardList[0], (530, 50), parent)
        if self.turnIndex == 2:
            self.showCard(54, (640, 50), parent)
        if self.turnIndex == 3:
            self.showCard(self.cardList[0], (530, 520), parent)
        if self.turnIndex == 4:
            self.showCard(self.cardList[0], (640, 520), parent)
        # self.turnIndex = self.turnIndex % 4
        self.turnIndex += 1
        self.cardList = self.cardList[1:]
    

    def run(self) -> None:
        '''Run the application'''
        self.root.mainloop()

if __name__ == '__main__':
    app = Application()
    