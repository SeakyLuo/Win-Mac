import math
import random
import datetime
import os
import time

desktop='C:\\Users\\Seaky\\Desktop\\'
DataTypeError=Exception('This data type is not supported!')

def timeused(func,iteration=1000,*args):
    '''If func has arguments, put them into args.'''
    t=time.time()
    for i in range(iteration):
        func(*args)
    return time.time()-t

def read_file(filename,decode='utf8'):
    '''Requires filename. Default decoding: utf8.'''
    file=open(filename,encoding=decode)
    content=file.read()
    try:
        content=eval(content)
    except:
        pass
    file.close()
    return content

def write_file(filename,content,mode='w',encode='utf8'):
    '''Requires filename and content.
        Default mode to write: "w"
        Default encoding: utf8.'''
    file=open(filename,mode,encoding=encode)
    if type(content)!=str:
        content=repr(content)
    file.write(content)
    file.close()

def copy_file(src,dst):
    filename=src[:find(src).last('\\')]
    write_file(dst+['',filename][have(dst).end(filename)],read_file(src))

def advancedSplit(obj,*sep):
    '''Can have multiple seperators.'''
    if sep==() or len(sep)==1:
        return obj.split(*sep)
    word=''
    lst=[]
    for i,ch in enumerate(obj):
        word+=ch
        f=find(word).any(*sep)
        if f:
            word=without(word,*f)
            if word:
                lst.append(word)
                word=''
    if word:
        lst.append(word)
    return lst
##abbreviation
asplit=advancedSplit

def similar(obj1,obj2):
    '''Check the similarity of two strings.'''
    def grade(o1,o2):
        ## Let o1>=o2
        if o1==o2:
            return 1
        if o1=='' or o2=='':
            return 0
        len_o1=len(o1)
        len_o2=len(o2)
        score=len_o2/len_o1
        if score==1:
            return eval(format(sum([o1[i]==o2[i] for i in range(len_o1) ])/len_o1,'.4f'))
        if len_o2<=15 and score>0.6:
            ps=list(reversed(find(o2).power_set()+[o2]))
            maxLen=0
            for i,sub in enumerate(ps):
                subLen=len(sub)
                if sub in o1 and maxLen<subLen:
                    maxLen=subLen
                try:
                    if i<2**len(o2)-2 and maxLen>len(ps[i+1]):
                        break
                except IndexError:
                    break
            else:
                return 0
            score=maxLen/len_o1
        if o2.lower() in o1.lower():
            if o2 in o1:
                if have(o1).start(o2):
                    score*=1.5
                else:
                    pass
            else:
                score*=0.9
        else:
            d1,d2=find(o1).count(),find(o2).count()
            sd=set(d2.keys()).difference(set(d1.keys()))
            if len(sd)==len(d2):  ##完全不一样
                return 0
            for key in d1:
                if key in d2:
##                    score*=(d2[key]/d1[key])**((d1[key]>=d2[key])*2-1)
                    if d1[key]>d2[key]:
                        score*=d2[key]/d1[key]
                    else:
                        score*=d1[key]/d2[key]
            score*=1-sum([d2.get(item) for item in sd ])/len_o2
##            不乘0.8的话similar('12345678','23')跟similar('12345678','24')都是0.25
            score*=0.8
        return eval(format(score,'.4f'))

    if type(obj1)!=str or type(obj2)!=str:
        raise DataTypeError
    if len(obj1)>=len(obj2):
        return grade(obj1,obj2)
    else:
        return grade(obj2,obj1)

def predir():
    '''Go back to the previous folder.'''
    path=os.getcwd()
    os.chdir(path[:find(path).last('\\')])

class have:
    def __init__(self,obj):
        self.support=[str,list,dict,frozenset,set,tuple]
        self.obj=obj
        self.type=type(obj)
        if self.type not in self.support:
             raise DataTypeError

    def which(self,*args):
        '''Check which elements of args are contained in the obj.'''
        contain=[ arg for arg in args if arg in self.obj ]
        if contain:
            if len(contain)==1:
                return contain[0]
            return contain
        empty=self.obj
        empty=empty.__new__(type(empty))
        return empty

    def all(self,*args):
        '''Check whether obj contains any element of the args.'''
        if args==():
            return True
        for arg in args:
            if arg not in self.obj:
                return False
        return True

    def any(self,*args):
        '''Check whether obj contains all the elements of args.'''
        if args==():
            return True
        for arg in args:
            if arg in self.obj:
                return True
        return False

    def sub(self,element):
        '''Check whether elements are in the subset of obj.'''
        if self.type==str:
            raise dataTypeError
        for sub in self.obj:
            if element in sub:
                return True
        return False

    def start(self,*args):
        '''Check whether the string starts with any occurence in args.'''
        if self.type!=str:
            raise DataTypeError
        for arg in args:
            if len(self.obj)>=len(arg):
                 if self.obj[:len(arg)]==arg:
                     return True
            else:
                return False
        return False

    begin=start

    def end(self,*args):
        '''Check whether the string ends with any occurence in args.'''
        if self.type!=str:
            raise DataTypeError
        for arg in args:
            if len(self.obj)>=len(arg):
                 if self.obj[-len(arg):]==arg:
                     return True
            else:
                return False
        return False

    def multiple(self,obj2):
        '''Check whether self.obj is the multiple of obj2'''
        if self.type not in [str,list,tuple]:
            raise DataTypeError
        if self.type!=type(obj2):
            raise Exception('Only data of the same type can be compared!')
        length1=len(l1)
        length2=len(l2)
        if length1%length2!=0:
            return False
        for i in range(0,length1,length2):
            if l1[i:i+length2]!=l2:
                return False
        return True

class find:
    def __init__(self,obj):
        self.support=[str,list,dict,tuple,set]
        self.type=type(obj)
        if self.type not in self.support:
            print('Unsupported data type automatically converts to str.')
            self.obj=repr(obj)
            self.type=str
        else:
            self.obj=obj

    def all(self,occurence):
        '''Find all the occuring positions in an obj.'''
        if self.type==str:
            return [ idx for idx in range(len(self.obj)) if occurence==self.obj[idx:idx+len(occurence)]]
        if self.type in [list,tuple]:
            return [ idx for idx in range(len(self.obj)) if occurence==self.obj[idx]]
        raise DataTypeError

    def any(self,*args):
        '''Find any element of args in obj.'''
        return [arg for arg in args if arg in self.obj]

    def second(self,occurence):
        '''Find the second occuring positions in an obj.'''
        count=0
        if self.type==str:
            for idx in range(len(self.obj)):
                if occurence==self.obj[idx:idx+len(occurence)]:
                    count+=1
                    if count==2:
                        return idx
        elif self.type in [list,tuple]:
            for idx in range(len(self.obj)):
                if occurence==self.obj[idx]:
                    count+=1
                    if count==2:
                        return idx
        raise DataTypeError

    def last(self,occurence):
        '''Find the last occuring position in an obj.'''
        if occurence not in self.obj:
            return -1
        index=self.obj.index(occurence)
        if self.type==str:
            for idx in range(len(self.obj)-1,index,-1):
                if self.obj[idx:idx+len(occurence)]==occurence:
                    index=idx
                    break
        elif self.type in [list,tuple]:
            for idx in range(len(self.obj)-1,index,-1):
                if self.obj[idx:]==occurence:
                    index=idx
                    break
        return index

    def between(self,obj1='',obj2=''):
        '''Return the obj between obj1 and obj2 (first occurence only),both of which are not included.'''
        if self.type not in [str,list,tuple]:
            raise DataTypeError
        try:
            if obj1:
                index1=self.obj.index(obj1)
            else:
                index1=0
            if obj2:
                index2=self.obj[index1:].index(obj2)+index1
            else:
                index2=None
            return self.obj[index1+len(obj1):index2]
        except ValueError:
            return self.obj.__init__()

    def count(self):
        '''Count the occurences of each element and return a dict.'''
        obj=self.obj
        if self.type==str:
            obj=list(obj)
        elif self.type not in [list,tuple]:
            raise DataTypeError
        d={}
        for item in obj:
            d[item]=d.get(item,0)+1
        return d

    def consecutive(self):
        '''Count the longest consecutive occurences.'''
        if self.type==dict:
            raise DataTypeError
        maxStreak=streak=1
        for i,ch in enumerate(self.obj):
            if i>0:
                if ch==self.obj[i-1]:
                    streak+=1
                else:
                    if streak>=maxStreak:
                        maxStreak=streak
                    streak=1
        return maxStreak

    def key(self,value):
        '''Find all the keys that have the value.'''
        if self.type!=dict:
            raise DataTypeError
        return tuple(k for k in self.obj if self.obj[k]==value)

    def power_set(self):
        '''Find all the subs of obj except the empty sub and itself.
           This fuction returns a list because set is not ordered.'''
        length=len(self.obj)
        return [self.obj[j:j+i] for i in range(1,length) for j in range(length+1-i)]


def start_with(string,occurence):
    '''Check whether the string starts with occurence.'''
    if len(string)>=len(occurence):
        return string[:len(occurence)]==occurence
    return False

def end_with(string,occurence):
    '''Check whether the string ends with occurence.'''
    if len(string)>=len(occurence):
        return string[-len(occurence):]==occurence
    return False

flatten = lambda x:[y for l in x for y in flatten(l)] if isinstance(x, list) else [x]

def rmdup(obj):
    '''Return a list without duplicates.'''
    new=[]
    for i in obj:
        if i not in new:
            new.append(i)
    typ=type(obj)
    if typ==list:
        return new
    elif typ==tuple:
        return tuple(new)

def without(obj,*args):
    '''Return an obj without elements of args.'''
    typ=type(obj)
    if typ==list:
        return [ i for i in obj if i not in args]
    if typ==tuple:
        return ( i for i in obj if i not in args)
    if typ==str:
        for arg in args:
            obj=obj.replace(arg,'')
        return obj
    if typ==dict:
        return { k:obj[k] for k in obj if k not in args}
    if typ in [set,frozenset]:
        return obj.difference(args)
    raise DataTypeError

def delta_days(day1,day2):
    '''Please enter an 8-digit number like 20170101'''
    year=lambda x:x//10000
    month=lambda x:(x%10000)//100
    day=lambda x:x%100
    start=datetime.datetime(year(day1),month(day1),day(day1))
    end=datetime.datetime(year(day2),month(day2),day(day2))
    delta=(end-start).days+1
    print(abs(delta))

isTextFile=lambda x:have(x.lower()).any('.txt','.doc','docx','.csv','.xls')

def substitute(file='',*args):
    '''To replace a with b in s, please call substitute(s,a,b).'''
    if args:
        if len(args)%2:
            raise Exception('Please type in the right number of subsitution words!')
        if isTextFile(file):
            infile=open(file)
            content=infile.read()
            infile.close()
            for i in range(0,len(args),2):
                if args[i]:
                    content=content.replace(args[i],args[i+1])
            outfile=open(file,'w')
            outfile.write(content)
            outfile.close()
            print('\nCongratulations, your file has been successfully modified!')
        else:
            for i in range(0,len(args),2):
                if args[i]:
                    file=file.replace(args[i],args[i+1])
            return file
    else:
        inputFile=''
        if file=='':
            inputFile=input('By using this function you can subtitute some words with the words you want.\nPlease type a string or a filename you want to work on below:\n>>> ')
            if isTextFile(inputFile):
                infile=open(inputFile)
                file=infile.read()
                infile.close()
            else:
                file=inputFile
        while True:
            inputSub=input('Please type in the word you want to substitute here, no input will stop this function.\n>>> ')
            if inputSub=='':
                break
            elif inputSub not in file:
                print('The word you want is not found! Please type again!')
                continue
            inputSubW=input('Please type in the word you want to substitute with here.\n>>> ')
            file=file.replace(inputSub,inputSubW)
        if inputFile.find('.')!=-1:
            outfile=open(inputFile,'w')
            outfile.write(file)
            outfile.close()
            print('\nCongratulations, your file has been successfully modified!')
        else:
            print ('\nThe file you want is:\n\n{}\n'.format(file))


##abbreviation
sub=substitute

def createList(sort=False,reverse=False,string=False): # create same elements
    print('By using this function you can create a list without typing punctuations.')
    lst=[]
    string=input('Please type STRING items seperated with space below like \'a b c\'. If you don\'t want strings please press the \'Enter\' button:\n>>> ')
    sl=string.split() # sl means string list
    for item in sl:
        lst.append(item)
    number=input('Please type NUMBERS seperated with space below like \'1 1.5 10\' or a range like \'1,10,2\'. If you don\'t want numbers please press the \'Enter\' button:\n>>> ')
    while True:
        sn=number.split()  # sn means split number list
        for item in sn:
            l=item.split(',')
            if len(l)>3:
                number=input('You typed in '+str(len(l)-3)+' more \',\' !Please type again!\n>>> ')
                lst=[]
                break
            elif len(l)==3: #quickly built a list that contains numbers from m to n
                if int(l[0])>int(l[1]):
                    for i in range(int(l[0]),int(l[1]),-abs(int(l[2]))):
                        lst.append(i)
                else:
                    for i in range(int(l[0]),int(l[1])+1,int(l[2])):
                        lst.append(i)
            elif len(l)==2:
                if int(l[0])>int(l[1]):
                    for i in range(int(l[0]),int(l[1]),-1):
                        lst.append(i)
                else:
                    for i in range(int(l[0]),int(l[1])+1):
                        lst.append(i)
            elif not item.isnumeric() and item.find('-')==0:
                lst.append(eval(item))
            elif not item.isnumeric() and item.find(',')==-1:
                print('The input should be NUMBERS!\n')
                createList()
                return
            else:
                lst.append(eval(item))
        break
    listOrTupleOrSetOrDict=input('Please type your list, tuple, set or dict here. If you want no input just press the \'Enter\' button:\n>>> ')
    if listOrTupleOrSetOrDict!='':
        while type(eval(listOrTupleOrSet)) not in [list,tuple,set,dict]:
            listOrTupleOrSetOrDict=input('Your input in not a list, tuple, set or dict! Please type again!\n>>> ')
        lst.append(listOrTupleOrSetOrDict)
    if sort:
        lst.sort()
    if reverse:
        lst.reverse()
    if string:
        s=''
        for item in lst:
            s+=str(item)+' '
        print('\''+s[:-1]+'\'')
    else:
        print(lst)

##abbreviation
cl=createList

def formatted():
    '''请叫我套路生成器'''
    fmt=input('Please input your format sentence with variables replaced by {}.\n>>> ')
    while fmt.find('{}')==-1:
        fmt=input('Please type in at least 1 pair of {}!\n>>> ')
    else:
        fmtlst=fmt.split('{}')
        printlst=[]
        while True:
            printstr=''
            var=input('Please input your variables seperated with only 1 space or comma below. No input will stop this function.\n>>> ')
            varlst=advancedSplit(var)
            if var=='':
                break
            if len(varlst)==1:
                varlst*=fmt.count('{}')
            elif len(varlst)!=fmt.count('{}'):
                print('Please type in the correct number of variables!')
                continue
            for i in range(len(varlst)):
                printstr+=fmtlst[i]+varlst[i]
            if len(fmtlst)==len(varlst)+1:
                printstr+=fmtlst[-1]
            printlst.append(printstr)
        seperation=input('How do you want to seperate them? Input your words below to seperate them. No input will be regarded as new line.\n>>> ')
        print('\nThe format sentence you want is:\n\n')
        for item in printlst:
            if seperation!='' and item!=printlst[-1]:
                print(item,end=seperation)
            else:
                print(item)

#abbreviation
fmt=formatted
