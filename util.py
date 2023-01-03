import serial

def getPorts():
    ports = ['COM%s' % (i + 1) for i in range(256)]
    encontrados = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            encontrados.append(port)
        except (OSError, serial.SerialException):
            pass
    return encontrados

def printPorts(select, ports):
    print(term.move(0,0))
    for port in ports:
        if select == ports.index(port):
            print(term.underline_bold_green_on_yellow(port)) 
        else:
            print(port)
