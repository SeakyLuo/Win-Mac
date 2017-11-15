from tkinter import *
root=Tk()
root.wm_title("Five In a Row")

def put(button):
    gi=button.grid_info()
    button.grid_forget()
    chess=Label(root,text='0')
    chess.grid(row=eval(gi['row']),column=eval(gi['column']))

for i in range(16):
    for j in range(16):
        if i==0:
            obj=Label(root,text=hex(j)[-1].upper())
        elif j==0:
            obj=Label(r oot,text=hex(i)[-1].upper())
        else:
            obj=Button(root)
            obj.configure(command=lambda button=obj: put(button))
        obj.grid(row=i,column=j)

restart=Button(root,text='Restart')
restart.grid(row=0,column=16)
cancel=Button(root,text='Cancel')
cancel.grid(row=1,column=16)
Quit=Button(root,text='Quit')
Quit.grid(row=2,column=16)
Message=Label(root,text='Message:\n\n\n')
Message.grid(row=16,column=0,columnspan=16,sticky=W)

root.mainloop()
