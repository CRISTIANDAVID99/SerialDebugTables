
import pandas as pd
import serial
from blessed import Terminal
from util import*


isTable = False
data = b' '
table = pd.DataFrame([])
titles = list()
columnValues   = list()

ports = getPorts()

term = Terminal()

print(term.home + term.clear + term.move_y(term.height // 2))
print(term.black_on_darkkhaki(term.center('Selecciona el puerto que quieres escuchar.')))

printPorts(0, ports)

maxPos = len(ports)
posy = 0
pressEnter = False 

while not pressEnter:
    with term.cbreak(), term.hidden_cursor():

        key =  term.inkey()
        pressEnter = "KEY_ENTER" == repr(key)

        if repr(key) == "KEY_UP":
            posy = posy-1 if posy > 0 else posy
            
        if repr(key) == "KEY_DOWN":
            posy = posy+1 if posy < maxPos-1 else posy
           
        printPorts(posy)

ser = serial.Serial(
    port=ports[posy],
    baudrate=115200,
)


print(term.hidden_cursor())
print(term.clear)


while(True):

    data = data + ser.readline()
    strData = data.decode('latin1')
    if b'<beginTable>' in data:
        isTable = True
        data = b' '

    if b'<endTable>' in data  and isTable == True :
        
        form = strData.replace('\r\n', "").replace('<endTable>', "").split(".")     
        form.pop(0)
        data = b' '

        title = form[0]
        if not(title in titles):
            titles.append(title)
        column = form[1].split(':')
        column.pop(0)

        
        columnNames = list(filter(lambda x: column.index(x) % 2 == 0, column))
        columnValues = list(filter(lambda x: column.index(x) % 2 != 0, column))
        
        
        dReg = dict(zip(columnNames, columnValues))

        #if table.empty:
        table = pd.DataFrame([dReg])
        #else:
        #    table = table.append(pd.DataFrame([dReg]), ignore_index=True)
        with term.hidden_cursor():
            i = titles.index(title)
            print(term.move(i*3,0))
            print(term.blue(title))
            print(table)
        html_table = table.to_html()

        with open('table.html', 'w') as f:
            f.write(html_table)