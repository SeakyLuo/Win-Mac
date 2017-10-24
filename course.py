import tkinter

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

class course:
    def __init__(self,*args):
        '''Usage: course(courseName,time,location,courseName,time,location...)
           or course(courseName,time,courseName,time...)
           or course(time,time...).
           Example: course('phys1','tr12:30-1:45','brda1610','phys1section','t3','nh1109'),
           or course('phys1','tr12:30-1:45','phys1section','t3')
           or course('tr12:30-1:45','t3')
        '''
        self.course=[]
        self.week=['m','t','w','r','f']
        self.mode=0
        self.add(*args)
        
    def add(self,*args):
        result=self.check(*args)
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
            for j in range(weekindex):
                week=time[j]
                if self.mode==1:
                    self.course.append((week,stime))
                elif self.mode==2:
                    self.course.append((week,stime,args[i]))
                else:
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

    def draw(self):
        if self.mode==1:
            for week,time in self.course:
                print(week,time)
        elif self.mode==2:
            for week,time,courseName in self.course:
                print('{}{:11} {}'.format(week,time,courseName))
        else:
            maxlen=str(max(len(courseName) for week,time,courseName,location in self.course))
            for week,time,courseName,location in self.course:
                print(('{}{:11} {:'+maxlen+'} {}').format(week,time,courseName,location))

    def write(self):
        s='M,T,W,R,F\n'
        for row in ['8', '9', '10', '11', '12', '8', '9', '10', '11', '12']:
            timetable=[0,0,0,0,0]
            for week,time in self.course:
                if time[:len(row)]==row:
                    timetable[self.week.index(week)]+=1
            s+=','.join('1'*i for i in timetable)+'\n'
        file=open('Users/luohaitian/Desktop/timetable.csv','w')
        file.write(s)
        file.close()
