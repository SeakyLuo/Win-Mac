import math
import random
import datetime
import menu

def draw_menu(date=0,meal=None,dc=None,lan='EN'):
    '''Input date in the form of 20170717 or 1202. Year is optional.
        Or input a number less than 7 to see the menu after n days.
        Leave it nothing to view today's menu.
        For meal, input "b" for "Breakfast","l" for "Lunch","d" for "Dinner",
        "ln" for "Late Night","br" for "Brunch" to see a specific meal.
        Leave it nothing to view the complete menu.
        For dc, input the first letter of a dining common to see its menu.
        Leave it nothing to view the complete menu.
        Default menu language is "EN"(English), change lan to "ZH" to see a Chinese menu.'''
    M=menu.menu()
    M.draw(date,meal,dc,lan)

def dm(dt=0,m=None,dc=None,l='EN'):  ##abbreviation
    '''Input dt(date) in the form of 20170717 or 1202. Year is optional.
        Or input a number less than 7 to see the menu after n days.
        Leave it nothing to view today's menu.
        For m(meal), input "b" for "Breakfast","l" for "Lunch","d" for "Dinner",
        "ln" for "Late Night","br" for "Brunch" to see a specific meal.
        Leave it nothing to view the complete menu.
        For dc, input the first letter of a dining common to see its menu.
        Leave it nothing to view the complete menu.
        Default menu language is "EN"(English), change l to "ZH" to see a Chinese menu.'''
    draw_menu(dt,m,dc,l)

def flatten(lst):
    if isinstance(lst, list):
        return [ sub for l in lst for sub in flatten(l)]
    return [lst]
##flatten = lambda x:[y for l in x for y in flatten(l)] if isinstance(x, list) else [x]

def other(son,father):
    fake=eval(repr(father))
    fake.remove(son)
    return fake

def delta_days(day1,day2):
    '''Please enter an 8-digit number like 20170101'''
    year=lambda x:x//10000
    month=lambda x:(x%10000)//100
    day=lambda x:x%100
    start=datetime.datetime(year(day1),month(day1),day(day1))
    end=datetime.datetime(year(day2),month(day2),day(day2))
    delta=(end-start).days+1
    print(abs(delta))

def pH(concentration):
    '''Support pH, pOH and any pK values'''
    return -math.log(concentration,10)

def titration(volume,molarity1,molarity2,pk,product_basic=0):
    '''Support weak acid or weak base only'''
    n1=volume*molarity1
    mol=n1/(volume+n1/molarity2)
    h=(mol*10**(pk-14))**0.5
    if product_basic:
        h=10**(-14)/h
    return pH(h)

def burn_equation(formula):
    '''Please enter a formula like C8H16O2'''
    d={}
    length=len(formula)
    parentheses=False
    d_={}

    def judge(i,ch,dictionary):
        if ch.isalpha():
            if i+1==length:
                dictionary[ch]=dictionary.get(ch,0)+1
            elif formula[i+1].isnumeric():
                num=''
                while i+1<length and formula[i+1].isnumeric():
                    num+=formula[i+1]
                    i+=1
                dictionary[ch]=dictionary.get(ch,0)+eval(num)
            else:
                dictionary[ch]=dictionary.get(ch,0)+1

    for i,ch in enumerate(formula):
        if ch=='(':
            parentheses=True
        elif ch==')':
            if i+1<length and formula[i+1].isnumeric():
                multiple=eval(formula[i+1])
            for element in d_:
                d[element]=d.get(element,0)+d_[element]*multiple
            parentheses=False
        if parentheses:
            judge(i,ch,d_)
        else:
            judge(i,ch,d)

    new_d={}
    new_d[formula]=1
    new_d['CO2']=max([d.get('C',0),d.get('c',0)])
    new_d['H2O']=max([d.get('H',0),d.get('h',0)])//2
    new_d['O']=2*new_d['CO2']+new_d['H2O']-max([d.get('O',0),d.get('o',0)])
    multiple=[1,2][new_d['O']%2]
    for compound in new_d:
        new_d[compound]*=multiple
    new_d['O2']=new_d['O']//[2,1][new_d['O']%2]

    for compound in new_d:
        if new_d[compound]==1:
            new_d[compound]='+'+compound
        elif new_d[compound]==0:
            new_d[compound]=''
        else:
            new_d[compound]='+{}{}'.format(new_d[compound],compound)
    reactant='{}{}→'.format(new_d[formula],new_d['O2'])[1:]
    product='{}{}'.format(new_d['CO2'],new_d['H2O'])[1:]
    print(reactant+product)

def truth_table(formula,output='a'):
    '''Please enter the formula in terms of a string.
       Use "=>" or "->" for "imply", "+" for "exclusive or".
       Please use () for precendence in case of miscalculations.
       Default output table will be of Ts and Fs.
       Change the value of output to "full" to output a complete table,
       to "num" to output a table of 1s and 0s.'''
    TF=[True, False]
    connective=['and','or','not']

    new_formula=''
    var_lst=[]  ## for p,q,r
    compound_dict={} ## for (p and q):"method['p'] and method['q']"
    col_lst=[]  ## for display
    parentheses_stack=[]  ## put parentheses' indice
    corresponding_stack=[] ## put parentheses' indice of new_formula
    variable=''
    compound=''
    is_compound=False

    formula.strip()
    if formula[-1].isalpha():
        formula+=' '
    for i,ch in enumerate(formula):
        if ch.isalpha():
            variable+=ch
        else:
            if ch=='(':
                parentheses_stack.append(i)
                corresponding_stack.append(len(new_formula)+1)
            elif ch==')':
                try:
                    start_pos=parentheses_stack.pop()+1
                except:
                    print('The numbers of left and right parentheses do not match!')
                    return
                compound=formula[start_pos:i].strip()
                if compound not in compound_dict:
                    is_compound=True
            elif (ch=='=' or ch=='-') and formula[i+1]=='>':
                previous_variable=''
                if len(corresponding_stack)==0:
                    if new_formula.find('(')==-1:
                        new_formula='not {} or'.format(new_formula)
                    else:
                        idx=-1
                        while True:
                            previous_variable=new_formula[idx]+previous_variable
                            if new_formula[idx]=='(':
                                break
                            idx-=1
                        new_formula=new_formula[:idx]+'not {} or'.format(previous_variable.strip())
                else:
                    idx=-1
                    while True:
                        previous_variable=new_formula[idx]+previous_variable
                        idx-=1
                        if idx+1==corresponding_stack[-1]-len(new_formula):
                            break
                    new_formula=new_formula[:idx+1]+'not {} or'.format(previous_variable.strip())
                continue
            elif ch=='>':
                continue
            elif ch=='+': ##(p and not q) or (not p and q)
                continue
            if variable:
                if variable not in connective:
                    if variable not in var_lst:
                        var_lst.append(variable)
                    new_formula+='method[\'{}\']'.format(variable)
                else:
                    new_formula+=variable
                variable=''
            if is_compound:
                compound_dict[compound]=new_formula[corresponding_stack.pop():]
                is_compound=False
            new_formula+=ch

    var_num=len(var_lst)
    col_lst=var_lst+list(compound_dict.keys())+[formula]
    var_len={}
    first_line=''
    for col in col_lst:
        length=[6,len(col)+1][len(col)>5]
        var_len[col]=length
        first_line+=('{:'+str(length)+'}').format(col)
    print(first_line)

    printout=''
    file_content=','.join(col_lst)+'\n'
    table=[]

    ##assign values
    def recursive(method={}):
        length=len(method)
        if length<var_num:
            for tf in TF:
                method[var_lst[length]]=tf
                if length==var_num-1:   ## after appending if length==var_num
                    table.append(repr(method))
                recursive()
                del method[var_lst[length]]

    recursive()

    for method in table:
        method=eval(method)
        row=[]
        for col in col_lst:
            if col in compound_dict:
                row.append((eval(compound_dict[col]),var_len[col]))
            elif col==formula:
                row.append((eval(new_formula),var_len[col]))
            else:
                row.append((eval('method[\'{}\']'.format(col)),var_len[col]))
        for tf,length in row:
            printout+=('{:'+str(length)+'}').format(repr(tf))
            file_content+='{},'.format(tf)
        printout+='\n'
        file_content=file_content[:-1]+'\n'
    printout=printout[:-1]
    file_content=file_content[:-1]
    print(printout)

    try:
        infile=open('C:\\Users\\Seaky\\Desktop\\truth table.csv','w')
    except:
        print('傻逼关进程啊！')
        return
    if output=='num':
        file_content=sub(file_content,'True','1','False','0')
    elif output!='full':
##        file_content=sub(file_content,'and','∧','or','∨','not','￢')
        file_content=sub(file_content,'True','T','False','F')
    infile.write(file_content)
    infile.close()

formLst=['w','l','s','b']

def matrixLaTeX(row=None,column=None,matrix=None,printOrNot='y'):
    if row==None or column==None or matrix==None:
        inputRC=input('By using this function you will get a matrix in LaTeX form.\nInput your matrix with m rows and n columns by typing numbers seperated with space or comma.\nPlease type m and n here: ')
        while True:
            RC=newSplit(inputRC)
            if len(RC)==0:
                return
            elif len(RC)==1:
                inputRC=' '.join(2*RC)
            elif len(RC)>2:
                inputRC=input('Your input must be 2 numbers! Please type again!\n>>> ')
                continue
            for item in RC:
                if not item.isnumeric():
                    inputRC=input('Your input must be numbers! Please type again!\n>>> ')
                    continue
            break
        RC=newSplit(inputRC)
        row=int(RC[0])
        column=int(RC[1])
        inputEnt=input('Input the entries of matrix row by row seperated with space or comma.\nPlease type here: ')
        Ent=newSplit(inputEnt)
    else:
        if type(row)!=int:
            print ('Please type an integer as row number!')
            matrixLaTeX()
            return
        if type(column)!=int:
            print ('Please type an integer as column number!')
            matrixLaTeX()
            return
        if type(matrix)!=str:
            print ('Please type in your matrix in string form!')
            matrixLaTeX()
            return
        Ent=newSplit(matrix)
    difference=len(Ent)-row*column
    if difference>0:
        if difference==1:
            print('\nYou typed in 1 more entry! We will get restarted!\n')
            matrixLaTeX()
            return
        else:
            print('\nYou typed in {} more entries! We will get restarted!\n'.format(difference))
            matrixLaTeX()
            return
    elif difference<0:
        if difference==-1:
            print('\nYou need to type in 1 more entry! We will get restarted!\n')
            matrixLaTeX()
            return
        else:
            print('\nYou need to type in {} more entries! We will get restarted!\n'.format(-difference))
            matrixLaTeX()
            return
    else:
        output=''
        for i in range(row):
            for j in range(column):
                output+=Ent[i*column+j]+'&'
            output=output[:-1]+'\\\\'
        finalMatrix='$$\\begin{bmatrix}'+output[:-2]+'\\end{bmatrix}$$'
        if (row==None or column==None or matrix==None) and printOrNot in ['y','p']:
            print('\nThe matrix you want in LaTeX is:\n\n'+finalMatrix+'\n')
        else:
            return finalMatrix

def ml(r=None,c=None,m=None,pon='y'): #abbreviation
    if (r==None or c==None or m==None) and (pon=='p' or pon=='y'):
        matrixLaTeX(r,c,m,pon)
    else:
        return matrixLaTeX(r,c,m,pon)

def matrixWolframAlpha(row=None,column=None,matrix=None,leftBracket='[',rightBracket=']',printOrNot='y'):   ##no bracket
    if row==None or column==None or matrix==None:
##        inputBracket=input('By using this function you will get a matrix in WolframAlpha form.\nFirst of all, which bracket do you want to use, \'(\', \'[\'(default) or\'{\'?\n>>> ')
##        if inputBracket!='(' and ')' and '[' and ']' and '{' and '}' and '':
##            print('Please type in the correct bracket!\n')
##            matrixWolframAlpha()
##        leftBracket='['
##        rightBracket=']'
##        if inputBracket=='(' or inputBracket==')':
##            leftBracket='('
##            rightBracket=')'
##        elif inputBracket=='{' or inputBracket=='}':
##            leftBracket='{'
##            rightBracket='}'
        inputRC=input('By using this function you will get a matrix in WolframAlpha form.\nInput your matrix with m rows and n columns by typing numbers seperated with space or comma.\nPlease type m and n here: ')
        while True:
            RC=newSplit(inputRC)
            if len(RC)==0:
                return
            elif len(RC)==1:
                inputRC=' '.join(2*RC)
            elif len(RC)>2:
                inputRC=input('Your input must be 2 numbers! Please type again!\n>>> ')
                continue
            for item in RC:
                if not item.isnumeric():
                    inputRC=input('Your input must be numbers! Please type again!\n>>> ')
                    continue
            break
        RC=newSplit(inputRC)
        row=int(RC[0])
        column=int(RC[1])
        inputEnt=input('Input the entries of the matrix row by row seperated with space or comma.\nPlease type here: ')
        Ent=newSplit(inputEnt)
    else:
        if type(row)!=int:
            print ('The row number must be an integer!\n')
            matrixLaTeX()
            return
        if type(column)!=int:
            print ('The column number must be an integer!\n')
            matrixLaTeX()
            return
        if type(matrix)!=str:
            print ('Please type in your matrix in string form!\n')
            matrixLaTeX()
            return
        if (leftBracket not in ['(','[','{']) or (rightBracket not in [')',']','}']):
            print ('Please type in your brackets correctly!')
            matrixLaTeX()
            return
        Ent=newSplit(matrix)
    difference=len(Ent)-row*column
    if difference>0:
        if difference==1:
            print('\nYou typed in 1 more entry! We will get restarted!\n')
            matrixWolframAlpha()
        else:
            print('\nYou typed in {} more entries! We will get restarted!\n'.format(difference))
            matrixWolframAlpha()
        return
    elif difference<0:
        if difference==-1:
            print('\nYou need to type in 1 more entry! We will get restarted!\n')
            matrixWolframAlpha()
        else:
            print('\nYou need to type in {} more entries! We will get restarted!\n'.format(-difference))
            matrixWolframAlpha()
        return
    else:
        output=''
        for i in range(row):
            output+=leftBracket
            for j in range(column):
                output+=Ent[i*column+j]+','
            output=output[:-1]+rightBracket+','
        finalMatrix=leftBracket+output[:-1]+rightBracket
        if (row==None or column==None or matrix==None) and printOrNot in ['y','p']:
            print('\nThe matrix you want in WolframAlpha is:\n\n'+finalMatrix+'\n')
        else:
            return finalMatrix

def mw(r=None,c=None,m=None,lb='[',rb=']',pon='y'): #abbreviation
    if (r==None or c==None or m==None) and (pon=='p' or pon=='y'):
        matrixWolframAlpha(r,c,m,lb,rb,pon)
    else:
        return matrixWolframAlpha(r,c,m,lb,rb,pon)

def mf(r=None,c=None,rg=None,var=None,f=None,pon='y'):
    if r==None or c==None:
        inputRC=input('This function gives a fast way to create a m*n matrix.\nPlease type m and n seperated with space or comma here: ')
        RC=newSplit(inputRC)
        if len(RC)==0:
            return
        elif len(RC)==1:
            RC*=2
        elif len(RC)>2:
            print('\nPlease type 2 numbers!\n')
            mf()
            return
        for item in RC:
            if not item.isnumeric():
                print('\nPlease type numbers!\n')
                mf()
                return
        r=int(RC[0]) #r means rows
        c=int(RC[1]) #c means columns
    else:
        if type(r)!=int:
            print ('The row number must be an integer!\n')
            mf()
            return
        if type(c)!=int:
            print ('The column number must be an integer!\n')
            mf()
            return
    if rg!=None and type(rg)!=(tuple or list):
        print ('Please type in a tuple or a list as range!\n')
        mf()
    if rg!=None and var!=None:
        print ('You can only choose a matrix with range or a variable matrix!\n')
        mf()
    if f!=None and (f not in formLst):
        print ('Your form is not supported! Please type again!\n')
        mf()
    elif f==None:
        inputForm=input('Please type in the form that you want. \'l\' represents LaTeX form, \'w\' represents WolframAlpha form(default), \'b\' represents beautified matrix form and \'s\' represents string form.\n>>> ')
        while True:
            if inputForm=='':
                inputForm='w'
                break
            elif inputForm not in formLst:
                inputForm=input('Your form is not supported! Please type again!\n>>> ')
            else:
                break
    else:
        inputForm=f
    output='['
    var=''
    if r*c<=26 and rg==None and input('Do you want to make the matrix a multi-variables matrix?Type \'y\' representing \'yes\'. Other input will be regarded as \'no\'.\n>>> ').lower() in ['y','yes']:
        for i in range(r):
            output+='['
            for j in range(c):
                output+=repr(chr(i*c+j))+','
            output=output[:-1]+'],'
        output=output[:-1]+']'
        output=matrixConvert(form=inputForm,matrix=output)
        output=output.replace('\'','')
    else:
        var=input('Do you want to make it a variable matrix? Type in the variable if you want 1 variable: ')
        if var=='':
            newLst=None
            if rg==None:
                newLst=[]
                inputRange=input('Please type in a range like 0(will produce a matrix that only contains 0) or 1 10 or 10,2,-2:\n>>> ')
                while True:
                    boolean=True
                    lst=newSplit(inputRange)
                    for item in lst:
                        if type(eval(item))!=int:
                            inputRange=input('Your input must be integers! Please type again!\n>>> ')
                            boolean=False
                        if not boolean:
                            newLst=[]
                            break
                        newLst.append(int(item))
                    if not boolean:
                        continue
                    break
            else:
                newLst=rg
            startNum=0
            endNum=0
            step=1
            numlst=[]
            if len(newLst)==1:
                numlst=newLst*r*c
            elif len(newLst)==2:
                startNum=newLst[0]
                endNum=newLst[1]
                if startNum>endNum:
                    step=-1
                for num in range(startNum,endNum+1,step):
                    numlst.append(num)
            elif len(newLst)==3:
                startNum=newLst[0]
                endNum=newLst[1]
                if startNum>endNum:
                    step=-abs(newLst[2])
                else:
                    step=newLst[2]
                for num in range(startNum,endNum+1,step):
                    numlst.append(num)
            else:
                print('The numbers you want do not match the number of entries in the matrix!.Please type in the correct number of numbers!\n')
                mf()
                return
            if len(numlst)!=r*c:
                print('Please type in the correct numbers!\n')
                mf()
                return
            for i in range(r):
                output+='['
                for j in range(c):
                    output+=str(numlst[i*c+j])+','
                output=output[:-1]+'],'
        else:
            lb=''
            rb=''
            if inputForm=='l':
                lb='{'
                rb='}'
            for i in range(r):
                output+='['
                for j in range(c):
                    output+=repr(var+'_'+lb+str(i+1)+str(j+1)+rb)+','
                output=output[:-1]+'],'
    finalMatrix=output[:-1]+']'
    finalMatrix=matrixConvert(form=inputForm,matrix=finalMatrix)
    if var!='':
        finalMatrix=finalMatrix.replace('\'','')
    if (r==None or c==None or rg==None) and pon in ['p','y']:
        print('\nThe matrix you want is:\n\n'+finalMatrix+'\n')
    else:
        return finalMatrix

def formJudge(m):
    if type(m)!=str:
        return False
    if m.find('$$\\begin{bmatrix}')==0 and len(m)-m.find('\end{bmatrix}$$')==15 and (m.find('&') and m.find('\\'))!=-1:
        return 'l'
    elif m.find('$$\\begin{vmatrix}')==0 and len(m)-m.find('\end{vmatrix}$$')==15 and (m.find('&') and m.find('\\'))!=-1:
        return 'dl'
    elif m.find(' ')>0:
        for i in m.split():
            if not i.isalnum():
                return False
        return 's'
    elif type(eval(m))==list:
        for item in eval(m):
            if type(item)!=list:
                return False
        return 'w'
    elif m.find(' ')==-1:
        if m.isalnum():
            return 's'
        return False
    elif m.count('|')%2==0 and m.count('\n')==m.count('|')/2-1:
        return 'b'
    else:
        return False

def matrixConvert(form=None,matrix=None):
    if matrix==None:
        inputMat=input('By using this function, you can change your matrix form.\nPlease type your matrix here:').strip()
    else:
        inputMat=matrix
    if formJudge(inputMat)==False:
        print('Your matrix is not supported! Please type again!\n')
        matrixConvert()
    while True:
        if form==None:
            inputForm=input('Please type in the form that you want. \'l\' represents LaTeX form,\'w\' represents WolframAlpha form, \'b\' represents beautified matrix form and \'s\' represents string matrix form.\n>>> ').lower()
        else:
            inputForm=form
        if inputForm.lower() not in formLst:
            inputForm=input('Your matrix form is not supported! Please type again!\n>>> ')
        else:
            break
    if formJudge(inputMat)==form:
        return inputMat
    newMat=''
    if formJudge(inputMat)=='w':
        if inputForm=='l':
            inputMat=inputMat.replace('[[','$$\\begin{bmatrix}')
            inputMat=inputMat.replace(']]','\\end{bmatrix}$$')
            inputMat=inputMat.replace('],[','\\\\')
            for i in range(len(inputMat)):
                if inputMat[i]==',':
                    ch='&'
                else:
                    ch=inputMat[i]
                newMat+=ch
        elif inputForm=='w':
            newMat+=matrix
        elif inputForm=='b':
            inputMat=inputMat.replace('[[','|')
            inputMat=inputMat.replace(']]','|')
            inputMat=inputMat.replace('],[','|\n|')
            inputMat=inputMat.replace(',',' ')
            newMat=formatBMat(inputMat)
        else:
            inputMat=inputMat.replace('[[','')
            inputMat=inputMat.replace(']]','')
            inputMat=inputMat.replace('],[',' ')
            for i in range(len(inputMat)):
                if inputMat[i]==',':
                    ch=' '
                else:
                    ch=inputMat[i]
                newMat+=ch
    elif formJudge(inputMat)=='l' or 'dl':
        if formJudge(inputMat)=='dl':
            inputMat=inputMat.replace('vmatrix','bmatrix')
        if inputForm=='w':
            inputMat=inputMat.replace('$$\\begin{bmatrix}','[[')
            inputMat=inputMat.replace('\\end{bmatrix}$$',']]')
            for i in range(len(inputMat)):
                if inputMat[i]=='&':
                    ch=','
                elif inputMat[i]=='\\' and inputMat[i+1]=='\\':
                    ch='],['
                elif inputMat[i]=='\\' and inputMat[i-1]=='\\':
                    ch=''
                else:
                    ch=inputMat[i]
                newMat+=ch
        elif inputForm=='l':
            newMat+=matrix
        elif inputForm=='b':
            inputMat=inputMat.replace('$$\\begin{bmatrix}','|')
            inputMat=inputMat.replace('\\end{bmatrix}$$','|')
            inputMat=inputMat.replace('\\\\','|\n|')
            inputMat=inputMat.replace('&',' ')
            newMat=formatBMat(inputMat)
        else:
            inputMat=inputMat[18:-15]
            for ch in inputMat:
                if not ch.isalnum():
                    ch=' '
                newMat+=ch
            newMat=newMat.replace('  ',' ')
    elif formJudge(inputMat)=='b':
        if inputForm=='w':
            inputMat=inputMat[1:]+'[['
            inputMat=inputMat[:-1]+']]'
            for i in range(len(inputMat)):
                if inputMat[i]=='|' and inputMat[i+1]=='\n':
                    ch=']'
                elif inputMat[i]=='\n':
                    ch=','
                elif inputMat[i]=='|' and inputMat[i-1]=='\n':
                    ch='['
                elif inputMat[i]==' ':
                    ch=','
                else:
                    ch=inputMat[i]
                newMat+=ch
        elif inputForm=='b':
            newMat+=matrix
        if inputForm=='l':
            inputMat=inputMat[1:]+'$$\\begin{bmatrix}'
            inputMat=inputMat[:-1]+'\\end{bmatrix}$$'
            for i in range(len(inputMat)):
                if inputMat[i]==' ':
                    ch='&'
                elif inputMat[i]=='|':
                    ch='\\'
                elif inputMat[i]=='\n':
                    ch=''
                else:
                    ch=inputMat[i]
                newMat+=ch
        else:
            inputMat=inputMat[1:-1]
            for ch in inputMat:
                if not ch.isalnum():
                    ch=' '
                newMat+=ch
            newMat=newMat.replace('  ',' ')
    if form==None or matrix==None:
        print('\n'+newMat)
    else:
        return newMat

def mc(f=None,m=None): #abbreviation
    if f==None or m==None:
        matrixConvert()
    else:
        return matrixConvert(f,m)

def matrixRandom(row=None,column=None,randomrange=None,form=None,printOrNot='y'):
    if row==None or column==None:
        inputRC=input('By using this function you will get a random matrix.\nInput your matrix with m rows and n columns by typing numbers seperated with space or comma.\nPlease type m and n here: ')
        while True:
            RC=newSplit(inputRC)
            if len(RC)==0:
                return
            elif len(RC)==1:
                inputRC=' '.join(2*RC)
            elif len(RC)>2:
                inputRC=input('Your input must be 2 numbers! Please type again!\n>>> ')
                continue
            for item in RC:
                if not item.isnumeric():
                    inputRC=input('Your input must be numbers! Please type again!\n>>> ')
                    continue
            break
        RC=newSplit(inputRC)
        row=int(RC[0])
        column=int(RC[1])
    else:
        if type(row)!=int:
            print ('Please type in an integer as row number!\n')
            matrixRandom()
            return
        if type(column)!=int:
            print ('Please type in an integer as column number!\n')
            matrixRandom()
            return
    if randomrange!=None and type(rg)!=(tuple or list):
        print ('Please type in a tuple or a list as range!\n')
        matrixRandom()
        return
    elif randomrange==None:
        newLst=[]
        inputRange=input('Please type in a range like 1 10 or 2,13,3:\n>>> ')
        while True:
            boolean=True
            lst=newSplit(inputRange)
            for item in lst:
                if type(eval(item))!=int:
                    inputRange=input('Your input must be integers! Please type again!\n>>> ')
                    boolean=False
                if not boolean:
                    newLst=[]
                    break
                newLst.append(int(item))
            if not boolean:
                continue
            break
        startNum=1
        endNum=15
        step=1
        numlst=[]
        if len(newLst)==1:
            endNum=newLst[0]+1
        elif len(newLst)==2:
            if startNum>endNum:
                startNum,endNum=endNum,startNum
            startNum=newLst[0]
            endNum=newLst[1]+1
        elif len(newLst)==3:
            if startNum>endNum:
                startNum,endNum=endNum,startNum
            startNum=newLst[0]
            endNum=newLst[1]+1
            step=abs(newLst[2])
        for num in range(row*column):
            numlst.append(random.randrange(startNum,endNum,step))
    if form!=None and (form not in formLst):
        print ('Your form is not supported! Please type again!\n')
        matrixRandom()
        return
    elif form==None:
        inputForm=input('Please type in the form that you want. \'l\' represents LaTeX form, \'w\' represents WolframAlpha form(default), \'b\' represents beautified matrix form and \'s\' represents string form.\n>>> ')
        while True:
            if inputForm=='':
                inputForm='w'
                break
            elif inputForm not in formLst:
                inputForm=input('Your form is not supported! Please type again!\n>>> ')
            else:
                break
    else:
        inputForm=form
    output='['
    for i in range(row):
        output+='['
        for j in range(column):
            output+=str(numlst[i*column+j])+','
        output=output[:-1]+'],'
    finalMatrix=output[:-1]+']'
    finalMatrix=matrixConvert(form=inputForm,matrix=finalMatrix)
    if (row==None or column==None or randomrange==None) and printOrNot in ['p','y']:
        print('\nThe matrix you want is:\n\n'+finalMatrix+'\n')
    else:
        return finalMatrix

def mr(r=None,c=None,f=None,rg=None,pon='y'):   ##abbreviation
    if (r==None or c==None or m==None) and (pon=='p' or pon=='y'):
        matrixRandom(r,c,f,rg,pon)
    else:
        return matrixRandom(r,c,f,rg,pon)

def formatBMat(matrix):
    rowmatrix=matrix.replace('|',' ')
    itemlist=rowmatrix.split
    L=[]
    longest=len(itemlist[0])
    newMat=''
    for item in itemlist:
        if len(item)>longest:
            longest=len(item)
    for item in itemlist:
        L.append(('{:'+str(longest)+'}').format(item))
    r=matrix.count('\n')+1
    c=int(len(itemlist)/r)
    for i in range(r):
        newMat+='|'
        for j in range(c):
            newMat+=L[i*c+j]
            if j!=c-1:
                newMat+=' '
        newMat+='|\n'
    return newMat[:-1]

## fold line version
##def formatBMat(m):
##    rm=m.replace('|',' ')
##    l=rm.split()
##    L=[]
##    longest=len(l[0])
##    newMat=''
##    for item in l:
##        if len(item)>longest:
##            longest=len(item)
##    for item in l:
##        L.append(('{:'+str(longest)+'}').format(item))
##    r=m.count('\n')+1
##    c=int(len(l)/r)
##    for i in range(r):
##        if i==0:
##            newMat+='┌'
##        elif i==r-1:
##            newMat+='└'
##        else:
##            newMat+=' |'
##        for j in range(c):
##            newMat+=L[i*r+j]
##            if j!=c-1:
##                newMat+=' '
##        if i==0:
##            newMat+='┐\n'
##        elif i==r-1:
##            newMat+='┘'
##        else:
##            newMat+='|\n'
##    return newMat

def matrixMultiplication():
    rightMat=input('Please type in your right matrix in any form except string form.\n>>>')
    rightPower=1
    mp=[]
    if rightMat.count('^')==1:
        mp=rightMat.split('^')
        rightPower=eval(mp[1])
    elif rightMat.count('**')==1:
        mp=rightMat.split('**')
        rightPower=eval(mp[1])
    else:
        mp=[rightMat]
    if type(rightPower)!=int:
        print('The exponent must be integers! Please type again!\n')
        matrixMultiplication()
        return
    rightMat=mp[0]
    if formJudge(rightMat)==False:
        print('Your right matrix form is not supported! Please type again!\n')
        matrixMultiplication()
        return
    elif formJudge(rightMat)=='s':
        print('String form is not supported currently, please type again!\n')
        matrixMultiplication()
        return
    rightMat=eval(matrixConvert('w',rightMat))
    ml=len(rightMat)
    nl=len(rightMat[0])
    if rightPower!=1:
        if ml==nl:
            for i in range(rightPower):
                lst=[]
                for i in range(ml):
                    l=[]
                    for j in range(ml):
                        item=0
                        for k in range(ml):
                            item+=rightMat[i][k]*rightMat[k][j]
                        l.append(item)
                    lst.append(l)
                rightMat=lst
        else:
            print('This matrix can\'t be powered! Please type again!\n')
            matrixMultiplication()
            return
    while True:
        leftMat=input('Please type in your left matrix in any form besides string form, no input will stop this function.\n>>> ')
        leftPower=1
        if leftMat=='':
            break
        elif leftMat.count('^')==1:
            leftPower=int(leftMat.split('^')[1])
            leftMat=leftMat.split('^')[0]
        elif leftMat.count('**')==1:
            leftPower=int(leftMat.split('**')[1])
            leftMat=leftMat.split('**')[0]
        elif leftPower!=1:
            print('This matrix can\'t be powered! Please type again!\n')
            continue
        if formJudge(leftMat)==False:
            print('Your left matrix form is not supported! Please type again!\n')
            continue
        leftMat=eval(matrixConvert(form='w',matrix=leftMat))
        mr=len(leftMat)
        nr=len(leftMat[0])
        if nl!=mr:
            print('We can\'t do multiplication with these 2 matrices! Please type again!\n')
            continue
        for i in range(leftPower):
            lst=[]
            for i in range(ml):
                l=[]
                for j in range(nr):
                    item=0
                    for k in range(nl):
                        item+=leftMat[i][k]*rightMat[k][j]
                    l.append(item)
                lst.append(l)
            rightMat=lst
    if input('Do you want to beautify this matrix? Type \'y\' representing \'yes\', other input will be regarded as \'no\'.\n>>> ').lower()==( 'y' or 'yes' ):
        print(matrixConvert(form='b',matrix=str(rightMat).replace(' ','')))
    else:
        print('The result matrix is:\n{}'.format(str(rightMat).replace(' ','')))

def mtp(): #abbreviation
    matrixMultiplication()

def determinantLaTeX(size=None,determinant=None,printOrNot='y'):
    if size==None or determinant==None:
        inputSize=input('By using this function you will get a determinant in LaTeX form.\nPlease type in the size of the determinant here: ')
        while True:
            SIZE=newSplit(inputSize)
            if type(eval(SIZE[0]))!=int:
                inputSize=input('\The input must be a integer! Please type again!\n>>> ')
                continue
            break
        size=eval(SIZE[0])
        inputEnt=input('Input the entries of determinant row by row seperated with space or comma like \'m n\' or \'m,n\'.\nPlease type here: ')
        Ent=newSplit(inputEnt)
    else:
        if type(rc)!=int:
            print ('The row number must be an integer!\n')
            determinantLaTeX()
            return
        if type(determinant)!=str:
            print ('Please type in your determinant in string form!')
            determinantLaTeX()
            return
        if formJudge(determinant)==False:
            print ('Please type in your determinant in correct form!')
            determinantLaTeX()
            return
        Ent=newSplit(determinant)
    difference=len(Ent)-size**2
    if difference>0:
        if difference==1:
            print('\nYou typed in 1 more entry! We will get restarted!\n')
            determinantLaTeX()
        else:
            print('\nYou typed in {} more entries! We will get restarted!\n'.format(difference))
            determinantLaTeX()
        return
    elif difference<0:
        if difference==-1:
            print('\nYou need to type in 1 more entry! We will get restarted!\n')
            determinantLaTeX()
        else:
            print('\nYou need to type in {} more entries!! We will get restarted!\n'.format(-difference))
            determinantLaTeX()
        return
    else:
        output=''
        for i in range(size):
            for j in range(size):
                output+=Ent[i*size+j]+'&'
            output=output[:-1]+'\\\\'
        finalDeterminant='$$\\begin{vmatrix}'+output[:-2]+'\end{vmatrix}$$'
        if (rc==None or determinant==None) and printOrNot in ['y','p']:
            print('\nThe determinant you want in LaTeX is:\n\n'+finalDeterminant+'\n\nAnd its VALUE is:   '+str(determinantCalculation(finalDeterminant))+'\n')
        else:
            return finalDeterminant

def dl(r=None,det=None,pon='y'): #abbreviation
    if (r==None or det==None) and (pon=='y' or pon=='p'):
        determinantLaTeX()
    else:
        return determinantLaTeX(r,det,pon)

def determinantCalculation(inputDet=None):
    if inputDet==None:
        det=input('Please input your determinant in LaTeX form or WolframAlpha form: ')
    else:
        det=inputDet
    if formJudge(det) not in ['dl','w']:
        print('Please type in the correct form!\n')
        determinantCalculation()
        return
    else:
        det=eval(matrixConvert('w',det))
        def compute(determinant):
            if len(determinant)==1:
                determinantValue=determinant[0][0]
            else:
                determinantValue=0
                for i in range(len(determinant)):
                    n=[[row[j] for j in range(len(determinant)) if j != i] for row in determinant[1:]]
                    if i%2==0:
                        determinantValue+=determinant[0][i]*compute(n)
                    else:
                        determinantValue-=determinant[0][i]*compute(n)
            return determinantValue
        detValue=compute(det)
    if inputDet==None:
        print('The value of your determinant is {}.'.format(detValue))
    else:
        return detValue

def dc(det=None): #abbreviation
    if det==None:
        determinantCalculation()
    else:
        return determinantCalculation(det)

def boldedRLaTeX(n=None):
    if n==None:
        n=input('How many dimensions do you want?\nPlease type here: ')
        if n=='':
            print('$$\mathbb{R}$$')
        else:
            print('$$\mathbb{R}^'+n+'$$')
    else:
        return ('$$\mathbb{R}^'+str(n)+'$$')

def br(n=None): #abbreviation
    if n!=None:
        return boldedRLaTeX(n)
    else:
        boldedRLaTeX()

def fractionLaTeX(numerator=None,denominator=None):
    if numerator==None or denominator==None:
        numerator=input('Please type in numerator here: ')
        denominator=input('Please type in denominator here: ')
        print('$$\frac{'+numerator+'}{'+denominator+'}$$')
    else:
        return ('$$\frac{'+str(numerator)+'}{'+str(denominator)+'}$$')

def fl(n=None,d=None):
    if n!=None and d!=None:
        return fractionLaTeX(numerator=n,denominator=d)
    else:
        fractionLaTeX()

def vectorLaTeX(entry=None,vector=True,overRightArrow=False):
    if entry==None:
        entry=input('Please input your entry here: ')
    if vector==True and overRightArrow==False:
        print('$$vec{'+entry+'}$$')
    elif overRightArrow==True:
        print('$$overrightarrow{'+entry+'}$$')

def vl(e=None,v=True,a=False):
    if e==None:
        vectorLaTeX()
    else:
        vectorLaTeX(entry=e,vector=v,overRightArrow=a)

def isTextFile(filename):
    idx=filename.find('.')
    if idx==-1:
        return False
    if filename[idx+1:] in ['txt','doc','docx','xlsx','csv']:
        return True
    return False

def substitute(filename=None,*args):
    file=''
    if args==():
        inputFile=''
        if filename==None:
            inputFile=input('By using this function you can subtitute some words with the words you want.\nPlease type a string or a filename you want to work on below:\n>>> ')
            if isTextFile(inputFile):
                infile=open(inputFile)
                file=infile.read()
                infile.close()
            else:
                file=inputFile
        else:
            file=filename
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
    else:
        if len(args)%2:
            print('Please type in the right number of subsitution words!')
            substitute()
            return
        else:
            if isTextFile(filename):
                infile=open(filename)
                file=infile.read()
                infile.close()
            else:
                file=filename
            for i in range(0,len(args),2):
                file=file.replace(args[i],args[i+1])
            if isTextFile(filename):
                outfile=open(filename,'w')
                outfile.write(file)
                outfile.close()
                print('\nCongratulations, your file has been successfully modified!')
            else:
                return file

def sub(fn=None,*args):  #abbreviation
    return substitute(fn,*args)

def createList(sort=False,reverse=False,string=False): # same element create
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

def cl(srt=False,rev=False,s=False): #abbreviation
    createList(sort=srt,reverse=rev,string=s)

def formatted():
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

def fmt(): #abbreviation
    formatted()

def arrangementNum(n,m):
    '''factorial(n)/factorial(n-m)
        n!/(n-m)!'''
    return factorial(n)//factorial(n-m)

def a(n,m): #abbreviation
    '''factorial(n)/factorial(n-m)
        n!/(n-m)!'''
    return arrangementNum(n,m)

def combinationNum(n,m):
    ''' n choose m
        factorial(n)/(factorial(m)*factorial(n-m))
        n!/(m!*(n-m)!)'''
    if m>n:
        return 0
    if m>n//2:
        return combinationNum(n,n-m)
    num=1
    for i in range(n-m+1,n+1):
        num*=i
    num//=factorial(m)
    return num


def c(n,m): #abbreviation
    ''' n choose m
        factorial(n)/(factorial(m)*factorial(n-m))
        n!/(m!*(n-m)!)'''
    return combinationNum(n,m)

def fraction(n,m):
    '''Reduce n/m'''
    output='{}/{}'.format(n,m)
    negative=''
    if n*m<0:
        negative='-'
        n=abs(n)
        m=abs(m)
    if type(n)==float or type(m)==float:
        while int(n)!=n or int(m)!=m:
            n*=10
            m*=10
        n=int(n)
        m=int(m)
    new_n=n
    new_m=m
    if n%m==0:
        new_n=n//m
        new_m=1
        output+='={}{}/1'.format(negative,new_n)
    elif m%n==0:
        new_n=1
        new_m=m//n
        output+='={}1/{}'.format(negative,new_m)
    else:
        for i in range(2,int(min(n,m)**0.5)+1):
            while new_n%i==0 and new_m%i==0:
                new_n//=i
                new_m//=i
        if new_n!=n:
            output+='={}{}/{}'.format(negative,new_n,new_m)
    quotient=n/m
    if quotient==int(quotient):
        quotient=int(quotient)
        output+='='
    elif set(findPrimeFactors(new_m,False)).issubset({2,5}):
        output+='='
    else:
        output+='≈'
    output+=negative+repr(quotient)
    print(output)

def frac(n,m): #abbreviation
    '''Reduce n/m'''
    fraction(n,m)

def factorial(n):
    '''Return n!'''
    product=1
    for i in range(1,n+1):
        product*=i
    return product

def isPrime(n):
    if type(n)==int and n>=2:
        for i in range(2,int(n**0.5)+1):
            if n%i==0:
                return False
        return True
    return False

def findPrimeFactors(num,ifPrint=True):
    '''Automatically Regarded as a non-negative number'''
    num=abs(num)
    if isPrime(num) or num in [0,1]:
        return [num]
    i=num
    d={}
    for k in range(2,num//2+1):
        while i%k==0:
            d[k]=d.get(k,0)+1
            i/=k
    s=''
    if d!={}:
        for key in d:
            if d[key]==1:
                s+=str(key)+'*'
            else:
                s+='('+str(key)+'^'+str(d[key])+')*'
    if ifPrint:
        print(str(num)+'='+s[:-1])
    return list(d.keys())

def fpf(i,ifPrint=True): #abbreviation
    '''Automatically Regarded as a non-negative number'''
    return findPrimeFactors(i,ifPrint)

def findCofactors(num1,num2):
    '''Automatically Regarded as a non-negative number'''
    return [ i for i in range(2,int(min([abs(num1),abs(num2)])**0.5)+1) if num1%i==num2%i==0]

def fc(n1,n2): #abbreviation
    '''Automatically Regarded as a non-negative number'''
    return findCofactors(n1,n2)

def findAll(string,substr):
    return [ i for i in range(len(string)) if substr==string[i:i+len(substr)]]

def newSplit(s):
    l1=s.split()
    l2=[]
    for item in l1:
        l2+=item.split(',')
    for item in l2:
        if item=='':
            l2.remove(item)
    return l2

def advancedSplit(s):
    lst=[]
    d={'\'':0,'\"':0,'(':0,')':0,'[':0,']':0,'{':0,'}':0}
    item=''
    for i in range(len(s)):
        ch=s[i]
        if ch in d:
            d[ch]+=1
        if ch in [' ',','] and s[i-1] not in [' ',','] and d['\'']%2==0 and d['\"']%2==0 and d['(']==d[')'] and d['[']==d[']'] and d['{']==d['}']:
           lst.append(item)
           item=''
           ch=''
        item+=ch
        if i==len(s)-1:
            lst.append(item)
    return lst

import cTurtle

# function plotHistogram returns nothing, but produces
# a histogram plot of the numbers contained in myList
#
# Other parameters include:
# binMin - left most boundary of histogram
# binMax - right most boundary of histogram
# nBins - number of bins to partition data into
# title - string name of histogram
#
def plotHistogram(myList, binMin=False, binMax=False, nBins=20, title=''):

    # set default bin boundaries
    if type(binMin) == bool:
        binMin = min(myList)
    if type(binMax) == bool:
        binMax = max(myList)

    # account for case when parameter values binMin == binMax
    if binMin == binMax:
        binMin -= 0.5
        binMax += 0.5
        nBins = 1

    # initialize the count frequency to 0 for each bin
    freq = []
    for i in range(nBins):
        freq += [0]

    # fill up bins with items from myList
    deltaBin = binMax - binMin
    for item in myList:
        k = floor(nBins*(item - binMin)/deltaBin)
        if k < 0:
            k = 0
        elif k >= nBins:
            k = nBins - 1
        freq[k] += 1

    # rescale frequency data for quicker turtle graphics drawing
    maxFreq0 = max(freq)
    for i in range(nBins):
        freq[i] /= maxFreq0
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

