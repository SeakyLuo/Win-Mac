from tkinter import *

root=Tk()

def multiple(l1,l2):
    '''Check whether l1 is the multiple of l2'''
    if l1==l2:
        return True
    length1=len(l1)
    length2=len(l2)
    if length1%length2!=0:
        return False
    for i in range(0,length1,length2):
        if l1[i:i+length2]!=l2:
            return False
    return True

def overlap(time1,time2):
    if time1==time2:
        return True
    t111=eval(time1[:time1.find(':')])
    t211=eval(time2[:time2.find(':')])
    if t111+[0,12][t111<8]>t211+[0,12][t211<8]:
        time1,time2=time2,time1
    t11,t12=time1.split('-')
    t21,t22=time2.split('-')
    if t11==t21 or t12==t22:
        return True
    t111,t112=t11.split(':')
    t111=eval(t111)
    t111+=[0,12][t111<8]
    t112=eval(t112)
    t121,t122=t12.split(':')
    t121=eval(t121)
    t121+=[0,12][t121<8]
    t122=eval(t122)

    t211,t212=t21.split(':')
    t211=eval(t211)
    t211+=[0,12][t211<8]
    t212=eval(t212)
    t221,t222=t22.split(':')
    t221=eval(t221)
    t221+=[0,12][t221<8]
    t222=eval(t222)
    if t111>t221 or \
       (t111==t221 and t112>t222) or \
       t121<t211 or \
       (t121==t211 and t122<t212):
        return False
    return True

class coursePlan(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.weekday=['Mon','Tue','Wed','Thu','Fri']
        self.time=[(i+7)%12+1 for i in range(12)]
        for i,date in enumerate(self.weekday):
            Label(self,text=date).grid(row=0,column=i+1)
        for i,time in enumerate(self.time):
            Label(self,text=time).grid(row=i+1,column=0)
        self.setup()

    def setup(self):
        self.course=[]
        self.courseLabel={(i,j):0 for i in range(1,6) for j in range(1,13)}
        for i in range(1,13):
            for j in range(1,6):
                self.courseLabel[(i,j)]=Label(self)
                self.courseLabel[(i,j)].grid(row=i,column=j)

cp=coursePlan(root)
cp.pack()
root.mainloop()

