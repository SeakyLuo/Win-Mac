from tkinter import *
from ezs import npickm
inRange=lambda x,y,i,j:(not (x==i and y==j)) and (x==i or y==j or \
                ((x-1)//3==(i-1)//3 and (y-1)//3==(j-1)//3)) # 同宫
locRange=lambda x,y:[ (i,j) for i in range(1,10) for j in range(1,10) if inRange(x,y,i,j)]

class sudoku:
    def __init__(self,master):
        self.master=master
        self.setup()
        self.calculateButton=Button(self.master,text='计算',command=self.calculate)
        self.calculateButton.grid(row=9,column=0)
        self.hintButton=Button(self.master,text='提示',command=self.show_hints)
        self.hintButton.grid(row=9,column=1)
        self.cleanAll=Button(self.master,text='清除全部',command=self.setup)
        self.cleanAll.grid(row=9,column=2)
        self.saveButton=Button(self.master,text='保存',command=self.save)
        self.saveButton.grid(row=9,column=3)
        self.loadButton=Button(self.master,text='加载',command=self.load)
        self.loadButton.grid(row=9,column=4)
        self.isFull=lambda :all(number for (i,j),number in self.numbers.items())
        self.load()
        self.entry[(1,1)].focus()

    def setup(self):
        self.empty={(i,j):0 for i in range(1,10) for j in range(1,10)}
        self.hints={(i,j):list(range(1,10)) for i in range(1,10) for j in range(1,10)}
        self.numbers=self.empty.copy()
        self.entry=self.empty.copy()
        for i in range(1,10):
            for j in range(1,10):
                box=Entry(self.master)
                box.grid(row=i-1,column=j-1)
                box.bind('<KeyRelease>',self.switch)
                self.entry[(i,j)]=box
        self.showHints=False
        self.full=False

    def read(self):
        ## read numbers
        for i in range(1,10):
            for j in range(1,10):
                number=self.entry[(i,j)].get()
                if not number.isnumeric():
                    continue
                number=eval(number)
                if not 0<number<10:
                    raise Exception('Invalid number at ({},{})'.format(i,j))
                self.numbers[(i,j)]=number
                self.hints[(i,j)]=[number]
        if self.numbers==self.empty:
            raise Exception('Empty sudoku')
        self.full=self.isFull()

    def calculate(self):
        if self.full:
            return
        self.read()
        while True:
            before=self.numbers.copy()
            self.remove()
            self.solve()
            self.full=self.isFull()
            if before==self.numbers or self.full:
                break

    def removeHints(self,x,y,number):
        for i,j in locRange(x,y):
            if self.hints[(i,j)]==[number]:
                raise Exception('Duplicates at ({},{}) and ({},{})'.format(x,y,i,j))
            elif number in self.hints[(i,j)]:
                self.hints[(i,j)].remove(number)
                if len(self.hints[(i,j)])==1:
                    self.numbers[(i,j)]=self.hints[(i,j)][0]
                    self.entry[(i,j)].insert(0,self.hints[(i,j)][0])

    def remove(self):
        while True:
            before=self.numbers.copy()
            for (i,j),number in self.numbers.items():
                if number:
                    self.removeHints(i,j,number)
            self.full=self.isFull()
            if before==self.numbers or self.full:
                break

    def solve(self):
        hintsRow=lambda x,y:[ hint for k in range(1,10) if k!=y and self.numbers[(x,k)]==0 for hint in self.hints[(x,k)] ]
        hintsCol=lambda x,y:[ hint for k in range(1,10) if k!=x and self.numbers[(k,y)]==0 for hint in self.hints[(k,y)] ]
        hintsBlk=lambda x,y:[ hint for i in range((x-1)//3*3+1,(x-1)//3*3+4) for j in range((y-1)//3*3+1,(y-1)//3*3+4) if (x,y)!=(i,j) and self.numbers[(i,j)]==0 for hint in self.hints[(i,j)] ]
        ## normal solve
        for number in range(1,10):
            for i,j in self.hints:
                if self.numbers[(i,j)] or number not in self.hints[(i,j)]:
                    continue
                if any(number not in set(lst) for lst in [hintsRow(i,j),hintsCol(i,j),hintsBlk(i,j)]):
                    self.numbers[(i,j)]=number
                    self.hints[(i,j)]=[number]
                    self.entry[(i,j)].insert(0,number)
                    self.removeHints(i,j,number)
        ## number pair:
        while True:
            before=self.numbers.copy()
            for i,j in self.numbers:
                if self.numbers[(i,j)]:
                    continue
                for pair in npickm(self.hints[(i,j)],2):
                    pair=list(pair)
                    rangedict={'r':hintsRow(i,j),'c':hintsCol(i,j),'b':hintsBlk(i,j)}
                    locdict={'r':[ (i,k) for k in range(1,10) if pair[0] in self.hints[(i,k)] and pair[1] in self.hints[(i,k)]],\
                             'c':[ (k,j) for k in range(1,10) if pair[0] in self.hints[(k,j)] and pair[1] in self.hints[(k,j)]],\
                             'b':[ (x,y) for x in range((i-1)//3*3+1,(i-1)//3*3+4) for y in range((j-1)//3*3+1,(j-1)//3*3+4) if pair[0] in self.hints[(x,y)] and pair[1] in self.hints[(x,y)]]}
                    for typ in rangedict:
                        hintsRange=rangedict[typ]
                        if hintsRange.count(pair[0])==hintsRange.count(pair[1])==1:
                            loc=locdict[typ]
                            if len(loc)==2:
                                for k in range(2):
                                    self.hints[loc[k]]=[ item for item in pair]##pair.copy()
                                self.remove()
            self.full=self.isFull()
            if before==self.numbers or self.full:
                break

    def show_hints(self):
        if self.showHints:
            self.showHints=False
            for i in range(1,10):
                for j in range(1,10):
                    if self.numbers[(i,j)]==0:
                        self.entry[(i,j)].delete(0,END)
        else:
            self.showHints=True
            for i in range(1,10):
                for j in range(1,10):
                    if self.numbers[(i,j)]==0:
                        text=','.join(str(number) for number in self.hints[(i,j)])
                        self.entry[(i,j)].insert(0,text)

    def save(self):
        file=open('C:\\Users\Seaky\\AppData\\Local\\Programs\\Python\\Python36\\Python Files\\sudoku\\puzzle.txt','w')
        self.numbers=self.empty.copy()
        self.read()
        file.write(repr(self.numbers))
        file.close()

    def load(self):
        self.setup()
        file=open('C:\\Users\Seaky\\AppData\\Local\\Programs\\Python\\Python36\\Python Files\\sudoku\\puzzle.txt')
        self.numbers=eval(file.read())
        file.close()
        for loc in self.numbers:
            number=self.numbers[loc]
            if number:
                self.entry[loc].insert(0,number)
                self.numbers[loc]=number
                self.hints[loc]=[number]

    def switch(self,event):
        key=event.keysym
        move={'Up':(-1,0),'Down':(1,0),'Left':(0,-1),'Right':(0,1)}
        if key not in move:
            return
        x,y=move[key]
        info=event.widget.grid_info()
        r=info['row']+1+x
        c=info['column']+1+y
        if r in [0,10] or c in [0,10]:
            return
        self.entry[(r,c)].focus()

root=Tk()
s=sudoku(root)
root.wm_title("sudoku solver")
root.mainloop()
