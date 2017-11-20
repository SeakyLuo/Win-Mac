from tkinter import *


def in_range(x1,y1,x2,y2):
        return (not (x1==x2 and y1==y2)) and (x1==x2 or y1==y2 or \
                (x1//3==x2//3 and y1//3==y2//3)) # in square

class sudoku(Frame):
    def __init__(self,parent):
        self.parent=parent
        self.entrylst=[ list(range(9)) for i in range(9)]
        self.hintlst=[ [list(range(1,10)) for j in range(9) ] for i in range(9)]
        self.numlst=[ [0 for j in range(9) ] for i in range(9) ]
        for i in range(9):
            for j in range(9):
                box=Entry(root)
                box.grid(row=i,column=j)
                self.entrylst[i][j]=box
        self.calculateb=Button(root,width=5,text='计算',command=self.calculate)
        self.calculateb.grid(row=9,column=0)
        self.hintb=Button(root,width=5,text='提示',command=self.show_hints)
        self.hintb.grid(row=9,column=1)
        self.hints=False
        self.cleanhintb=Button(root,width=5,text='清除提示',command=self.clean_hints)
        self.cleanhintb.grid(row=9,column=2)
        self.cleanhintb=Button(root,width=5,text='清除全部',command=self.reset)
        self.cleanhintb.grid(row=9,column=3)
        self.quitb=Button(root,width=5,text='关闭',command=self.parent.destroy)
        self.quitb.grid(row=9,column=4)

    def reset(self):
        self.entrylst=[ list(range(9)) for i in range(9)]
        self.hintlst=[ [list(range(1,10)) for j in range(9) ] for i in range(9)]
        self.numlst=[ [0 for j in range(9) ] for i in range(9) ]
        for i in range(9):
            for j in range(9):
                box=Entry(root)
                box.grid(row=i,column=j)
                self.entrylst[i][j]=box
        self.hints=False

    def set_numbers(self):
        for i in range(9):
            for j in range(9):
                try:
                    num=eval(self.entrylst[i][j].get())
                    if not 0<num<10:
                        raise Exception('Invalid number at ({},{})'.format(i,j))
                    self.numlst[i][j]=num
                    self.hintlst[i][j]=[num]
                except SyntaxError:
                    pass

    def calculate(self):
        self.set_numbers()
        self.check()
        self.solve()
        self.show_answer()

    def check(self):
        for i in range(9):
            for j in range(9):
                num=self.numlst[i][j]
                if num:
                    for x in range(9):
                        for y in range(9):
                            if in_range(i,j,x,y):
                                if len(self.hintlst[x][y])==1:
                                    if self.hintlst[x][y][0]==num:
                                        raise Exception('Duplicates at ({},{}) and ({},{})'.format(i,j,x,y))
                                else:
                                    try:
                                        self.hintlst[x][y].remove(num)
                                        if len(self.hintlst[x][y])==1:
                                            self.numlst[x][y]=self.hintlst[x][y][0]
                                    except ValueError:
                                        pass
    def solve(self):
        def row():
            pass
        def col():
            pass
        def blk():
            pass
        row()
        col()
        blk()

    def show_answer(self):
        for i in range(9):
            for j in range(9):
                num=self.numlst[i][j]
                if num and self.entrylst[i][j].get()=='':
                    self.entrylst[i][j].insert(0,num)

    def show_hints(self):
        if not self.hints:
            self.hints=True
            for i in range(9):
                for j in range(9):
                    if self.numlst[i][j]==0:
                        text=','.join(str(num) for num in self.hintlst[i][j])
                        self.entrylst[i][j].insert(0,text)

    def clean_hints(self):
        if self.hints:
            self.hints=False
            for i in range(9):
                for j in range(9):
                    if self.numlst[i][j]==0:
                        self.entrylst[i][j].delete(0,END)

root = Tk()
s=sudoku(root)
root.wm_title("sudoku solver")
root.mainloop()
