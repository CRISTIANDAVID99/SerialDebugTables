import pandas as pd
import serial
import json
import matplotlib.pyplot as plt
import time
from blessed import Terminal
from prettytable import PrettyTable

ser = serial.Serial(
    port='COM12',
    baudrate=115200,
)

isTable = False
data = b' '
table = pd.DataFrame([])
tables = []
titles = list()

register = list([])
columnValues   = list()

term = Terminal()

print(term.home + term.clear + term.move_y(term.height // 2))
print(term.black_on_darkkhaki(term.center('press any key to continue.')))

with term.cbreak(), term.hidden_cursor():
    inp = term.inkey()

print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))
print(term.hidden_cursor())
print(term.clear)

while(True):

    data = data + ser.readline()
    strData = data.decode('latin1')
    if b'beginTable' in data:
        isTable = True
        data = b' '

    if b'endTable' in data  and isTable == True :
        
        form = strData.replace('\r\n', "").replace('endTable', "").split(".")     
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