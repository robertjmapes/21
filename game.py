from tkinter import *
import random, time, os, sys

class Menu:
    def __init__(self, master):

        self.master = master
        self.menu()

    def menu(self):

        self.logoimg = PhotoImage(file="images/logo.png")

        self.master.geometry("400x450")
        self.master.resizable(False, False)

        self.title = Label(self.master, text="Blackjack", width = 25, font = ("Courier", 45))
        self.start = Button(self.master, text = 'Start', width = 25, command = self.start, bg="green", font = ("Courier", 14))
        self.quit = Button(self.master, text = 'Quit', width = 25, command = self.kill, bg="red", font = ("Courier", 14))
        self.logo = Label(self.master, image=self.logoimg)

        self.title.pack()
        self.start.pack()
        self.quit.pack()
        self.logo.pack()

    def kill(self):
        self.master.destroy()
        sys.exit(0)

    def start(self):
        self.newWindow = Toplevel(self.master)
        self.app = Game(self.newWindow)

class Cards:
    def __init__(self, master):
        self.master = master

    def createCards(self):
        self.cards = []
        for i in range(0,14):
            if i == 1:
                self.cards.append(["a","s"])
                self.cards.append(["a","c"])
                self.cards.append(["a","h"])
                self.cards.append(["a","d"])
            if i == 13:
                self.cards.append(["q","s"])
                self.cards.append(["q","c"])
                self.cards.append(["q","h"])
                self.cards.append(["q","d"])
            if i == 12:
                self.cards.append(["k","s"])
                self.cards.append(["k","c"])
                self.cards.append(["k","h"])
                self.cards.append(["k","d"])
            if i == 11:
                self.cards.append(["j","s"])
                self.cards.append(["j","c"])
                self.cards.append(["j","h"])
                self.cards.append(["j","d"])
            elif i > 1 and i < 11:
                self.cards.append([str(i), "s"])
                self.cards.append([str(i),"c"])
                self.cards.append([str(i),"h"])
                self.cards.append([str(i),"d"])
        random.shuffle(self.cards)
        return self.cards

    def dealCards(self):

        self.cardimages = []
        self.playerCards = []
        self.computerCards = []

        cards_to_remove = []
        for i in range(0,2):

            # Appends a card from a cards array I have made earlier and shuffled, each card looks like this ['5', 's']
            self.playerCards.append(self.cards[i])
            self.computerCards.append(self.cards[i+2])

            a = "".join(self.playerCards[i])
            b = "".join(self.computerCards[i])

            # I have a collection of cards labbelled QD, AS... etc // 150x170
            self.cardUser = PhotoImage(file=f"images/cards/{a.upper()}.png")
            self.cardComputer = PhotoImage(file=f"images/cards/{b.upper()}.png")
            self.purpleBack = PhotoImage(file=f"images/cards/purple_back.png")

            #We need persistant objects for images used in Label
            if self.cardUser not in self.cardimages:
                self.cardimages.append(self.cardUser)
            if self.cardComputer not in self.cardimages:
                self.cardimages.append(self.cardComputer)
            if self.purpleBack not in self.cardimages:
                self.cardimages.append(self.purpleBack)


            self.cardUser = Label(self.master, image=self.cardUser, bg="green")
            self.cardUser.grid(row=3,column=i)

            self.cardComputer = Label(self.master, image=self.cardComputer, bg="green")
            self.cardComputer.grid(row=2,column=1)

            self.blankCard = Label(self.master, image=self.purpleBack, bg="green")
            self.blankCard.grid(row=2,column=0)

            cards_to_remove.append(self.cards[i])
            cards_to_remove.append(self.cards[i+2])

        print(f"CARD IMAGES STORED IN MEMORY:\n\n {self.cardimages}\n")
        print(f"COMPUTER CARDS: {self.computerCards}\n")
        print(f"PLAYER CARDS: {self.playerCards}\n")
        print(f"CARDS:\n {self.cards}")

        for card in cards_to_remove:
            self.cards.remove(card)

    def sumCards(self):

        x = 0
        for i in self.playerCards:
            if i[0] == "a":
                x += 1
            if i[0] == "q":
                x += 10
            if i[0] == "k":
                x += 10
            if i[0] == "j":
                x += 10
            elif i[0] in ["1","2","3","4","5","6","7","8","9","10"]:
                x += int(i[0])

        self.sumPlayer = x

        if self.sumPlayer <= 11:
            for i in self.playerCards:
                if "a" == i[0]:
                    self.sumPlayer = self.sumPlayer + 10
                    break

        print(f"\nSUM OF PLAYERS CARD: {self.sumPlayer}\n")

        self.labelSum = Label(self.master,text=f"Total: {self.sumPlayer}", width = 20, font = ("Courier", 14), bg="green" )
        self.labelSum.grid(row=1,column=3)

        return self.sumPlayer

    def sumComputer(self):
        x = 0
        for i in self.computerCards:
            if i[0] == "a":
                x += 1
            if i[0] == "q":
                x += 10
            if i[0] == "k":
                x += 10
            if i[0] == "j":
                x += 10
            elif i[0] in ["1","2","3","4","5","6","7","8","9","10"]:
                x += int(i[0])

        self.sumComputerCards = x

        if self.sumComputerCards <= 11:
            for i in self.computerCards:
                if "a" == i[0]:
                    self.sumComputerCards = self.sumComputerCards + 10
                    break

        print(f"\nSUM OF COMPUTERS CARD: {self.sumComputerCards}\n")

        return self.sumComputerCards



class Game:

    def __init__(self, master):

        self.master = master
        self.money = 0
        self.mainWindow()

    def mainWindow(self):

        self.master.geometry("1000x700")
        self.master.configure(background="green")

        self.hitButton = Button(self.master, text= "Hit me!", width = 15, command = lambda : self.hit(), bg="lightblue", font = ("Courier", 14) )
        self.hitButton.grid(row=1,column=0)

        self.stickButton = Button(self.master, text= "Stick!", width = 15, command = lambda: self.stick(), bg="orange", font = ("Courier", 14) )
        self.stickButton.grid(row=1,column=1)

        self.stickButton.config(state="normal")
        self.hitButton.config(state="normal")

        # Creates, Deals, Sums and Displays Cards
        Cards.createCards(self)
        Cards.dealCards(self)
        Cards.sumCards(self)

    def increasebet(self):
        self.money += 10

    def hit(self):

        if len(self.cards) == 6:
            self.master.destroy()

        print(f"CARDS LEFT: {self.cards}\n")


        self.playerCards.append(self.cards[0])
        a = "".join(self.cards[0])
        self.cards.remove(self.cards[0])

        self.cardUser = PhotoImage(file=f"images/cards/{a.upper()}.png")

        #We need persistant objects for images used in Label
        if self.cardUser not in self.cardimages:
            self.cardimages.append(self.cardUser)

        self.cardUser = Label(self.master, image=self.cardUser, bg="green")
        self.cardUser.grid(row=3,column=len(self.playerCards))

        print(f"PLAYERS NEW SET: {self.playerCards}")

        self.sumPlayer = Cards.sumCards(self)

        if self.sumPlayer > 21:

            self.labelSum = Label(self.master,text=f"Total: {self.sumPlayer}", fg="red",width = 20, font = ("Courier", 14) )
            self.labelSum.grid(row=1,column=3)
            self.stick()
            #loser label

            #self.master.after(1000, lambda:[Cards.dealCards(self), Cards.sumCards(self)])

        if len(self.playerCards) == 5:
            pass

    def stick(self):

        self.stickButton.config(state="disabled")
        self.hitButton.config(state="disabled")

        if len(self.cards) == 6:
            print(f"\n\nLIMIT REACHED!")
            self.master.destroy()

        v = "".join(self.computerCards[0])

        self.cardCompR = PhotoImage(file=f"images/cards/{v.upper()}.png")

        if self.cardCompR not in self.cardimages:
            self.cardimages.append(self.cardCompR)

        self.cardCompR = Label(self.master, image=self.cardCompR, bg="green")
        self.cardCompR.grid(row=2,column=0)

        print(f"CARDS LEFT: {self.cards}\n")

        self.sumComputerCards = Cards.sumComputer(self)
        self.sumPlayer = Cards.sumCards(self)

        if self.sumPlayer > 21:
            self.loseLabel = Label(self.master, text = "Banker wins!", fg="black", width = 20, font = ("Courier",14),  bg="red")
            self.loseLabel.grid(row=1,column=4)
            self.master.after(3000, lambda:[Cards.dealCards(self),self.loseLabel.destroy(), Cards.sumCards(self), self.resetButtons()])

        else:

            while self.sumComputerCards <= self.sumPlayer:

                self.computerCards.append(self.cards[0])
                a = "".join(self.cards[0])
                self.cards.remove(self.cards[0])

                self.cardComp = PhotoImage(file=f"images/cards/{a}.png")

                #We need persistant objects for images used in Label
                if self.cardComp not in self.cardimages:
                    self.cardimages.append(self.cardComp)

                self.cardComp = Label(self.master, image=self.cardComp, bg="green")
                self.cardComp.grid(row=2,column=len(self.computerCards))

                print(f"COMPUTER NEW SET: {self.computerCards}")
                self.sumComputerCards = Cards.sumComputer(self)

            if self.sumComputerCards >= self.sumPlayer and self.sumComputerCards < 21:
                self.loseLabel = Label(self.master, text = "Banker wins!", fg="black", width = 20, font = ("Courier",14),  bg="red")
                self.loseLabel.grid(row=1,column=4)
                self.master.after(3000, lambda: [Cards.dealCards(self), Cards.sumCards(self), self.loseLabel.destroy(), self.resetButtons()])

            if self.sumComputerCards > 21:
                self.winLabel = Label(self.master, text="Player wins!", fg="black",width = 20, font = ("Courier", 14),  bg="yellow" )
                self.winLabel.grid(row=1,column=4)
                self.master.after(3000, lambda: [Cards.dealCards(self),Cards.sumCards(self),self.winLabel.destroy(), self.resetButtons()])


            if self.sumComputerCards == 21:
                self.loseLabel = Label(self.master, text = "Banker wins!", width = 20, font = ("Courier",14),  bg="red", fg="black")
                self.loseLabel.grid(row=1,column=4)
                self.master.after(3000, lambda: [Cards.dealCards(self), Cards.sumCards(self), self.loseLabel.destroy(), self.resetButtons()])

    def resetButtons(self):
        self.hitButton.config(state="normal")
        self.stickButton.config(state="normal")

def main():
    root = Tk()
    app = Menu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
