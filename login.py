from tkinter import *
import encryption
import dna
import cv2
class login():
    def __init__(self, root):
        self.path=''
        self.f = Frame(root, width=600, height=400, cursor='cross', bg='silver')
        self.f.propagate(0)
        self.f.pack()
        user = Label(root, text="Distort value -", )
        user.place(x=50, y=20)

        self.Username =Entry(self.f,width=35)
        self.Username.place(x=150, y=20, width=100)

        passw = Label(root, text="key -")
        passw.place(x=50, y=50)

        self.password = Entry(self.f,show='*',width=35)
        self.password.place(x=150, y=50, width=100)

        button = Button(root, text="scramble",
                              bg='blue', command=self.login)
        button.place(x=150, y=75, width=85)
        button = Button(root, text="DNA encrypt",
                        bg='blue', command=self.encrypt)
        button.place(x=150, y=100, width=85)
    def login(self):
        User=int(self.Username.get())
        Pass=self.password.get()
        self.path=encryption.main(User)
    def encrypt(self):
        pass1 = self.password.get()
        key=""
        for i in pass1:
            key=key+str(ord(i))
        key=hex(int(key))
        dna.encode(key,self.path)

root=Tk()
m=login(root)
root.mainloop()
