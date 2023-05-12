from tkinter import *
def help():
    inter = Tk()
    inter.geometry("1080x720")
    text1 = Label(inter,text="CHINESE CHECKERS GAME",fg='#F1C40F',font=("verdana",30))
    text2 = Label(inter,text="Game Rules :",fg='#515A5A',font=("verdana",25))
    text3 = Label(inter,text= "The goal of the game is to move all of his pawns to the opposite area of his starting area. The winner is the first player \nto have brought all of his pawns to opposite zone ."
                             " Each player has 10 pawns of the same color placed at the beginning\n of his starting point."
                             " Each player is only allowed to move one pawn per turn of play.There are 2 possibilities of movement: \n-Move a pawn from one frame to any direction\n -Move a pawn by successive jumps.\nIt is forbidden to have your pawns parked in a point that is neither its starting area nor its arrival area \n(but you can move there).",font=("arial",15))
    image = PhotoImage(file="help.png").zoom(20).subsample(35)
    canvas = Canvas(inter,width=1080,height=400)
    canvas.create_image(500,200,image=image)
    canvas.place(x=0,y=300)
    text1.pack()
    text2.pack()
    text3.pack()
    inter.mainloop()
