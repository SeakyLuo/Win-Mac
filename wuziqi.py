from tkinter import *
root=Tk()
root.wm_title("Five in a row")
buttonlst=[ list(range(16)) for i in range(16)]

chess=Label(root,width=2,height=2,text='0')

def p(button):
    gi=button.grid_info()
    x=gi['row']
    y=gi['column']
    button.grid_forget()
    chess.grid(row=x,column=y)
    buttonlst[x][y]=chess
    
for i in range(16):
    for j in range(16):
        if i==0:
            obj=Label(root,width=2,text=hex(j)[-1].upper())
        elif j==0:
            obj=Label(root,width=2,text=hex(i)[-1].upper())
        else:
##            obj=Button(root,relief=FLAT,width=2,command=p(obj))
            obj=Button(root,relief=FLAT,width=2)
            obj.bindtags((i,j))
        obj.grid(row=i,column=j)
        buttonlst[i][j]=obj

root.mainloop()
