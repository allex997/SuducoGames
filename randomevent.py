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
# сделать prollax в 3d

import copy as cop
suduc = [[8,2,6,3,7,9,5,4,1],[1,7,5,2,6,4,9,3,8],[3,4,9,1,5,8,7,2,6],[5,8,2,7,1,6,3,9,4],[7,3,1,9,4,2,8,6,5],
[6,9,4,5,8,3,2,1,7],[4,6,3,8,9,5,1,7,2],[2,5,7,4,3,1,6,8,9],[9,1,8,6,2,7,4,5,3]]
def create():
    global suduc
    #for n in range(9):
    #    suduc.append([x for x in range(1,10)])
    suduc = [[x for x in range(1,10)] for y in range(9)]
    

def output():
    global suduc
    for z1 in suduc:
        print(z1)

def rotate(table,angle = 0):
    # 1 - 90
    # 2 - 180
    # 3 - 270
    #table = cop.deepcopy(suduc)
    suduc = cop.deepcopy(table)
    suduc2 = cop.deepcopy(suduc)
    if angle==1:
        for yy in range(len(suduc)):
            lenx = len(suduc[yy])
            for xx in range(lenx):
                suduc2[yy][xx] = suduc[xx][-yy-1]
        
    if angle==2:
        for yy in range(len(suduc)):
            lenx = len(suduc[yy])
            for xx in range(lenx):
                suduc2[yy][xx] = suduc[yy][-xx-1]
    
    #не логично
    if  angle==3:
        
        #suduc = cop.copy(suduc)
        for yy in range(len(suduc)):
            lenx = len(suduc[yy])
            for xx in range(lenx):
                suduc2[yy][xx] = suduc[xx][yy]
        
    return suduc2

def createblok(table,sizex=3,sizey=3):
    blok = []
    #table[0:3][0:3]
    leny = len(table)
    for yy in range(0,leny,sizey):
        yyy = table[yy:yy+sizey]
        lenx = len(table[yy])
        for xx in range(0,lenx,sizex):
            xxx = yyy[xx:xx+sizex]
            print(xxx)
            #pass
     #   blok.append([])
     #   
     #   for xx in range(lenx):


    return
if __name__ == "__main__":
    #create()
    #suduc = rotate(suduc,1)
    createblok(suduc)
    #output()
    #print(suduc[0:2])#[0:2])