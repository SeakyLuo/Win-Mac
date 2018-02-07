from tkinter import *
from tkinter import messagebox
import ez

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
    if any(t1[0]<=t<=t1[1] for t in t2) or any(t2[0]<=t<=t2[1] for t in t1):
        return True
    return False

def length(t1,t2):
    return abs(evaluate(t2)-evaluate(t1))

class coursePlan(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.bgcolor='mint cream'
        self['bg']=self.bgcolor
        self.buttonColor='SeaGreen1'
        self.labelWidth=18
        self.buttonWidth=6
        self.colorList=['Aquamarine', 'Gold', 'IndianRed1', 'Khaki', 'MistyRose','Moccasin', 'OliveDrab1', 'Orchid1','PeachPuff', 'Salmon', 'SkyBlue', 'SpringGreen', 'Thistle', 'Tan1', 'Thistle']
        self.fontList=['Arial', 'Calibri', 'Cambria', 'Century', 'Corbel', 'Courier', 'Georgia','Century', 'Helvetica', 'Impact', 'STENCIL', 'Times', 'TkDefaultFont', 'Verdana']
        Label(self,text='Time',relief=FLAT,bg='#00ffff',\
                  width=self.buttonWidth,height=1).grid(row=0,column=0,sticky=NSEW)
        self.aweekday=['m','t','w','r','f']
        self.weekday=['Mon','Tue','Wed','Thu','Fri']
        self.time=['{}:{}0'.format((i//2+7)%12+1,[0,3][i%2]) for i in range(24)]
        for i,date in enumerate(self.weekday):
            Label(self,text=date,relief=FLAT,bg='#00{}ff'.format(hex(250-i*25)[2:]),\
                  width=self.labelWidth,height=1).grid(row=0,column=i+1,sticky=NSEW)
        for i,time in enumerate(self.time):
            Label(self,text=time,relief=FLAT,bg='#00{}ff'.format(hex(250-i*5)[2:]),\
                  width=self.buttonWidth,height=1).grid(row=i+1,column=0,sticky=NSEW)
        self.timeLabel=Label(self,text='Time:')
        self.timeBox=Entry(self)
        self.exampleText='Example: tr12-1:15'
        self.timeBox.bind('<FocusIn>',self.focusIn)
        self.timeBox.bind('<FocusOut>',self.focusOut)
        self.nameLabel=Label(self,text='Name:')
        self.nameBox=Entry(self)
        self.locLabel=Label(self,text='Location:')
        self.locBox=Entry(self)
        self.boxList=[self.timeBox,self.nameBox,self.locBox]
        for i,(box,label) in enumerate(zip(self.boxList,[self.timeLabel,self.nameLabel,self.locLabel])):
            label.configure(anchor='n',\
                            bg='lavender',\
                            bd=0,\
                            height=1,\
                            width=self.labelWidth//2,\
                            relief=FLAT)
            label.grid(row=i,column=6,sticky=NSEW)
            box.configure(bg='lavender',\
                           bd=0,\
                           width=3*self.labelWidth//2,\
                           relief=FLAT)
            box.grid(row=i,column=7,columnspan=2,sticky=NSEW)
            box.bind('<KeyRelease>',self.switch)
        self.setup()
        self.addButton=Button(self,text='Add',command=self.add)
        self.clearButton=Button(self,text='Clear',command=self.clearBox)
        self.readButton=Button(self,text='Read',command=self.read)
        self.saveButton=Button(self,text='Save',command=self.save)
        self.colorButton=Button(self,text='Color',command=self.switchColor)
        self.fontButton=Button(self,text='Font',command=self.switchFont)
        buttonList=[self.addButton,self.clearButton,self.readButton,self.saveButton,self.colorButton,self.fontButton]
        for i,button in enumerate(buttonList):
            self.configureButton(button)
            button.grid(row=i//2,column=9+i%2,sticky=NSEW)
        Label(self,text='Course List',relief=FLAT,bg='DeepSkyBlue',\
              bd=0,width=2*self.labelWidth,height=1).grid(row=3,column=6,columnspan=3,sticky=NSEW)
        self.dropAllButton=Button(self,text='Drop All',command=self.dropAll)
        self.configureButton(self.dropAllButton)
        self.dropAllButton.grid(row=3,column=10)
        self.read()

    def setup(self):
        self.courses=[]
        self.courseLabels=[]
        self.courseList=[]
        self.nameBox.focus()
        self.focusOut('<FocusOut>')
        self.modifyButtons=[]
        self.exception=False

    def putLabel(self,datetime,name,loc,mode=0):
        def weekIndex(datetime):
            weekindex=0
            while datetime[weekindex].isalpha():
                if datetime[weekindex] not in self.aweekday: raise SyntaxError
                weekindex+=1
            return weekindex
        datetime=datetime.lower()
        try:
            weekindex=weekIndex(datetime)
            if weekindex==0: raise SyntaxError
            time=datetime[weekindex:]
            if time.isnumeric():
                time='{}:00-{}:50'.format(time,time)
            elif time.count('-')==0 and time.count==1:
                ## 4:00 -> 4:00-4:50
                time=time+'-'+time[:-2]+'50'
            elif time.count('-')==1 and time.count(':')<2:
                ## 2-3:15 -> 2:00-3:15
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
                    if mode!=item: raise ValueError
        except SyntaxError:
            messagebox.showerror('Error','Invalid Time Format!\n'+self.exampleText)
            self.exception=True
            return
        except ValueError:
            messagebox.showerror('Error','Schedule conflict!\nCourse cannot be added.')
            self.exception=True
            return
        dash=time.find('-')
        start=time[:dash]
        end=time[dash+1:]
        grids=length(start,end)//30+1
        datetime=datetime[:weekindex]+time
        courseLabel=Label(self,text=name+[' --- '+loc,''][loc==''],bg=self.colorList[0],\
                          bd=0,width=2*self.labelWidth,height=1)
        index=-1
        if mode:
            index=self.courses.index(mode)
            self.courseList[index][0].grid_forget()
            courseLabel.grid(row=index+4,column=6,columnspan=3,sticky=NSEW)
            self.courses[index]=(datetime,name,loc)
            for label in self.courseLabels[index]:
                label.grid_forget()
            self.courseLabels[index]=[]
        else:
            rowNum=len(self.courseList)+4
            courseLabel.grid(row=rowNum,column=6,columnspan=3,sticky=NSEW)
            modifyButton=Button(self,text='Modify')
            modifyButton['command']=lambda :self.modify(modifyButton)
            self.modifyButtons.append(modifyButton)
            dropButton=Button(self,text='Drop')
            dropButton['command']=lambda :self.drop(dropButton)
            pair=[modifyButton,dropButton]
            for i,button in enumerate(pair):
                self.configureButton(button)
                button.grid(row=rowNum,column=9+i,sticky=NSEW)
            self.courseList.append((courseLabel,modifyButton,dropButton))
            self.courses.append((datetime,name,loc))
            self.courseLabels.append([])

        for weekday in datetime[:weekindex]:
            day=self.weekday[self.aweekday.index(weekday)]
            label=Label(self,text=name+'\n'+loc,bg=self.colorList[0],font=self.fontList[0],\
                        bd=0,width=self.labelWidth,height=grids)
            self.courseLabels[index].append(label)
            label.grid(row=self.time.index(start)+1,column=self.weekday.index(day)+1,rowspan=grids,sticky=NSEW)

    def add(self,mode=0):
        if len(self.courses)==20:
            messagebox.showerror('Error','You have reached the limit of courses!')
            return
        datetime=self.timeBox.get()
        name=self.nameBox.get()
        loc=self.locBox.get()
        if datetime in ('',self.exampleText) or (datetime,name,loc) in self.courses:
            return
        if name=='':
            messagebox.showerror('Error','Please input course name!')
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
        color=content['color']
        if color in self.colorList:
            index1=self.colorList.index(color)
            self.colorList=self.colorList[index1:]+self.colorList[:index1]
        font=content['font']
        if font in self.fontList:
            index2=self.fontList.index(font)
            self.fontList=self.fontList[index2:]+self.fontList[:index2]
        for datetime,name,loc in content['courses']:
            self.putLabel(datetime,name,loc)

    def save(self):
        content={'courses':self.courses,'color':self.colorList[0],'font':self.fontList[0]}
        ez.fwrite('settings.txt',content)

    def clearBox(self):
        if self.timeBox.get()!=self.exampleText:
            self.timeBox.delete(0, END)
            self.focusOut('<FocusOut>')
        self.nameBox.delete(0,END)
        self.locBox.delete(0,END)
        self.nameBox.focus()

    def modify(self,button):
        self.clearBox()
        if button['text']=='Cancel':
            button['text']='Modify'
        elif button['text']=='Modify':
            ## 如果先按了一个modify再按了另一个modify
            for mb in self.modifyButtons:
                if mb['text']=='Cancel':
                    self.modify(mb)
                    break
            index=button.grid_info()['row']-4
            data=datetime,name,loc=self.courses[index]            
            self.focusIn('<FocusIn>')
            self.timeBox.insert(0,datetime)
            self.nameBox.insert(0,name)
            self.locBox.insert(0,loc)
            self.addButton['command']=lambda :self.modifyMode(button,data)
            button['text']='Cancel'

    def modifyMode(self,button,data):
        self.add(data)
        self.addButton['command']=self.add
        button['text']='Modify'

    def drop(self,button):
        index=button.grid_info()['row']-4
        for label in self.courseLabels[index]:
            label.grid_forget()
        self.courseLabels.pop(index)
        self.courses.pop(index)
        for widget in self.courseList.pop(index):
            widget.grid_forget()
        for i,widget in enumerate(self.courseList[index:]):
            rowNum=i+index+4
            for j,item in enumerate(widget):
                item.grid_forget()
                item.grid(row=rowNum,column=6+j+(j!=0)*2,columnspan=1+(j==0)*2,sticky=NSEW)
                
    def dropAll(self):
        for lst in self.courseLabels:
            for label in lst:
                label.grid_forget()
        for widget in self.courseList:
            for item in widget:
                item.grid_forget()
        self.setup()

    def configureButton(self,button):
        button.configure(bg=self.buttonColor,\
                         height=1,\
                         width=self.buttonWidth,\
                         bd=0,\
                         relief=FLAT)

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
                label['bg']=self.colorList[0]
        for item in self.courseList:
            item[0]['bg']=self.colorList[0]

    def switchFont(self):
        self.fontList=self.fontList[1:]+[self.fontList[0]]
        for lst in self.courseLabels:
            for label in lst:
                label['font']=self.fontList[0]

    def focusIn(self,event):
        if self.timeBox.get()==self.exampleText:
            self.timeBox.delete(0,END)
            self.timeBox['fg']='black'

    def focusOut(self,event):
        if self.timeBox.get()=='':
            self.timeBox.insert(0,self.exampleText)
            self.timeBox['fg']='grey39'

root=Tk()
cp=coursePlan(root)
cp.pack()
root.title('Schedule')
root.mainloop()
