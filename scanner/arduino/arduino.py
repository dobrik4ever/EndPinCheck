from PyQt5 import QtCore
import threading
import serial
from threading import Event, Thread
from time import sleep, time

class Arduino(QtCore.QThread):

    no_arduino_found = QtCore.pyqtSignal(str, threading.Event)
    new_message = QtCore.pyqtSignal(object)
    done = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str)
    puk = Event()
    puk.clear()

    def __init__(self, port_name="", baud_rate=250000):
        QtCore.QThread.__init__(self)
        self.last_msg = ''
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial_input = ""
        self.wait_for_dialog = threading.Event()
        self.wait_for_dialog.clear()

        self.ready_to_eat = Event()
        self.ready_to_eat.clear()
        self.listen_to_serial_thread = Thread(
            target = self.listenToSerial,
            name = 'listen to serial'
            )

    def findComPorts(self):
        import serial.tools.list_ports as listComPorts
        a = []
        while True:
            a = listComPorts.comports(include_links=True)
            if len(a) == 0:
                self.wait_for_dialog.clear()
                self.no_arduino_found.emit("No COM ports", self.wait_for_dialog)
                self.wait_for_dialog.wait()
            else:
                break
        return a

    def connect(self):
        ports = self.findComPorts()
        for port in ports:
            print(port.description)
        for port in ports:
            if "CH340" or "Arduino" in port.description:
                try:
                    print("connecting to {}...".format(port.device))
                    self.ser = serial.Serial(
                        port=port.device,
                        baudrate=self.baud_rate
                    )
                    self.portName = port.device
                    break
                except serial.SerialException:
                    pass

        print(self.portName)
        try:
            self.ser.flushInput()
        except:
            self.wait_for_dialog.clear()
            self.no_arduino_found.emit("No arduino here", self.wait_for_dialog)
            self.wait_for_dialog.wait()

        portNames_for_combox = [port.device for port in ports]
        return portNames_for_combox  

    def listenToSerial(self):
        last_input = '0'
        while True:
            try:
                t = self.ser.readline()
                t = t.decode("utf-8")
                self.serialInput = t[:-2]

                if self.serialInput != last_input:
                    self.new_message.emit(self.serialInput)
                    last_input = self.serialInput
                    self.puk.set()

                    
                    # print('received:[{}]'.format(self.serialInput))
                if self.serialInput == 'done':
                    self.ready_to_eat.set()
                    self.done.emit()
                    # print('done!')
                if self.serialInput == 'WRONG':
                    self.error.emit('Wrong command to Arduino!')
                    self.ready_to_eat.set()
                    self.done.emit()

            except Exception as e:
                print(e)

    def send(self, text):
        self.ready_to_eat.wait()
        text += '\n'
        # print('me:[{}]'.format(text))
        try:
            self.ready_to_eat.clear()
            self.ser.write(text.encode("utf-8"))
            self.last_msg = text[:-1]
        except Exception as e:
            print(e)

if __name__ == "__main__":
    a = Arduino()
    a.connect()
    a.listen_to_serial_thread.start()
    # while True:
        # a.send('A 8 M1:10000 M2:10000 M3:10000 M4:10000 M5:10000 M6:10000 M7:10000 M8:10000')
    a.send('ok')
    a.wait()
    # sleep(1)
    # a.send('M 1 M1:0')
