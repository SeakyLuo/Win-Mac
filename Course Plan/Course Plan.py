from tkinter import *
from tkinter import messagebox
import ez
## sort

def evaluateTime(time):
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

def evalInfo(info):
    '''Help reduce the problem between Windows and Mac.'''
    if type(info)==str:
        return eval(info)
    return info

def overlap(time1,time2):
    t1=[evaluateTime(t) for t in time1.split('-')]
    t2=[evaluateTime(t) for t in time2.split('-')]
    if any(t1[0]<=t<=t1[1] for t in t2) or any(t2[0]<=t<=t2[1] for t in t1):
        return True
    return False

def length(t1,t2):
    return abs(evaluateTime(t2)-evaluateTime(t1))

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
        self.clearButton=Button(self,text='Clear',command=self.clear)
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
        self.dropAllButton.grid(row=3,column=11)
        self.read()

    def setup(self):
        self.courseInfo=[]
        self.courseLabels=[]
        self.courseWidgets=[]
        self.nameBox.focus()
        self.focusOut('<FocusOut>')
        self.modifyButtons=[]
        self.exception=False
        self.conflict=False

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
            ## 时间冲突
            conflict=[]
            for info in self.courseInfo:
                if mode==info: continue
                t2=info[0]
                weekindex2=weekIndex(t2)
                for weekday in t2[:weekindex2]):
                    if weekday in datetime[:weekindex] and overlap(time,t2[weekindex2:]):
                        conflict.append(t2[weekindex2:])
                if any(weekday in datetime[:weekindex] and overlap(time,t2[weekindex2:]) \
                       for weekday in t2[:weekindex2]):
                    if self.conflict: raise ValueError
                    else: self.conflict=True
        except SyntaxError:
            messagebox.showerror('Error','Invalid Time Format!\n'+self.exampleText)
            self.exception=True
            return
        except ValueError:
            messagebox.showerror('Error','You have a severe schedule conflict!\Course cannot be added!')
            self.exception=True
            return
        dash=time.find('-')
        start=time[:dash]
        end=time[dash+1:]
        grids=length(start,end)//30+1
        datetime=datetime[:weekindex]+time
        courseButton=Button(self,text=name+[' --- '+loc,''][loc==''],bg=self.colorList[0],\
                          bd=0,width=2*self.labelWidth,height=1)
        courseButton['command']=lambda :self.showCourseInfo(courseButton)
        index=-1
        if mode:
            index=self.courseInfo.index(mode)
            self.courseWidgets[index][0].grid_forget()
            courseLabel.grid(row=index+len(self.boxList)+1,column=6,columnspan=3,sticky=NSEW)
            self.courseInfo[index]=(datetime,name,loc)
            for label in self.courseLabels[index]:
                label.grid_forget()
            self.courseLabels[index]=[]
        else:
            rowNum=len(self.courseWidgets)+len(self.boxList)+1
            courseButton.grid(row=rowNum,column=6,columnspan=3,sticky=NSEW)
            copyButton=Button(self,text='Copy')
            copyButton['command']=lambda :self.copy(copyButton)
            modifyButton=Button(self,text='Modify')
            modifyButton['command']=lambda :self.modify(modifyButton)
            self.modifyButtons.append(modifyButton)
            dropButton=Button(self,text='Drop')
            dropButton['command']=lambda :self.drop(dropButton)
            butts=[copyButton,modifyButton,dropButton]
            for i,button in enumerate(butts):
                self.configureButton(button)
                button.grid(row=rowNum,column=9+i,sticky=NSEW)
            self.courseWidgets.append((courseButton,copyButton,modifyButton,dropButton))
            self.courseInfo.append((datetime,name,loc))
            self.courseLabels.append([])

        for weekday in datetime[:weekindex]:
            day=self.weekday[self.aweekday.index(weekday)]
            label=Label(self,text=name+'\n'+loc,bg=self.colorList[0],font=self.fontList[0],\
                        bd=0,width=self.labelWidth,height=grids)
            self.courseLabels[index].append(label)
            label.grid(row=self.time.index(start)+1,column=self.weekday.index(day)+1,rowspan=grids,sticky=NSEW)

    def add(self,mode=0):
        if len(self.courseInfo)==20:
            messagebox.showerror('Error','You have reached the limit of courses!')
            return
        datetime=self.timeBox.get()
        name=self.nameBox.get()
        loc=self.locBox.get()
        if datetime in ('',self.exampleText) or (datetime,name,loc) in self.courseInfo:
            return
        if name=='':
            messagebox.showerror('Error','Please input course name!')
            return
        self.putLabel(datetime,name,loc,mode)
        if self.exception:
            self.exception=False
        else:
            self.clear()

    def read(self):
        self.setup()
        self.clear()
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
        content={'courses':self.courseInfo,'color':self.colorList[0],'font':self.fontList[0]}
        ez.fwrite('settings.txt',content)

    def clear(self):
        if self.timeBox.get()!=self.exampleText:
            self.timeBox.delete(0, END)
            self.focusOut('<FocusOut>')
        self.nameBox.delete(0,END)
        self.locBox.delete(0,END)
        self.nameBox.focus()
        
    def copy(self,button):
        index=evalInfo(button.grid_info()['row'])-len(self.boxList)-1
        info=self.courseInfo[index]
        self.clear()
        self.focusIn('<FocusIn>')
        for i,box in enumerate(self.boxList):
            box.insert(0,info[i])

    def modify(self,button):
        self.clear()
        if button['text']=='Cancel':
            button['text']='Modify'
        elif button['text']=='Modify':
            ## 如果先按了一个modify再按了另一个modify
            for mb in self.modifyButtons:
                if mb['text']=='Cancel':
                    self.modify(mb)
                    break
            index=evalInfo(button.grid_info()['row'])-len(self.boxList)-1
            data=datetime,name,loc=self.courseInfo[index]            
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
        index=evalInfo(button.grid_info()['row'])-len(self.boxList)-1
        for label in self.courseLabels[index]:
            label.grid_forget()
        self.courseLabels.pop(index)
        self.courseInfo.pop(index)
        for widget in self.courseWidgets.pop(index):
            widget.grid_forget()
        for i,widgets in enumerate(self.courseWidgets[index:]):
            rowNum=i+index+len(self.boxList)+1
            for j,wid in enumerate(widgets):
                wid.grid_forget()
                wid.grid(row=rowNum,column=6+j+(j!=0)*2,columnspan=1+(j==0)*2,sticky=NSEW)
                
    def dropAll(self):
        for lst in self.courseLabels:
            for label in lst:
                label.grid_forget()
        for widget in self.courseWidgets:
            for item in widget:
                item.grid_forget()
        self.setup()

    def showCourseInfo(self,button):
        index=evalInfo(button.grid_info()['row'])-len(self.boxList)-1
        info=self.courseInfo[index]
        info=f'Time: {info[0]}\nName: {info[1]}\nLocation:{info[2]}'
        messagebox.showinfo('Course Info',info)

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
        for item in self.courseWidgets:
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
