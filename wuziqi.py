from tkinter import *
from random import choice

root=Tk()
##先后手
class FIR(Frame):
    def __init__(self,parent,player='0',pc='*'):
        Frame.__init__(self,parent)
        self.parent=parent
        self.player=player
        self.pc=pc
        for i in range(16):
            r=Label(self.parent,width=2,text=hex(i)[-1].upper())
            r.grid(row=0,column=i)
            c=Label(self.parent,width=2,text=hex(i)[-1].upper())
            c.grid(row=i,column=0)
        self.restart=Button(self.parent,text='Restart',command=self.setup)
        self.restart.grid(row=0,column=16)
        self.cancel=Button(self.parent,text='Cancel',command=self.cancel)
        self.cancel.grid(row=1,column=16)
        self.Quit=Button(self.parent,text='Quit',command=self.parent.destroy)
        self.Quit.grid(row=2,column=16)

        self.setup()
        self.sendmsg('游戏开始啦~你是{}，电脑是{}'.format(self.player,self.pc))

    def setup(self):
        self.objlst=[list(range(16)) for i in range(16) ]
        for i in range(1,16):
            for j in range(1,16):
                obj=Button(self.parent,width=2)
                obj.configure(command=lambda button=obj: self.put(button))
                obj.grid(row=i,column=j)
                self.objlst[i][j]=obj
        self.grid=[['_' ]*15 for i in range(15)]
        self.moves=[]
        self.jam=[]
        self.line=[]
        self.msg=Label(self.parent)
        self.msg.grid(row=16,column=0,columnspan=17,sticky=W)

    def restart(self):
        self.msg.grid_remove()
        self.setup()

    def sendmsg(self,message):
        textlst=self.msg['text'].split('\n')
        if len(textlst)==5:
            textlst.pop(1)
        textlst.append(message)
        self.msg=Label(self.parent,text='\n'.join(textlst))
        self.msg.grid(row=16,column=0,columnspan=17,sticky=W)

    def put(self,button):
        gi=button.grid_info()
        r=gi['row']
        c=gi['column']
        button.grid_forget()
        Label(self.parent,text=self.player).grid(row=r,column=c)
        self.moves.append((c,r))
        self.grid[c-1][r-1]=self.player
        self.respond()

    def cancel(self):
        for i in range(2):
            x,y=self.moves.pop()
            self.grid[x][y]='_'
            self.objlst[x][y].grid_forget()
            b=Button(self.parent,width=2)
            b.configure(command=lambda button=b: self.put(button))
            b.grid(row=x,column=y)
        self.sendmsg('怎么可以悔棋呐')

    def respond(self):
        num_player=self.check(self.player,self.pc)
        if num_player==5:
            self.sendmsg('恭喜哦赢了我这个笨笨的AI~~~')
            i=input("想要再虐我嘛⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄？按Enter键表示同意，输入任意字符表示拒绝哦~\n>>>")
            if i=='':
                self.__init__()
            return
        num_computer=self.check(self.pc,self.player)
        x=y=0
        if num_computer>num_player and num_computer in [3,4]:
            x,y=choice(self.line)
        elif num_computer<num_player and num_player in [3,4]:
            x,y=choice(self.jam)
        elif num_computer==num_player and num_computer in [3,4]:
            x,y=choice(self.jam+self.line)
        else:
            x,y=self.taolu()
        self.jam=[]
        self.line=[]
        self.grid[x][y]=self.pc
        self.objlst[x][y].grid_forget()
        Label(self.parent,text=self.pc).grid(row=x,column=y)
        self.moves.append((x,y))
        self.sendmsg('轮到电脑啦↓\n电脑把棋放在了'+str((y,x)))
        num_computer=self.check(self.pc,self.player)
        if num_computer==5:
            self.printBoard()
            self.sendmsg('辣鸡连人家这么笨的AI都会输吗？？？')
            i=input("不服想要再挑战一次嘛？按Enter键表示同意，输入任意字符表示拒绝哦~\n>>>")
            if i=='':
                self.__init__()
            return
        elif len(self.moves)==256:
            self.sendmsg("棋盘满啦，游戏平局.")
            return
        self.sendmsg('轮到你啦↓')

    def check(self,player='0',pc='*'):
        max_lst=[]
        line_dict={'row':(1,0),'col':(0,1),'lower_right':(1,1),'upper_right':(1,-1)}
        lst={'0':self.jam,'*':self.line}[player]
        for line in ['row','col','lower_right','upper_right']:
            x,y=line_dict[line]
            max_chess=1
            for x0,y0 in self.moves:
                if self.grid[x0][y0]==player:
                    potential=[(x0+i*x,y0+i*y) for i in range(1,5) if 0<=x0+i*x<15 and 0<=y0+i*y<15]
                    condition=''.join([self.grid[x0+i*x][y0+i*y] for i in range(1,5) if 0<=x0+i*x<15 and 0<=y0+i*y<15])
                    acc=1
                    if condition==player*4:
                        return 5
                    elif condition.count(player)==3:
                        if condition==player*3+pc and 0<=x0-x<15 and 0<=y0-y<15 and self.grid[x0-x][y0-y]=='':
                            lst.append((x0-x,y0-y))
                            acc=4
                        elif pc not in condition:
                            if condition[:3]==player*3:
                                if 0<=x0-x<15 and 0<=y0-y<15 and self.grid[x0-x][y0-y]=='_':
                                    lst.append((x0-x,y0-y))
                                if 0<=x0+4*x<15 and 0<=y0+4*y<15 and self.grid[x0+4*x][y0+4*y]=='_':
                                    lst.append((x0+4*x,y0+4*y))
                            else:
                                idx=condition.find('_')+1
                                lst.append((x0+idx*x,y0+idx*y))
                            acc=4
                    elif condition[:3].count(player)==2 and pc not in condition[:3]:
                        idx=condition[:3].find('_')+1
                        lst.append((x0+idx*x,y0+idx*y))
                        if 0<=x0-x<15 and 0<=y0-y<15 and self.grid[x0-x][y0-y]==pc:
                            continue
                        elif 0<=x0-x<15 and 0<=y0-y<15 and self.grid[x0-x][y0-y]=='_':
                            if max_chess<4:
                                lst.append((x0-x,y0-y))
                        if idx!=3 and 0<=x0+4*x<15 and 0<=y0+4*y<15 and self.grid[x0+4*x][y0+4*y]=='_':
                            if max_chess<4:
                                lst.append((x0+4*x,y0+4*y))
                        acc=3
                    if acc>max_chess:
                        max_chess=acc
            max_lst.append(max_chess)
        return max(max_lst)

    def taolu(self):
        x0,y0=self.moves[-1]
        i=1
        hoop=[ (x0+num1,y0+num2) for num1 in range(-i,i+1) for num2 in range(-i,i+1)
               if 0<=x0+num1<=15 and 0<=y0+num2<=15 and self.grid[x0+num1][y0+num2]=='_' ]
        while hoop==[]:
            i+=1
            hoop=[ (x0+num1,y0+num2) for num1 in range(-i,i+1) for num2 in range(-i,i+1)
               if 0<=x0+num1<=15 and 0<=y0+num2<=15 and self.grid[x0+num1][y0+num2]=='_' ]
        return choice(hoop)

fir=FIR(root)
fir.master.title("Five In a Row")
root.mainloop()
