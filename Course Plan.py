from tkinter import *
import ez

root=Tk()
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
        self.weekday={'Mon':'m','Tue':'t','Wed':'w','Thu':'r','Fri':'f'}
        self.time=['{}:{}0'.format((i//2+7)%12+1,[0,3][i%2]) for i in range(24)]
        for i,date in enumerate(self.weekday):
            Label(self,text=date).grid(row=0,column=i+1)
        for i,time in enumerate(self.time):
            Label(self,text=time).grid(row=i+1,column=0)
        self.timeLabel=Label(self,text='Time:')
        self.timeLabel.grid(row=0,column=6)
        self.timeEntry=Entry(self)
        self.timeEntry.grid(row=0,column=7)
        self.nameLabel=Label(self,text='Name:')
        self.nameLabel.grid(row=1,column=6)
        self.nameEntry=Entry(self)
        self.nameEntry.grid(row=1,column=7)
        self.locLabel=Label(self,text='Location:')
        self.locLabel.grid(row=2,column=6)
        self.locEntry=Entry(self)
        self.locEntry.grid(row=2,column=7)
        self.addButton=Button(self,text='Add',command=self.add)
        self.addButton.grid(row=3,column=6)
        self.readButton=Button(self,text='Read',command=self.read)
        self.readButton.grid(row=3,column=7)
        self.saveButton=Button(self,text='Save',command=self.save)
        self.saveButton.grid(row=4,column=6)
        self.clearButton=Button(self,text='Clear',command=self.clear)
        self.clearButton.grid(row=4,column=7)
        self.read()

    def setup(self):
        self.courses=[]
        self.courseLabel={}
##        for i,date in enumerate(self.weekday):
##            for j,time in enumerate(self.time):
##                self.courseLabel[(date,time)]=Label(self)
##                self.courseLabel[(date,time)].grid(row=j+1,column=i+1)

    def add(self):
        time=self.timeEntry.get()
        name=self.nameEntry.get()
        loc=self.locEntry.get()
        if ez.have(self.courses).sub(time):
            return
##        self.courses.append((time,name,loc))
        weekindex=1
        while time[weekindex].isalpha():
            weekindex+=1
        stime=time[weekindex:]
        if stime.isnumeric():
            stime='{}:00-{}:50'.format(stime,stime)
        elif stime.count('-') and stime.count(':')<2:
            index=stime.find('-')
            start=stime[:index]
            if start.count(':')==0:
                start+=':00'
            end=stime[index:]
            if end.count(':')==0:
                end+=':00'
            stime=start+end
        start=stime[:stime.find('-')]
        for weekday in time[:weekindex]:
            ez.find(self.weekday).key()
                       
    def read(self):
        return
        self.setup()
        self.courses=ez.fread('course.txt')

    def save(self):
        return
        file=open('course.txt','w')
        file.write(repr(self.courses))
        file.close()

    def clear(self):
        self.setup()
        self.timeEntry.delete(0,END)
        self.nameEntry.delete(0,END)
        self.locEntry.delete(0,END)
        
cp=coursePlan(root)
cp.pack()
root.mainloop()

