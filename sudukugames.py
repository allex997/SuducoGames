import random as rd
import copy as cop
import time
import os
from threading import Thread
import colorama as col
import threading

col.init()

xs,xy = 3,3
drawsudoku,suducooutput = None, None

fcolor = {"WHITE": col.Fore.WHITE,"MAGENTA": col.Fore.MAGENTA,
"RED":col.Fore.RED,"YELLOW":col.Fore.YELLOW,"BLACK":col.Fore.BLACK,
"BLUE":col.Fore.BLUE,"CYAN":col.Fore.CYAN,"GREEN":col.Fore.GREEN,"RESET":col.Fore.RESET}

bcolor = {"WHITE": col.Back.WHITE,"MAGENTA": col.Back.MAGENTA,
"RED":col.Back.RED,"YELLOW":col.Back.YELLOW,"BLACK":col.Back.BLACK,
"BLUE":col.Back.BLUE,"CYAN":col.Back.CYAN,"GREEN":col.Back.GREEN,"RESET":col.Back.RESET}
def generatetable(sizex,sizey=0):
    

    def createsuduco():
        suductable =[]
        b2,b3 =True,False
        while b2:
            for y in range(sizey):
                suductable.append([])# один лишний
                numbers = [z1 for z1 in range(1,10)]# x 9
                error = 0
                if b3:
                    b3 = False
                    break
                for x in range(sizex):
                    if y>0:
                        xb = x
                        b = True
                        if b3:
                            break
                        while b:
                            z2 =[]
                            # пробегаемся сверху вниз
                            for yy in range(y):
                                z2.append(suductable[yy][x])
                            #z2 = [mn if mn not in z2 for mn in range(1,10)]
                            z3 = [mn for mn in range(1,10)]
                            z4 =[]
                            # Числа которые можно использовать которых нет сверху вниз
                            for zo in z3:
                                if zo not in z2:
                                    z4.append(zo)
                            
                            # numbers and z4
                            n0 = numbers if len(numbers) > len(z4) else z4
                            n1 = z4 if len(numbers) > len(z4) else numbers
                            z3 = []
                            # Числа которых не ни сверху вниз ни слева на право
                            for zo in n0:
                                if zo in n1:
                                    z3.append(zo)

                            #проверка по блоку xs xy # находим промежуток
                            x4 =  [x2 * xs for x2 in range(xs)]# x 0 3 6 '+1'
                            n = 0
                            prx =[]# промежуток x
                            for nn in x4:
                                if ((nn-1)<=x) and (x<=(nn-1)+xs):
                                    prx.append(nn)
                                    prx.append(nn+xs)
                                    break
                                n+=1

                            x4 =  [x2 * xy for x2 in range(xy)]# y 0 3 6 '+1'
                            n = 0
                            pry =[]# промежуток y
                            for nn in x4:
                                if ((nn-1)<=y) and (y<=(nn-1)+xy):#nn-1 ?
                                    pry.append(nn)
                                    pry.append(nn+xy)
                                    break
                                n+=1
                            
                            #что то пошло ни так
                            z4 =[]
                            for yy in range(pry[0],y+1):#pry[1]
                                n = x if yy == y else prx[1]
                                for xx in range(prx[0],n):
                                    z4.append(suductable[yy][xx])
                            
                            z2 =[]
                            for nn in range(1,10):
                                if nn not in z4:
                                    z2.append(nn)
                            
                            z4 = z2
                            

                            n0 = z3 if len(z3) > len(z4) else z4
                            n1 = z4 if len(z3) > len(z4) else z3
                            z3 = []
                            for zo in n0:
                                if zo in n1:
                                    z3.append(zo)

                            if len(z3)>0:
                                n = rd.randint(0,len(z3)-1)#z3 =[]
                                suductable[y].append(z3[n])
                                #if z3[n] in 
                                numbers.remove(z3[n])
                                if x!=xb:
                                    x+=1
                                else:
                                    b = False
                                if (x==sizex-1) and (y==sizey-1):
                                    b2 = False
                            else:
                                suductable[y].clear()# после  что то шло ни так x
                                numbers = [z1 for z1 in range(1,10)]
                                x = 0
                                error += 1# пророботать этот момент
                                if error >10: # тут ошибка
                                    suductable =[]
                                    y=0
                                    error = 0
                                    b3=True
                                    break

                    else:
                        n = rd.randint(0,len(numbers)-1)
                        if len(suductable)==0:
                            suductable.append([])
                        suductable[y].append(numbers[n])
                        numbers.remove(numbers[n])
        #
        for y in range(len(suductable)):
            if len(suductable[y])==0:# suductable[0] слишком большой
                del(suductable[y])
        
        return suductable
    
    
    def hideelements(st1):
        st = st1
        leny = len(st[:])  
        lenx = len(st[:][:])
        for y in range(leny):
            for x in range(lenx):
                if rd.randint(0,1)==0:
                    st[y][x] = ' '
        return st
    
    def graficstable(st):
        leny = len(st[:])  
        lenx = len(st[:][:])+xs+1
        for y in range(leny):
            for x in range(0,lenx,xs+1):
                st[y].insert(x,'|')
        leny = len(st[:])+xy+1 
        #lenx = len(st[:][:])
        for y in range(0,leny,xy+1):
            st.insert(y,[])
            for x in range(lenx):
                st[y].insert(x,'-')
        
        def drawcoordinat(st):
            leny = len(st)
            #y
            for y in range(leny):
                st[y].insert(0," ")

            st[0][0]="y"
            y,sy = 1,1  #sy счет
            n = xy+1    
            while y<sizey+1+xy:
                if y==n:
                    st[y][0]=" "
                    n+=xy+1
                else:
                    st[y][0]=sy
                    sy+=1
                y+=1
            # x
            st.insert(0,[])
            st.insert(0,[])
            st[1].append(" ")
            st[1].append("x")
            for x in range(2,sizex+2):
                st[1].append(x-1)#
            for x in range(2+xs,sizex+2,xs+1):
                st[1].insert(x,' ')
     
            return st
        st = drawcoordinat(st)
        return st
    cs =[]
    er = True
    while er:
        try:
            st = createsuduco()# иногда ошибка # перепроверить все с len(a[:])
        except Exception:
            er = True
        else:
            er = False
    cs.append(cop.deepcopy(st))
    st =hideelements(st)
    cs.append(cop.deepcopy(st))
    st = graficstable(st)
    global drawsudoku,suducooutput
    drawsudoku = graficstable
    def output(st,color,backcolor =[]):
        # вывод судоку
        s = ""
        bc = backcolor if len(backcolor)>0 else None
        for y in range(len(st)):
            #print()
            s += "\n"
            lenx = len(st[y])
            for x in range(lenx):
                if color[y][x] in fcolor:
                    if bc == None:
                        s +=fcolor[color[y][x]]+str(st[y][x])+" "
                    else:
                        if bc[y][x] in bcolor:
                            s +=bcolor[bc[y][x]]+fcolor[color[y][x]]+str(st[y][x])+" "
                    #print(fcolor[color[y][x]]+str(st[y][x]),end = ' ')
                #print(str(st[y][x]),end = " ")
        print(s)
        print(col.Fore.RESET)
        print(col.Back.RESET)
    #output()
    suducooutput = output

    return cs

# рисунки платные
#смена цвета
#переворот
#скрытие элементов (?)
# подмена элемента(мина)
# сдвиг
# замена на буквы
# полное самоуничтожение с выбором несколько цифр
# наложенная анимация
# замена все на 1 цифру 1 минуту
#+ миниигра
# звукове сопровождение
# перемешевание
# перемещение отдельных блоков, линий
# помехи
# растущие цифры или буквы
# боссы город

#добавить эфект правильно и неправильного ответа -y
# добавить удобное управление
clear = lambda: os.system('cls')

correctnumbercolor = "GREEN"
correctnumbercolorArr = []
errornumbercolorArr =[]
errornumber = "RED"
errornumberother = "CYAN"

def getaxisxy(st2):
    x,y = None,None
    leny = len(st2)
    for yy in range(leny):
        lenx = len(st2[yy])
        if 'x' in st2[yy]:
            for xx in range(lenx):
                if 'x' == st2[yy][xx]:
                    x = [xx,yy]
        if 'y' in st2[yy]:
            for xx in range(lenx):
                if 'y' == st2[yy][xx]:
                    y = [xx,yy]
    return x,y
    

def getxxxyyy(st2,numbercolorArr):
    
    x,y = getaxisxy(st2)
    xxx,yyy = [],[] # настоящие координаты x
    #тут неправильно
    for n in range(len(numbercolorArr)):
        #for xx in range(x[0]+1,len(st2[x[1]])):
        xxx.append(st2[x[1]].index(numbercolorArr[n]['x']))# тут может быть ошибка
        #ny=0
        for yy in range(y[1]+1,len(st2)):
            #ny+=1
            if numbercolorArr[n]['y']==st2[yy][y[0]]:
                yyy.append(yy)
                break
    
    return xxx,yyy

bcorrectnumber,bcorrecsharp = False, False
#эффект распространнения bcolor
def effectdistribution(x,y,st,frontcolor):

    def drawbackcolor(ccolorr2,direction = 0):#0
        ccolorr = cop.deepcopy(ccolorr2)
        color = cop.deepcopy(st)
        gax,gay = getaxisxy(st)
        leny = len(st)
        for yy in range(leny):
            lenx = len(st[yy])
            for xx in range(lenx):
                color[yy][xx] = "RESET"
        #        if st[yy][xx] != "|" and st[yy][xx] != "-" and xx>gax[0] and yy>gay[1]:
        #            color[yy][xx] = errornumber
        #        else:
        #            color[yy][xx] = "RESET"
        #-
        lenx = len(st[y])
        leny = len(st)
        if direction == 1:
            for i in range(2):
                if i==0:
                    zacr = ccolorr
                elif i==1:
                    zacr = "RESET"
                x1 = x+1
                x2 = x-1
                while x1<lenx-1 or x2>gay[0]+1:
                    if st[y][x2] != "|":
                            color[y][x2] = zacr
                    if st[y][x1] != "|":
                        color[y][x1] = zacr
                    if x1<lenx-1:
                        x1+=1
                    if x2>gay[0]+1:
                        x2-=1
                    clear()
                    suducooutput(st,frontcolor,color)
                    time.sleep(0.002)
            
        if direction == 2:
            for i in range(2):
                if i==0:
                    zacr = ccolorr
                elif i==1:
                    zacr = "RESET"
                y1 = y+1
                y2 = y-1
                while y1<leny-1 or y2>gax[1]+1:
                    if st[y2][x] != "-":
                            color[y2][x] = zacr
                    if st[y1][x] != "-":
                        color[y1][x] = zacr
                    if y1<leny-1:
                        y1+=1
                    if y2>gax[1]+1:
                        y2-=1
                    clear()
                    suducooutput(st,frontcolor,color)
                    time.sleep(0.002)
        
        if direction == 3:
            m =[]
            x1,y1= cop.deepcopy(x),cop.deepcopy(y)
            def dirof(x1,y1):
                diro=[{"x":x1-1,"y":y1-1},{"x":x1,"y":y1-1},{"x":x1+1,"y":y1-1},{"x":x1-1,"y":y1},{"x":x1+1,"y":y1},{"x":x1-1,"y":y1+1},{"x":x1,"y":y1+1},{"x":x1+1,"y":y1+1}]
                return diro

            m.append([])

            diro = cop.deepcopy(dirof(x1,y1))
            for n in diro:
                if n["x"]>-1 and n["x"]<len(st[y]) and n["y"]>-1 and n["y"]<len(st):
                    if st[n["y"]][n["x"]] != "-" and st[n["y"]][n["x"]] != "|":
                        m[0].append(n)

            #b = True
            while len(m[-1])>0:
                m.append([])
                for nx in m[-2]:
                    x1,y1 = nx["x"],nx["y"]
                    diro = cop.deepcopy(dirof(x1,y1))

                    for n in diro:
                        if n not in m[-1] and (x,y) !=(n["x"],n["y"]):
                            if n["x"]>-1 and n["x"]<len(st[y]) and n["y"]>-1 and n["y"]<len(st):
                                if st[n["y"]][n["x"]] != "-" and st[n["y"]][n["x"]] != "|":
                                    if n not in m[-2]:
                                        if len(m)>2:
                                            if n not in m[-3]:
                                                m[-1].append(cop.deepcopy(n))
                                        else:    
                                            m[-1].append(cop.deepcopy(n))
            for n in m:
                if len(n)==0:
                    m.remove(n)
            # m
            leny = len(st)
            for yy in range(leny):
                    lenx = len(st[yy])
                    for xx in range(lenx):
                        color[yy][xx] = "RESET"
            b = rd.randint(0,1)
            for i in range(2):
                if i==0:
                    zacr = ccolorr
                elif i==1:
                    zacr = "RESET"
                y1 = y+1
                y2 = y-1
                # Закрашивание
                for n1 in m: # [(),(),()]
                   for n2 in n1: #('x':,'y':):
                       color[n2['y']][n2['x']] = zacr
                   #color[y2][x] = zacr
                       if b==0:
                        clear()
                        suducooutput(st,frontcolor,color)
                        time.sleep(0.002)
                   if b==1:
                        clear()
                        suducooutput(st,frontcolor,color)
                        time.sleep(0.002)
        return color
                #pass
        # - direction 1
        # | drirection 2
        # # direction 3 
        # all direction 4
        #print(bcolor[errornumber])#correctnumbercolor])
        #print(col.Back.RESET)

    direct = []
    if len(errornumbercolorArr)>0:
        for n in errornumbercolorArr:
            if "axis" in n:
                if n["axis"] not in direct:
                    direct.append(n["axis"]) 
        
        while len(direct)>0:
            n = rd.randint(0,len(direct)-1)
            drawbackcolor(errornumber,direct[n])
            direct.remove(direct[n])

    global bcorrectnumber
    if len(correctnumbercolorArr)>0 and bcorrectnumber: # if правильный ход
        if " " not in st[y]:#-
            direct.append(1)
        leny = len(st)
        bsty = True
        for yy in range(leny):
            if len(st[yy])>0:
                if st[yy][x] == " ":
                    bsty = False
                    break
        if bsty:
            direct.append(2) #|
        if bcorrecsharp:
            direct.append(3) # #
        
        while len(direct)>0:
            n = rd.randint(0,len(direct)-1)
            drawbackcolor(correctnumbercolor,direct[n])
            direct.remove(direct[n])
                    #z4.append()
                    #if csh[yy][xx]==number:
                    #    errornumbercolorArr.append({"x":xx+1,"y":yy+1,"axis":3})

            #clear()
        # проверка на пустоту в случае правильного ответа

    clear()
    

border = "MAGENTA" # цвет границ
colornumber = "WHITE" # цвет цифр 
def coloring(st2):
    
    color = cop.deepcopy(st2)
    #correctstep =
    global border,colornumber
    # | -
    n = int(1) if len(color[0])==0 else int(0)
    lenx = len(color[n])
    leny = len(color)
    for yy in range(n,leny):
        lenx = len(color[yy])
        for xx in range(lenx):
            if color[yy][xx] == "|" or color[yy][xx]=="-":
                color[yy][xx] = border
            else:
                 color[yy][xx] = colornumber
    
    global correctnumbercolorArr,bcorrectnumber
    if len(correctnumbercolorArr)>0:
        # Числа правильные ответы
        #x = st2.index('x')
        
        ##### correctnumbercolorArr
        xxx,yyy = cop.deepcopy(getxxxyyy(st2,correctnumbercolorArr))           
        n = len(xxx) if len(xxx)==len(yyy) else None
        for n1 in range(n):
            color[yyy[n1]][xxx[n1]]=correctnumbercolor

            #color[yyy[len[-1]][len(xxx)-1] # последний добавленный
        if bcorrectnumber:
            effectdistribution(xxx[-1],yyy[-1],st2,color)
            bcorrectnumber = False

    global errornumbercolorArr
    if len(errornumbercolorArr)>0:
        xxx,yyy = cop.deepcopy(getxxxyyy(st2,errornumbercolorArr))
        n = len(xxx) if len(xxx)==len(yyy) else None
        color[yyy[0]][xxx[0]]=errornumber
        for n1 in range(1,n):
            color[yyy[n1]][xxx[n1]]=errornumberother
        effectdistribution(xxx[0],yyy[0],st2,color)
    
    #global addbackcolor,addfrontcolor
    #global colorbackcursor,colorfrontcursor


    return color


addbackcolor,addfrontcolor = [],[] #{'name':'focuscursor','x': ,'y': , 'color': } x = 1-9 y = 1-9
colorbackcursor,colorfrontcursor = 'WHITE','RESET'
backapcolorback,backapcolorfront = [],[]
#clear()
#suducooutput(st,frontcolor,color)
#clear()
def extra(st,cst,bst = []): # избыточные цвета # cst - передний цвет # bst - задний цвет
    global addbackcolor,addfrontcolor
    global backapcolorback,backapcolorfront

    cst = cop.deepcopy(cst)
    # Копируем то что есть
    if len(bst)>0:
        bst = cop.deepcopy(bst)
        backapcolorback = cop.deepcopy(bst)
    backapcolorfront = cop.deepcopy(cst)

    def getxxxyyy(st,x2,y2):
        x,y = getaxisxy(st)
        xxx,yyy = [],[] # настоящие координаты x
        #тут неправильно
        for n in range(len(x2)):
            #for xx in range(x[0]+1,len(st2[x[1]])):
            xxx.append(st[x[1]].index(x2[n]))# тут может быть ошибка
            #ny=0
            for yy in range(y[1]+1,len(st)):
                #ny+=1
                if y2[n]==st[yy][y[0]]:
                    yyy.append(yy)
                    break
        return xxx,yyy


    xxb,yyb = [],[]
    xxf,yyf = [],[]
    newcolorback,newcolorfront = [],[]
    # получаем x и y для данной системы x,y
    def addarrxyc(addcolor,xx,cc,yy):
        for abc in addcolor:
            if 'x' in abc and 'color' in abc and 'y' in abc:
                xx.append(abc['x'])
                cc.append(abc['color'])
                yy.append(abc['y'])
    
    addarrxyc(addbackcolor,xxb,newcolorback,yyb)
    addarrxyc(addfrontcolor,xxf,newcolorfront,yyf)
    
    xxb,yyb = getxxxyyy(st,xxb,yyb)
    xxf,yyf = getxxxyyy(st,xxf,yyf)

    # заполняем пустотой
    if len(addbackcolor)>0:
        bst =cop.deepcopy(st)
        leny = len(bst)
        for yy in range(leny):
            lenx = len(bst[yy])
            for xx in range(lenx):
                bst[yy][xx] = "RESET"


    if len(bst)>0:
        for yy,xx,cc in zip(yyb,xxb,newcolorback):
            bst[yy][xx]=cc
    
    for yy,xx,cc in zip(yyf,xxf,newcolorfront):
            cst[yy][xx]=cc
    
    return bst #cst,bst cst -bug
    #getxxxyyy(st,)
    #addbackcolor
    # if len(cst)>0:
    # меняем цвета
    
cshbackap = None
xc,yc = None,None
def redraw(csh2,control = 0):
    #if control==0:
    #    global cshbackap
    #    cshbackap = cop.deepcopy(csh2) # делаем копию неправильно
    global xc,yc
    if xc !=None and yc !=None:
        csh2[yc-1][xc-1]=" "
        xc,yc = None,None

    csh = cop.deepcopy(csh2)
    clear()
    st =cop.deepcopy(drawsudoku(csh))# появляеться
    cst = coloring(st) # color front st
    #if len(addbackcolor)>0: 
    #    bst = extra(st,cst) # cst,bst
    #    suducooutput(st,cst,bst)#,bst)
    #else:
    suducooutput(st,cst)
    global errornumbercolorArr
    if len(errornumbercolorArr)>0:
        xc,yc = errornumbercolorArr[0]['x'],errornumbercolorArr[0]['y']
        #csh[yc][xc]=" "
        errornumbercolorArr = []
    #if control==1:
    #   game([None],csh2)
    

btimegame = True
def timerr():
    global btimegame
    second = 0
    minut = 0
    hourse = 0
    while btimegame:
        time.sleep(1)
        second+=1
        if second == 60:
            minut += 1
            second = 0
        if minut == 60:
            hourse+=1
            minut = 0
            second = 0
        secondstr = '0'+str(second) if second < 10 else str(second)
        minutstr = '0'+str(minut) if minut < 10 else str(minut)
        hoursestr = '0'+str(hourse) if hourse < 10 else str(hourse)
        #print()
        os.system("title "+"Время игры: "+hoursestr+':'+minutstr+':'+secondstr)

xcursor,ycursor = 1,1
cursorfocus = False
threadfocuscursor = []
#csh3 = None
# управление клавиатурой
def control(): #dst,baccolor = []
    #from pynput import keyboard
    
    from pynput.keyboard import Key, Listener,KeyCode
    contorlkey = ['Key.enter','Key.left','Key.up','Key.right','Key.down']
    numberkey = ['1','2','3','4','5','6','7','8','9']
    def deletekeydistionary(namm,keyy,lis):# 'name' 'focuscursor' addfrontcolor
        if len(lis)>0:
            breek = False
            for afc in lis:
                    if breek:
                        breek = False
                        break
                    for nam,key in afc.items():
                        if key==keyy and nam==namm:
                            lis.remove(afc)
                            breek = True
                            break # т.к такой элеменет 1
    def endfocus():
        global cursorfocus,threadfocuscursor
        global addbackcolor,addfrontcolor,colorbackcursor,colorfrontcursor
        if len(threadfocuscursor)>0:
            del threadfocuscursor[0]
        if len(threadfocuscursor)==0:
            cursorfocus = False
            deletekeydistionary('name','focuscursor',addbackcolor)
            deletekeydistionary('name','focuscursor',addfrontcolor)
            #global cshbackap
            #redraw(cshbackap,1)

            # перерисовка
    def get_key_name(key):
        if isinstance(key, KeyCode):
            return key.char
        else:
            return str(key)
    
    def on_press(key):
        key_name = get_key_name(key)
        #if key_name in contorlkey:
        #    #print(1)
        #    print('Key {} pressed.'.format(key_name))
        
    
    def on_release(key):
        global xcursor,ycursor,cursorfocus,threadfocuscursor
        global addbackcolor,addfrontcolor,colorbackcursor,colorfrontcursor
        #global cshbackap
        lennumberx,lennumbery = 9,9
        key_name = get_key_name(key)
        if key_name in contorlkey or key_name in numberkey:
            if cursorfocus==False: 
                cursorfocus = True
            
            deletekeydistionary('name','focuscursor',addbackcolor)
            deletekeydistionary('name','focuscursor',addfrontcolor)
            addbackcolor.append({'name':'focuscursor','x':cop.deepcopy(xcursor),'y':cop.deepcopy(ycursor),'color':colorbackcursor})
            addfrontcolor.append({'name':'focuscursor','x':cop.deepcopy(xcursor),'y':cop.deepcopy(ycursor),'color':colorfrontcursor})
            #redraw(cshbackap,1)    # перерисовка
            t = threading.Timer(4.0, endfocus)
            t.name = 'timer-endfocus'
            threadfocuscursor.append(t)
            t.start()
        if key_name in contorlkey:
            if key_name=='Key.left':
                if xcursor-1<1:
                    xcursor = lennumberx
                else:
                    xcursor -= 1
            if key_name=='Key.up':
                if ycursor-1<1:
                    ycursor = lennumbery
                else:
                    ycursor-=1
            if key_name=='Key.right':
                if xcursor+1>lennumberx:
                    xcursor = 1
                else:
                    xcursor+=1
            if key_name=='Key.down':
                if ycursor+1>lennumbery:
                    ycursor = 1
                else:
                    ycursor+=1
            
            
            
    
    with Listener(
        on_press = on_press,
        on_release = on_release) as listener:
        listener.join()


def game(cs=[],csh=[]):
    def check(x,y,number):
        lenx = len(csh[0])-1
        leny = len(csh)-1
        global errornumbercolorArr,correctnumbercolorArr,bcorrectnumber,bcorrecsharp
        global xc,yc,btimegame
        def checkdiapozon():
            cx,cy = [],[]
            # ось x
            for nx in range(lenx+1):
                if csh[y][nx] !=" " and nx != x:
                    cx.append(cop.deepcopy(csh[y][nx]))
            
            for ny in range(leny+1):
                if csh[ny][x] !=" " and ny != y:
                    cy.append(cop.deepcopy(csh[ny][x]))
            
            #проверка по блоку xs xy # находим промежуток
            x4 =  [x2 * xs for x2 in range(xs)]# x 0 3 6 '+1'
            n = 0
            prx =[]# промежуток x
            for nn in x4:
                if ((nn-1)<=x) and (x<=(nn-1)+xs):
                    prx.append(nn)
                    prx.append(nn+xs)
                    break
                n+=1

            x4 =  [x2 * xy for x2 in range(xy)]# y 0 3 6 '+1'
            n = 0
            pry =[]# промежуток y
            for nn in x4:
                if ((nn-1)<=y) and (y<=(nn-1)+xy):#nn-1 ?
                    pry.append(nn)
                    pry.append(nn+xy)
                    break
                n+=1
            
            z4 =[]
            for yy in range(pry[0],pry[1]):#pry[1]
                n = prx[1]#x if yy == y else prx[1]
                for xx in range(prx[0],n):
                    if (xx!=x or yy!=y) and csh[yy][xx]!=" ":
                        z4.append(csh[yy][xx])
            
            if (number not in z4) and (number not in cx) and (number not in cy):
                return True
            else:
                return False
            
        def checkdiapozonforcolor():
            # ось x
            
            for xx in range(lenx+1):
                if csh[y][xx]==number and xx!=x:
                    errornumbercolorArr.append({"x":xx+1,"y":y+1,"axis":1})
            # ось y
            for yy in range(leny+1):
                if csh[yy][x]==number and yy!=y:
                    errornumbercolorArr.append({"x":x+1,"y":yy+1,"axis":2})
            
            #проверка по блоку xs xy # находим промежуток
            x4 =  [x2 * xs for x2 in range(xs)]
            n = 0
            prx =[]# промежуток x
            for nn in x4:
                if ((nn-1)<=x) and (x<=(nn-1)+xs):
                    prx.append(nn)
                    prx.append(nn+xs)
                    break
                n+=1

            x4 =  [x2 * xy for x2 in range(xy)]
            n = 0
            pry =[]# промежуток y
            for nn in x4:
                if ((nn-1)<=y) and (y<=(nn-1)+xy):
                    pry.append(nn)
                    pry.append(nn+xy)
                    break
                n+=1
            
            #z4 =[]
            for yy in range(pry[0],pry[1]):
                n = prx[1]#x if yy == y else prx[1]
                for xx in range(prx[0],n):
                    if (xx!=x or yy!=y) and csh[yy][xx]!=" ":
                        if csh[yy][xx]==number:
                            errornumbercolorArr.append({"x":xx+1,"y":yy+1,"axis":3})
                        # z4.append(csh[yy][xx])

        def checksharpcorrect():
            #проверка по блоку xs xy # находим промежуток
            x4 =  [x2 * xs for x2 in range(xs)]
            n = 0
            prx =[]# промежуток x
            for nn in x4:
                if ((nn-1)<=x) and (x<=(nn-1)+xs):
                    prx.append(nn)
                    prx.append(nn+xs)
                    break
                n+=1

            x4 =  [x2 * xy for x2 in range(xy)]
            n = 0
            pry =[]# промежуток y
            for nn in x4:
                if ((nn-1)<=y) and (y<=(nn-1)+xy):
                    pry.append(nn)
                    pry.append(nn+xy)
                    break
                n+=1
            
            #z4 =[]
            bstxy = True
            for yy in range(pry[0],pry[1]):
                n = prx[1]#x if yy == y else prx[1]
                if bstxy==False:
                    break
                for xx in range(prx[0],n):
                    if (xx,yy)!=(x,y):# and csh[yy][xx]!=" ":
                        if csh[yy][xx] == " ":
                            bstxy = False
                            break
            return bstxy
            



        if (0<=x<=lenx) and (0<=y<=leny) and (1<=number<=9):
            if yc!=None and xc!=None and csh[y][x]==csh[yc-1][xc-1]:
                        csh[yc-1][xc-1]=" "
                        xc,yc = None,None
                        errornumbercolorArr = []
            if (csh[y][x]==" "):# or ( if yc!=None and xc!=None else False): #and такого нет в диапозоне xc,yc
                
                if checkdiapozon(): # если правильный ответ
                    csh[y][x]=number
                    correctnumbercolorArr.append({"x":x+1,"y":y+1})
                    bcorrectnumber = True
                    bcorrecsharp = checksharpcorrect()
                else:
                    errornumbercolorArr.insert(0,{"x":x+1,"y":y+1})#число выделяем красным
                    csh[y][x]=number
                    checkdiapozonforcolor()

                    redraw(csh)
                    print('\nТакое число уже есть!!!')
                    return True
            else:
                redraw(csh)
                print('\nx: '+str(x+1)+' y: '+str(y+1)+' Число: '+str(csh[y][x]))
                return True

            # проверка на пустую ячейку
            for nz in range(len(csh)):
                for nz2 in range(len(csh[0])):
                    if csh[nz][nz2]==" ":
                        redraw(csh)
                        return True
            
            return False      
        else:
            redraw(csh)
            return True
        
    
    def networkgame():
        pass
    b = True
    checknumb = [n for n in range(1,10)]
    
    while b:
        print()
        try:
            x,y,number = int(input("Введите x: "))-1,int(input("Введите y: "))-1,int(input("Введите Число от 1 до 9: "))
            if (x+1 in checknumb) and (y+1 in checknumb) and (number in checknumb):
                b = check(x,y,number)
            else:
                redraw(csh)
        except:
            redraw(csh)
    
    btimegame = False
    redraw(csh)
    print("\nВы выйграли!!")
    #pass

def thr():
    cs,csh = cop.deepcopy(generatetable(9,9)) # изменяется csh
    redraw(csh)# испортил csh
    game(cs,csh)
# запуск таймера
thread1 = Thread(target=timerr)
thread2 = Thread(target=thr)
#thread3 = Thread(target=control)
thread1.start()
thread2.start()
#thread3.start()
thread1.join()
thread2.join()
#thread3.join()

#Зеленый правильные ходы
#Красный неправильно
# голубой где такой уже есть
# Желтый сходил соперник
# красный розовый оранжевый жёлтый зеленый голубой синий фиолетовый белый чёрный коричневый
# фиолетовый рамки


