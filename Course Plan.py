from tkinter import *
from tkinter import messagebox
import ez

root=Tk()
def evaluate(time):
    '''Time format 12:30'''
    colon=time.find(':')
    h=eval(time[:colon])
    if h<8:
        h+=12
    m=time[colon+1:]
    if m[0]=='0':
        m=eval(m[1])
    else:
        m=eval(m)
    return h*60+m

def overlap(time1,time2):
    t1=[evaluate(t) for t in time1.split('-')]
    t2=[evaluate(t) for t in time2.split('-')]
    if any(t1[0]<t<t1[1] for t in t2) or any(t2[0]<t<t2[1] for t in t1):
        return True
    return False

def length(t1,t2):
    return abs(evaluate(t2)-evaluate(t1))

class coursePlan(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.labelWidth=18
        self.widgetHeight=1
        self.aweekday=['m','t','w','r','f']
        self.weekday=['Mon','Tue','Wed','Thu','Fri']
        self.time=['{}:{}0'.format((i//2+7)%12+1,[0,3][i%2]) for i in range(24)]
        for i,date in enumerate(self.weekday):
            Label(self,text=date,width=self.labelWidth).grid(row=0,column=i+1)  ##needs bg
        for i,time in enumerate(self.time):
            Label(self,text=time,height=self.widgetHeight).grid(row=i+1,column=0)  ##needs bg
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
        self.readButton=Button(self,text='Read',command=self.read)
        self.colorButton=Button(self,text='Color',command=self.switchColor)
        self.saveButton=Button(self,text='Save',command=self.save)
        self.clearButton=Button(self,text='Clear',command=self.clear)
        self.buttonList=[self.addButton,self.readButton,self.colorButton,self.saveButton,self.clearButton]
        for i,button in enumerate(self.buttonList):
            button['borderwidth']=0.5
            button.grid(row=3+i//3,column=6+i%3)
        self.courseListLabel=Label(self,text='Course List',height=self.widgetHeight)
        self.courseListLabel.grid(row=5,column=6)
        self.read()

    def setup(self):
        self.courses=[]
        self.courseLabels=[]
        self.courseList=[]
        self.colorList=['white','pink','orange','yellow','light green','cyan','azure','violet','magenta']
        self.nameBox.focus()
        self.exception=False

    def putLabel(self,datetime,name,loc,mode=0):
        def weekIndex(datetime):
            weekindex=0
            while datetime[weekindex].isalpha():
                if datetime[weekindex] not in self.aweekday:
                    raise SyntaxError
                weekindex+=1
            return weekindex
        datetime=datetime.lower()
        try:
            weekindex=weekIndex(datetime)
            if weekindex==0:
                raise SyntaxError
            time=datetime[weekindex:]
            if time.isnumeric():
                time='{}:00-{}:50'.format(time,time)
            elif time.count('-')==1 and time.count(':')<2:
                dash=time.find('-')
                start=time[:dash]
                if start.count(':')==0:
                    start+=':00'
                end=time[dash:] ## 不用dash+1
                if end.count(':')==0:
                    end+=':00'
                time=start+end
            elif time.count('-')!=1 or time.count(':')>2:
                raise SyntaxError
            ## 时间冲突不能加课 可不可以有别的解决方法呢
            for item in self.courses:
                t2=item[0]
                weekindex2=weekIndex(t2)
                if any(weekday in datetime[:weekindex] for weekday in t2[:weekindex2]) and \
                   overlap(time,t2[weekindex2:]):
                    raise ValueError
        except SyntaxError:
            print(weekindex,time.count('-')!=1,time.count(':')>2)
##            messagebox.showinfo('Error','Invalid Time Format!\n'+self.exampleText)
            self.exception=True
            return
        except ValueError:
            messagebox.showinfo('Error','Schedule conflict!\nCourse cannot be added.')
##            print(item[1],name,any(weekday in datetime[:weekindex] for weekday in t2[:weekindex2]),overlap(time,t2[weekindex2:]))
            self.exception=True
            return
        dash=time.find('-')
        start=time[:dash]
        end=time[dash+1:]
        grids=length(start,end)//30+1
##        datetime=datetime[:weekindex]+time
        courseLabel=Label(self,text=name+[' --- '+loc,''][loc==''])
        index=-1
        if mode==0:
            rowNum=len(self.courseList)+6
            courseLabel.grid(row=rowNum,column=6)
            modifyButton=Button(self,text='Modify',height=self.widgetHeight,borderwidth=0.5)
            modifyButton.grid(row=rowNum,column=7)
            modifyButton.configure(command=lambda button=modifyButton:self.modify(button))
            dropButton=Button(self,text='Drop',command=self.drop,height=self.widgetHeight,borderwidth=0.5)
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
            
        for weekday in datetime[:weekindex]:
            day=self.weekday[self.aweekday.index(weekday)]
            label=Label(self,text=name+'\n'+loc,bg=self.colorList[0],\
                        width=self.labelWidth,height=self.widgetHeight*grids)
            self.courseLabels[index].append(label) 
            label.grid(row=self.time.index(start)+1,column=self.weekday.index(day)+1,rowspan=grids)

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
        if self.exception:
            self.exception=False
        else:
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
        for lst in self.courseLabels:
            for label in lst:
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
root.title('Schedule')
root.mainloop()
