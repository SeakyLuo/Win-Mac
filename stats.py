import ez
import math

class stats:
    def __init__(self,*numbers):
        '''Support int and float numbers only.'''
        self.data=()
        for i in numbers:
            if type(i)==range:
                self.data+=tuple(i)
            else:
                self.data+=(i,)
        try:            
            self.calculate()
            self.round()
        except TypeError:
            raise ez.DataTypeError
        print('Your input data is:\n{}'.format(self.data))
        self.show()

    def calculate(self):
        '''Calculate data.'''
        self.num=len(self.data)
        if self.num==1 or self.data==(self.data[0],)*self.num:
            raise Exception('Are you serious???')
        self.sorted=()
        self.reverse=False
        self.sort()
        self.count=ez.find(self.sorted).count()
        self.nodup=ez.rmdup(self.data)
        self.Max()
        self.Min()
        self.mean=sum(self.data)/self.num
        if self.mean==int(self.mean):
            self.mean=int(self.mean)
        self.Median()
        self.mode=ez.find(self.count).key(max(self.count[k] for k in self.count))
        self.var=sum((data-self.mean)**2 for data in self.data)/self.num
        self.sd=self.var**0.5
        self.group={}
        self.outlier=None
        self.Outlier()
        
    def sort(self,reverse=False):
        '''Sort data.'''
        self.reverse=reverse
        self.sorted=sorted(self.data,reverse=self.reverse)

    def Max(self,nth=1):
        '''Find the nth largest number.'''
        if not self.sorted:
            self.sort()
        if self.reverse:
            self.max=self.sorted[nth-1]
        else:
            self.max=self.sorted[-nth]

    def Min(self,nth=1):
        '''Find the nth least number.'''
        if not self.sorted:
            self.sort()
        if self.reverse:
            self.min=self.sorted[-nth]
        else:
            self.min=self.sorted[nth-1]

    def Mean(self,precision=4):
        '''Give 5 kinds of mean: Arithmatic Mean, Geometric Mean, Harmonicc Mean, Weighted Arithmatic Mean and Sqaure Mean.'''
        self.precision=presicion
        self.AM=sum(self.data)/self.num
        if self.AM==int(self.AM):
            self.AM=int(self.AM)
        self.GM=1
        for n in self.data:
            self.GM*=n
        self.GM=self,geometric**(1/self.num)
        self.HM=self.num/sum(1/n for n in self.data)
        self.wAM=sum(k*self.count[k] for k in self.count)/self.num
        self.SM=(sum(n**2 for n in self.data)/n)**0.5
        if precision>0:
            self.AM=round(self.AM,precision)
            self.GM=round(self.GM,precision)
            self.HM=round(self.HM,precision)
            self.wAM=round(self.wAM,precision)
            self.SM=round(self.SM,precision)
        print('''Arithmatic Mean: {}
                Geometric Mean: {}
                Harmonic Mean: {}
                Weighted Arithmatic Mean: {}
                Square Mean: {}'''.format(self.AM,self.GM,self.HM,self.wAM,self.SM))

    def Median(self):
        '''Find the median.'''
        if self.num%2:
            self.median=self.sorted[(self.num-1)//2]
        else:
            self.median=(self.sorted[self.num//2-1]+self.sorted[self.num//2])/2

    def Outlier(self):
        '''Outliers: less than Q1-1.5*interquartile or greater than Q3+1.5*interquartile.'''
        if self.num>=4:
            mod=self.num%4
            if mod:
                self.q1=self.sorted[(self.num-mod)//4]
                self.q3=self.sorted[(self.num*3-4+mod)//4]
            else:
                self.q1=(self.sorted[self.num//4-1]+self.sorted[self.num//4])/2
                self.q3=(self.sorted[self.num*3//4-1]+self.sorted[self.num*3//4])/2
            self.interquartile=self.q3-self.q1
            self.outlier=ez.rmdup([ i for i in self.sorted if i<self.q1-1.5*self.interquartile or i>self.q3+1.5*self.interquartile])
    
    def add(self,*numbers):
        '''Add numbers to self.data.'''
        if numbers:
            num=len(numbers)
            if num==1:
                print('1 number is added.')
            else:
                print(str(num)+' numbers are added.')
            self.data+=numbers
            self.calculate()
        else:
            print('Nothing is added.')

    def round(self,precision=4):
        '''Round numbers to a specific precision.
            If precision is negative, results will be as precise as possible.'''
        self.precision=precision
        if precision<0:
            self.mean=sum(self.data)/self.num
            self.var=sum( (data-self.mean)**2 for data in self.data)/self.num
            self.sd=math.sqrt(self.var)
        else:
            self.mean=round(self.mean,precision)
            self.var=round(self.var,precision)
            self.sd=round(self.sd,precision)

    def show(self):
        '''Print data.'''
        print('{} numbers in total.'.format(self.num))
        print('Min: {}'.format(self.min))
        print('Max: {}'.format(self.max))
        print('Mean: {}'.format(self.mean))
        print('Median: {}'.format(self.median))
        print('Mode: {}'.format(', '.join(str(i) for i in self.mode)))
        print('Variance: {}'.format(self.var))
        print('Standard Deviation: {}'.format(self.sd))
        if self.num>=4:
            if self.outlier:
                print('Outliers: {}'.format(', '.join(str(i) for i in self.outlier)))
            else:
                print('No outliers.')
        if self.group:
            print(self.group)

    def analyze(self,interval=-1):
        '''Group numbers with interval.'''
        if interval==-1:
            maximum=max(abs(i) for i in self.data)
            minimum=min(abs(i) for i in self.data)
            dmax=math.floor(math.log(maximum,10))+1
            dmin=1
            if minimum:
                dmin=math.floor(math.log(minimum,10))+1
            dmdiff=dmax-dmin
            diff=maximum-minimum
            ddiff=math.floor((math.log(diff,10)))+1
            if dmdiff==0:                
                interval=10**ddiff
                if ddiff<dmax:
                    self.group=self.count
                    print(self.group)
                    return
            elif dmdiff==1:
                interval=10**dmin
            elif dmdiff==2:
                interval=10**dmin
                if ddiff==dmax:
                    interval*=10
            elif dmdiff>=3:
                pass
        mini=self.min//interval*interval
        maxi=(self.max//interval+1)*interval
        while mini!=maxi:
            for k in self.count:
                upper=mini+interval
                if mini<=k<upper:
                    key='[{},{})'.format(mini,upper)
                    self.group[key]=self.group.get(key,0)+self.count[k]
            mini+=interval
        print(self.group)

    def rm(self,number='out',*nums):
        '''Remove all the occurences of user input.
            Set number to 'out' to remove outliers (Default).
            Set number to min to remove minimum values.
            Set number to max to remove maximum values.'''
        if number=='out':
            if self.num>4 and self.outlier:
                self.data=[i for i in self.data if i not in self.outlier]
            else:
                print('No outliers.')
                return
        else:
            if number==max:
                number=self.max
            elif number==min:
                number=self.min
            elif number not in self.data:
                print('No change')
                return
            self.data=[i for i in self.data if i not in (number,)+nums]
        before=self.num
        self.calculate()
        difference=before-self.num
        if difference==1:
            print('1 number is removed.')
        else:
            print(str(difference)+' numbers are removed.')
        self.show()

    def plot(self,binMin=False, binMax=False, nBins=20, title=''):
        '''binMin - left most boundary of histogram
        binMax - right most boundary of histogram
        nBins - number of bins to partition data into
        title - string name of histogram'''
        import cTurtle
        # set default bin boundaries
        if type(binMin) == bool:
            binMin = self.min
        if type(binMax) == bool:
            binMax = self.max

        # account for case when parameter values binMin == binMax
        if binMin == binMax:
            binMin -= 0.5
            binMax += 0.5
            nBins = 1

        # initialize the count frequency to 0 for each bin
        freq = [0]*nBins

        # fill up bins with items from self.data
        deltaBin = binMax - binMin
        for item in self.data:
            k = math.floor(nBins*(item - binMin)/deltaBin)
            if k < 0:
                k = 0
            elif k >= nBins:
                k = nBins - 1
            freq[k] += 1

        # rescale frequency data for quicker turtle graphics drawing
        maxFreq0 = max(freq)
        freq=[ freq[i]/maxFreq0 for i in range(nBins)]
        maxFreq = 1

        # set figure scale
        xMin = binMin - 0.1*deltaBin
        xMax = binMax + 0.1*deltaBin
        yMin = -0.1*maxFreq
        yMax = 1.1*maxFreq
        figure = cTurtle.Turtle()
        figure.speed(0)
        figure.setWorldCoordinates(xMin, yMin, xMax, yMax)
        figure.hideturtle()

        # draw horizontal bar at bottom
        figure.up()
        figure.goto(binMin,0)
        figure.down()
        figure.goto(binMax,0)
        figure.up()

        # label vertical axis scale
        figure.goto(binMin - 0.05*deltaBin,0)
        figure.write('0',font=("Helvetica",16,"bold"))
        figure.goto(binMin - 0.05*deltaBin,maxFreq)
        figure.write(str(maxFreq0),font=("Helvetica",16,"bold"))
        figure.goto(0.5*(binMin + binMax),1.05*maxFreq)
        figure.write(title,align="center",font=("Helvetica",16,"bold"))

        # label horizontal axis scale
        figure.goto(binMin,-0.05*maxFreq)
        figure.write(str(binMin),font=("Helvetica",16,"bold"))
        figure.goto(binMax,-0.05*maxFreq)
        figure.write(str(binMax),font=("Helvetica",16,"bold"))

        # draw a bar of height freq[i] for each bin, i
        binGap = 0.0
        for i in range(nBins):
            #figure.goto(binMin + (i + 0.5*binGap)*deltaBin/nBins, -0.05*maxFreq)
            #figure.write(str(binMin + (i + 0.5)*deltaBin/nBins), \
            #             font=("Helvetica",16,"bold"))
            figure.goto(binMin + (i + 0.5*binGap)*deltaBin/nBins, 0)
            figure.down()
            figure.pencolor("black")
            figure.fillcolor("blue")
            figure.begin_fill()
            figure.goto(binMin + (i + 0.5*binGap)*deltaBin/nBins, freq[i])
            figure.goto(binMin + (i + 1 - 0.5*binGap)*deltaBin/nBins, freq[i])
            figure.goto(binMin + (i + 1 - 0.5*binGap)*deltaBin/nBins, 0)
            figure.goto(binMin + (i + 0.5*binGap)*deltaBin/nBins, 0)
            figure.end_fill()
            figure.up()

        figure.exitOnClick()
    
##s=stats(44, 32, 40, 42, 39, 33, 47, 45, 38, 42, 49, 45, 43, 43, 31, 38, 38, 42, 36, 37, 28, 48, 38, 45, 43, 46, 36, 50, 46, 48, 27, 46, 47, 44, 44, 48, 37, 48, 49, 47, 49, 40, 40, 41, 48, 42, 42, 41, 43, 27, 27, 40, 38, 40, 42, 45, 46, 46, 49, 37, 43, 36, 41, 36, 43, 46, 47, 46, 47, 22, 49, 49, 41, 44, 41, 43, 40, 45, 48)
##s=stats(50, 42, 57, 36, 0, 54, 56, 50, 36, 45, 42, 49, 45, 54, 44, 47, 62, 54, 57, 40, 36, 43, 52, 39, 29, 0, 56, 40, 49, 52, 38, 48, 48, 46, 39, 35, 59, 47, 51, 55, 49, 56, 43, 53, 49, 53, 59, 44, 53, 28, 56, 57, 55, 45, 40, 55, 38, 48, 43, 43, 36, 42, 40, 42, 42, 48, 41, 46, 41, 36, 47, 56, 39, 48, 59, 53, 58, 54, 44, 44, 64, 58, 53, 61, 45, 37, 52, 49, 46, 59, 30, 44, 50, 35, 55, 51, 44, 52, 0, 49, 39, 39, 47, 45, 50, 47, 59, 47, 23, 46, 34, 52, 33, 42, 36, 32, 51, 27, 44, 43, 52, 49, 55, 51, 43, 46, 45, 57, 53, 57, 52, 33, 56, 54, 57, 52, 33, 32, 23, 52, 44, 54, 59, 41, 54, 43, 39, 59, 21, 53, 40, 45, 52, 62, 50, 41, 49, 49, 57, 32, 46, 49, 48, 50, 53, 41, 52, 44, 46, 38, 47, 45, 36, 35, 46, 49, 42, 50, 33, 54, 51, 60, 58, 46, 44, 28, 34, 64, 51, 58, 39, 37, 51, 50, 37, 44, 36, 26, 56, 53, 33, 41, 44, 34, 34, 34, 54, 36, 41, 35, 48, 28, 34, 51, 41, 53, 35, 59, 46, 44, 52, 56, 51, 59, 47, 37, 49, 52, 52, 53, 34, 53, 41, 47, 52, 44, 0, 31, 39, 0, 51, 54, 49, 48, 44, 53, 0, 50, 50)
