import sys
sys.path.append("C:\\Users\\Seaky\\AppData\\Local\\Programs\\Python\\Python36\\Python Files")
import menu
import lyrics
import course
import stats
##lyrics=__import__("lyrics - 副本")

def lyrics_searcher(title,artist='',Print=True,save=False):
    '''Title means the title of a song.
        The artist of the song is optional but recommended for more accurate results.
        Default set to print the lyrics but not to save them.
        Change "saveAs" to the format of lyrics(Default: lrc) to save.'''
    s=lyrics.searcher(title,artist,Print,save)
    while True:
        if s.error or s.lyrics=='' or len(s.lyrics_list)==1:
            return s
        check=input('Is this what you are looking for? Press "Enter" for yes. Other input will be regarded as no.\n>>> ')
        if check:
            s.next()
        else:
            return s

##abbreviation
lsch=lyrics_searcher

def lyrics_setter(path='',artist='',src='',ow=False):
    '''Default directory: "D:\\Media\\Music". Path can be a music but need ".mp3" at the end.
       You can add artist to specify the song.
       If source, they will be regarded as user's lyrics and overwrite the existing lyrics.'''
    lrcsetter=lyrics.setter(path,artist)
    lrcsetter.add(src,ow)
    return lrcsetter

##abbreviation
lset=lyrics_setter

def draw_menu(date=0,meal=None,dc=None,lan='en'):
    '''Input date in the form of 20170717 or 1202. Year is optional.
        Or input a number less than 7 to see the menu after n days.
        Leave it nothing to view today's menu.
        For meal, input "b" for "Breakfast","l" for "Lunch","d" for "Dinner",
        "ln" for "Late Night","br" for "Brunch" to see a specific meal.
        Leave it 0 to view the complete menu.
        For dc, input the first letter of a dining common to see its menu.
        Leave it nothing to view the complete menu.
        Default menu language is "en"(English), change lan to "zh" to see a Chinese menu.'''
    M=menu.menu()
    M.draw(date,meal,dc,lan)

##abbreviation
dm=draw_menu

def coursePlan(*courses):
     '''Usage: course(courseName,time,location,courseName,time,location...)
        or course(courseName,time,courseName,time...)
        or course(time,time...).
        Example: course('phys1','tr12:30-1:45','brda1610','phys1section','t3','nh1109')
        or course('phys1','tr12:30-1:45','phys1section','t3')
        or course('tr12:30-1:45','t3')
        '''
     return course.course(*courses)
    
##abbreviation
cp=coursePlan

def stat(*numbers,prec=4,pt=True):
    '''Anaylyze numbers only.
        Usage: s=stat(1,2,3,4,5,10,range(1,21,2),prec=2,pt=False)
        Set precision(prec) to a specific number to round the results.
        If prec is negative, results will be as precise as possible.
        Set pt to False for not printing the result automatically.'''
    return stats.stats(*numbers,precision=prec,point=pt)
    
