from tkinter import *
 #TODO: only buttons work in my current version of tk/tc
 #TODO: can't change the button data without refreshing somehow
 #TODO: decouple burnstack controller print methods and instead modify a model we can view here
class View:
    hand = ['🂠', '🂠', '🂠', '🂠', '🂠']
    stack = 6
    bet_title = "Bet: " + str(stack) + " card(s) left"
    burn_title = "Burn: " + str(stack) + " card(s) left"

    def __init__(self):
        self.root = Tk()
        self.root.geometry("900x500")
        self.bet_button = Button(self.root, text=self.bet_title)
        self.bet_button.pack()
        self.burn_button = Button(self.root, text=self.burn_title)
        self.burn_button.bind("Bet", self.burn)
        self.burn_button.pack()
        self.swap_button = Button(self.root, text="Pass")
        self.swap_button.pack()
        for i in self.hand:
            Button(self.root, text=i, font=("Helvetica", 40), height=1, width=2).pack()

    def burn(self):
        self.hand.append('🂠')
        self.stack -= 1
        Button(self.root, text='🂠', font=("Helvetica", 40), height=1, width=2).pack()
        self.bet_button.config(text=self.bet_title)
        self.burn_button.config(text=self.burn_title)

    def start(self):
        self.root.mainloop()



if __name__ == "__main__":
    view = View()
    view.start()

