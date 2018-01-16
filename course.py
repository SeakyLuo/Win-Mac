import ez

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
        
class course:
    def __init__(self,*args):
        '''Usage: course(courseName,time,location,courseName,time,location...)
           or course(courseName,time,courseName,time...)
           or course(time,time...).
           Example: course('phys1','tr12:30-1:45','brda1610','phys1section','t3','nh1109')
           or course('phys1','tr12:30-1:45','phys1section','t3')
           or course('tr12:30-1:45','t3')
        '''
##        self.print=True
##        self.file=False
        self.course=[]
        self.week=['m','t','w','r','f']
        self.mode=0
        self.maxlen=1
        self.add(*args)
        self.courseNum=len(self.course)
        self.overlap=[]
        for i,course in enumerate(self.course):
            week1,time1=course[:2]
            for j in range(i+1,self.courseNum):
                week2,time2=self.course[j][:2]
                if week1==week2:
                    if overlap(time1,time2):
                        if (time1,time2) not in self.overlap:
                            self.overlap.append((time1,time2))
                            try:
                                courseName1=course[2]
                                courseName2=self.course[j][2]
                                print('{}跟{}重课啦'.format(courseName1,courseName2))
                            except:
                                print('重课啦')
                else:
                    break
                
    def remove(time):
        weekindex=1
        while time[weekindex].isalpha():
            weekindex+=1
        stime=time[weekindex:]
        if stime.isnumeric():
            stime='{}:00-{}:50'.format(stime,stime)
        elif stime.count('-') and stime.count(':')<2:
            index=stime.find('-')
            qian=stime[:index]
            if qian.count(':')==0:
                qian+=':00'
            hou=stime[index:]
            if hou.count(':')==0:
                hou+=':00'
            stime=qian+hou
        for i in range(weekindex):
            week=time[i]
            self.course=[ course for course in self.course if course[0]!=week or course[1]!=stime]

    def add(self,*args):
        result=self.check(*args)
        if result==-1:
            raise Exception('格式不对哦')
        if result==3 and self.mode in [1,2]:
            raise Exception('You should input courseName,time and location.')
        elif result==2 and self.mode in [1,3]:
            raise Exception('You should input courseName and time!')
        elif result==1 and self.mode in [2,3]:
            raise Exception('You should input time only!')
        self.mode=result
        for i in range(0,len(args),self.mode):
            if self.mode==1:
                time=args[i]
            else:
                time=args[i+1]
            weekindex=1
            while time[weekindex].isalpha():
                weekindex+=1
            stime=time[weekindex:]
            if stime.isnumeric():
                stime='{}:00-{}:50'.format(stime,stime)
            elif stime.count('-') and stime.count(':')<2:
                index=stime.find('-')
                qian=stime[:index]
                if qian.count(':')==0:
                    qian+=':00'
                hou=stime[index:]
                if hou.count(':')==0:
                    hou+=':00'
                stime=qian+hou
            for j in range(weekindex):
                week=time[j]
                if self.mode==1 and (week,stime) not in self.course:
                    self.course.append((week,stime))
                elif self.mode==2 and (week,stime,args[i]) not in self.course:
                    self.course.append((week,stime,args[i]))
                elif self.mode==3 and (week,stime,args[i],args[i+2]) not in self.course:
                    self.course.append((week,stime,args[i],args[i+2]))
        self.course.sort(key=lambda x:self.week.index(x[0]))
        self.draw()

    def check(self,*args):
        lst=[]
        for arg in args:
            if '-' in arg or ':' in arg:
                lst.append(1)
                continue
            arg=arg.lower()
            index=0
            while arg[index] in self.week:
                index+=1
                if arg[index].isnumeric():
                    lst.append(1)
                    break
                if index>3:
                    lst.append(3)
                    break
            else:
                lst.append(3)
        if multiple(lst,[1]):
            return 1
        if multiple(lst,[3,1,3]):
            return 3
        if multiple(lst,[3,1]):
            return 2
        return -1

    def draw(self):
        s1=',M,T,W,R,F\n'
        timelist=['8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6', '7']
        timedict={i:['','','','',''] for i in timelist}
        for row in timelist:
            timetable=['','','','','']
            if self.mode==1:
                for week,time in self.course:
                    if time[:len(row)]==row and not time[len(row)].isnumeric():
                        timetable[self.week.index(week)]+='+'
            elif self.mode==2:
                for week,time,courseName in self.course:
                    if time[:len(row)]==row:
                        timetable[self.week.index(week)]+=courseName
            else:
                for week,time,courseName,location in self.course:
                    if time[:len(row)]==row:
                        timetable[self.week.index(week)]+=courseName+' --- '+location
            timedict[row]=timetable
            s1+=row+','+','.join(timetable)+'\n'
        maxlen=str(max( max( len(i) for i in timedict[k]) for k in timedict))
        s2=('   {:'+maxlen+'} {:'+maxlen+'} {:'+maxlen+'} {:'+maxlen+'} {:'+maxlen+'}\n').format('M','T','W','R','F')+ \
            '\n'.join( '{:2} '.format(row)+' '.join( ('{:'+maxlen+'}').format(i) for i in timedict[row] ) for row in timelist)

        print(s2)
        file=open('C:\\Users\\Seaky\\Desktop\\timetable.csv','w')
        file.write(s1)
        file.close()

##c=course('phys1','tr12:30-1:45','brda1610','phys1section','t3','nh1109',\
##         'hist2b','mw2-3:15','iv thea1','hist2bsection','r4','hssb2202',\
##         'pstat120b','mw11-12:15','nh1006','pstat120bsetion','m4','girv2115',\
##         'cs56','tr11-12:15','phelp2516','cs56section','r5','phelp3525')
##c=course('phys1','tr12:30-1:45','phys1section','t3',\
##         'hist2b','mw2-3:15','hist2bsection','r4',\
##         'pstat120b','mw11-12:15','pstat120bsetion','m4',\
##         'cs56','tr11-12:15','cs56section','r5')
##c=course('tr12:30-1:45','t3',\
##         'mw2-3:15','r4',\
##         'mw11-12:15','m4',\
##         'tr11-12:15','r5')
##c.add('tr3:30-4:45','r10')
##c.add('mw12:30-1:45','r5')
