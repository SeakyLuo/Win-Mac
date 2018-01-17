from tkinter import *
from tkinter import messagebox
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

def length(t1,t2):
    '''Time format 12:30'''
    i1=t1.index(':')
    h1=eval(t1[:i1])
    if h1<8:
        h1+=12
    time1=h1*60+eval(t1[i1+1:])
    i2=t2.index(':')
    h2=eval(t2[:i2])
    if h2<8:
        h2+=12
    time2=h2*60+eval(t2[i2+1:])
    return abs(time2-time1)

class coursePlan(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.weekday={'Mon':'m','Tue':'t','Wed':'w','Thu':'r','Fri':'f'}
        self.time=['{}:{}0'.format((i//2+7)%12+1,[0,3][i%2]) for i in range(24)]
        for i,date in enumerate(self.weekday):
            Label(self,text=date).grid(row=0,column=i+1)  ##needs bg
        for i,time in enumerate(self.time):
            Label(self,text=time).grid(row=i+1,column=0)  ##needs bg
        self.timeLabel=Label(self,text='Time:')
        self.timeBox=Entry(self)
        self.exampleText='Example: tr12-1:15'
        self.timeBox.bind('<FocusIn>',self.focusIn)
        self.timeBox.bind('<FocusOut>',self.focusOut)
        self.focusOut('<FocusOut>')
        self.nameLabel=Label(self,text='Name:')
        self.nameBox=Entry(self)
        self.locLabel=Label(self,text='Location:')
        self.locBox=Entry(self)
        self.boxList=[self.timeBox,self.nameBox,self.locBox]
        for i,(box,label) in enumerate(zip(self.boxList,[self.timeLabel,self.nameLabel,self.locLabel])):
            label.grid(row=i,column=6)
            box.grid(row=i,column=7,columnspan=2)
            box.bind('<KeyRelease>',self.switch)
        self.addButton=Button(self,text='Add',command=self.add)
        self.addButton.grid(row=3,column=6)
        self.readButton=Button(self,text='Read',command=self.read)
        self.readButton.grid(row=3,column=7)
        self.colorButton=Button(self,text='Color',command=self.switchColor)
        self.colorButton.grid(row=3,column=8)
        self.saveButton=Button(self,text='Save',command=self.save)
        self.saveButton.grid(row=4,column=6)
        self.clearButton=Button(self,text='Clear',command=self.clear)
        self.clearButton.grid(row=4,column=7)
        self.courseListLabel=Label(self,text='Course List')
        self.courseListLabel.grid(row=5,column=6)
        self.read()

    def setup(self):
        self.courses=[]
        self.courseLabels=[]
        self.courseList=[]
        self.colorList=['white','pink','orange','yellow','light green','cyan','azure','violet','magenta']
        self.nameBox.focus()

    def putLabel(self,datetime,name,loc,mode=0):
        datetime=datetime.lower()
        courseLabel=Label(self,text=name+[' --- ',''][loc==None]+loc)
        index=-1
        if mode==0:
            rowNum=len(self.courseList)+6
            courseLabel.grid(row=rowNum,column=6)
            modifyButton=Button(self,text='Modify')
            modifyButton.grid(row=rowNum,column=7)
            modifyButton.configure(command=lambda button=modifyButton:self.modify(button))
            dropButton=Button(self,text='Drop',command=self.drop)
            dropButton.grid(row=rowNum,column=8)
            dropButton.configure(command=lambda button=dropButton:self.drop(button))
            self.courseList.append((courseLabel,modifyButton,dropButton))
            self.courses.append((datetime,name,loc))
            self.courseLabels.append([])
        else:
            index=self.courses.index(mode)
            self.courseList[index][0].grid_forget()
            courseLabel.grid(row=index+6,column=6)
            self.courses[index]=(datetime,name,loc)
            for label in self.courseLabels[index]:
                label.grid_forget()
            self.courseLabels[index]=[]

        weekindex=1
        while datetime[weekindex].isalpha():
            weekindex+=1
        time=datetime[weekindex:]
        if time.isnumeric():
            time='{}:00-{}:50'.format(time,time)
        elif time.count('-') and time.count(':')<2:
            dash=time.find('-')
            start=time[:dash]
            if start.count(':')==0:
                start+=':00'
            end=time[dash:]
            if end.count(':')==0:
                end+=':00'
            time=start+end
        dash=time.find('-')
        start=time[:dash]
        end=time[dash+1:]
        grids=length(start,end)//30+1
        for weekday in datetime[:weekindex]:
            day=ez.find(self.weekday).key(weekday)[0]
            beginRow=self.time.index(start)+1
            col=list(self.weekday.keys()).index(day)+1
            maxlen=max(len(name),len(loc))
            courseInfo=[('{:'+str(maxlen)+'}').format(name),('{:'+str(maxlen)+'}').format(loc)]+[' '*maxlen for i in range(grids-2)]
            for i in range(grids):
                label=Label(self,text=courseInfo[i],bg=self.colorList[0])
                self.courseLabels[index].append(label) 
                label.grid(row=beginRow+i,column=col)

    def add(self,mode=0):
        datetime=self.timeBox.get()
        name=self.nameBox.get()
        loc=self.locBox.get()
        if datetime in ('',self.exampleText) or (datetime,name,loc) in self.courses:
            return
        if name=='':
            messagebox.showinfo('Error','Please input course name!')
            return
        self.putLabel(datetime,name,loc,mode)
        self.clearBox()

    def read(self):
        self.setup()
        self.clearBox()
        content={}
        try:
            content=ez.fread('settings.txt')
        except FileNotFoundError:
            ez.fwrite('settings.txt',content)
        if content=={}:
            return
        index=self.colorList.index(content['color'])
        self.colorList=self.colorList[index:]+self.colorList[:index]
        for datetime,name,loc in content['courses']:
            self.putLabel(datetime,name,loc)
        
    def save(self):
        content={'courses':self.courses,'color':self.colorList[0]}
        ez.fwrite('settings.txt',content)

    def clear(self):
        for abel in self.courseLabels:
            label.grid_forget()
        for courseLabel,modifyButton,dropButton in self.courseList:
            courseLabel.grid_forget()
            modifyButton.grid_forget()
            dropButton.grid_forget()
        self.clearBox()
        self.setup()

    def clearBox(self):
        if self.timeBox.get()!=self.exampleText:
            self.timeBox.delete(0,END)
            self.focusOut('<FocusOut>')
        self.nameBox.delete(0,END)
        self.locBox.delete(0,END)
        self.nameBox.focus()

    def modify(self,button):
        index=eval(button.grid_info()['row'])-6
        data=datetime,name,loc=self.courses[index]
        if (self.timeBox.get(),self.nameBox.get(),self.locBox.get())==data:
            self.clearBox()
            button.configure(text='Modify')
        else:
            self.clearBox()
            self.focusIn('<FocusIn>')
            self.timeBox.insert(0,datetime)
            self.nameBox.insert(0,name)
            self.locBox.insert(0,loc)
            self.addButton.configure(command=lambda :self.modifyMode(button,data))
            button['text']='Cancel'

    def modifyMode(self,button,data):
        self.add(data)
        self.addButton.configure(command=self.add)
        button['text']='Modify'

    def drop(self,button):
        index=eval(button.grid_info()['row'])-6
        for label in self.courseLabels[index]:
            label.grid_forget()
        self.courseLabels.pop(index)
        self.courses.pop(index)
        courseLabel,modifyButton,dropButton=self.courseList.pop(index)
        courseLabel.grid_forget()
        modifyButton.grid_forget()
        dropButton.grid_forget()
        for i,(courseLabel,modifyButton,dropButton) in enumerate(self.courseList[index:]):
            rowNum=i+index+6
            courseLabel.grid_forget()
            courseLabel.grid(row=rowNum,column=6)
            modifyButton.grid_forget()
            modifyButton.grid(row=rowNum,column=7)
            dropButton.grid_forget()
            dropButton.grid(row=rowNum,column=8)

    def switch(self,event):
        key=event.keysym
        widget=event.widget
        index=self.boxList.index(widget)
        if key=='Up':
            self.boxList[index-1].focus()
        elif key=='Down':
            self.boxList[(index+1)%len(self.boxList)].focus()

    def switchColor(self):
        self.colorList=self.colorList[1:]+[self.colorList[0]]
        for label in self.courseLabels:
            label.configure(bg=self.colorList[0])

    def focusIn(self,event):
        if self.timeBox.get()==self.exampleText:
            self.timeBox.delete(0,END)
            self.timeBox.configure(fg='black')

    def focusOut(self,event):
        if self.timeBox.get()=='':
            self.timeBox.insert(0,self.exampleText)
            self.timeBox.configure(fg='grey')

cp=coursePlan(root)
cp.pack()
root.mainloop()
