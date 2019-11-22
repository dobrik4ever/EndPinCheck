from scanner.arduino.arduino import Arduino
# from scanner.camera.camera import Camera
import pandas as pd
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QWidget
from threading import Event
import cv2
from time import sleep

def instruction(instr,d):
        if instr == 'H' or instr == 'invert':
            msg = '{} '.format(instr)
            msg += str(len(d)) + ' '
            for m in d:
                msg += '{} '.format(m)
        else:
            msg = '{} '.format(instr)
            msg += str(len(d)) + ' '
            for m in d:
                msg += '{}:{} '.format(m,d[m])
        print(msg[:-1])
        return msg[:-1]

class Focuser(QtCore.QThread):
    
    go_to = QtCore.pyqtSignal(object)
    change_speed = QtCore.pyqtSignal(object)

    def __init__(self, motor_settings, objective, arduino_signal, camera, motor='M1'):
        QtCore.QThread.__init__(self)
        self.e1 = Event()
        self.e1.clear()
        self.focus_start = objective['focus_start']
        self.focus_end = objective['focus_end']
        self.m_settings = motor_settings
        self.motor = motor
        self.ard = arduino_signal
        self.ard.connect(lambda: self.e1.set())
        
        self.camera = camera

    def run(self):
        import operator
        val = {}
        self.goto(self.focus_start)
        self.change_speed.emit(instruction('S', {self.motor : 100}))
        self.e1.wait()
        # Серж Серж Серж, бахни тут плес последовательную фокусировку, а то прям как у пидоров
        for step in range(self.focus_start, self.focus_end + 1):
            self.goto(step)
            blr = self.check_blur()
            val[step]=blr
            print(step, blr)
            
        self.focus_pos = max(val.items(), key=operator.itemgetter(1))[0]
        self.goto(self.focus_start)
        self.e1.wait()
        self.goto(self.focus_pos)
        print(self.focus_pos)
        # self.change_speed.emit(instruction('S',{self.motor : 1000}))

    def goto(self, pos):
        self.e1.clear()
        self.go_to.emit(
            {self.motor : pos}
        )
        self.e1.wait()

    def check_blur(self):
        self.camera.e2.wait()
        blr = self.get_blur_value(self.camera.frame)
        self.camera.e2.clear()
        return int(blr)

    def get_blur_value(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        return fm

class Scanner(QtCore.QObject):

    new_position_signal = QtCore.pyqtSignal(dict)
    unlock_buttons = QtCore.pyqtSignal()
    new_pos = Event()
    new_pos.clear()
  
    def __init__(self):
        super().__init__()
        self.safety = False #Ограничение моторов по координатам из степа
        self.arduino = Arduino()
        motors_settings_path = 'scanner/settings/motors.xlsx'
        objectives_settings_path = 'scanner\settings\objectives.xlsx'
        self.motors_settings = pd.read_excel(motors_settings_path,index_col='M')
        self.objective_settings = pd.read_excel(objectives_settings_path, index_col='name')
        self.objectives = self.objective_settings.index
        self.cur_objective = {
            'distance_to_kiss':0,
            'focus_end':0,
            'focus_start':0
        }
        
        self.cur_objective['distance_to_kiss'] = self.objective_settings.iloc[0]['distance_to_kiss']
        self.cur_objective['focus_end'] = self.objective_settings.iloc[0]['focus_end']
        self.cur_objective['focus_start'] = self.objective_settings.iloc[0]['focus_start']
        print(self.cur_objective)

        self.m_position = {'M1':0,'M2':0,'M3':0,'M4':0,'M5':0,'M6':0,'M7':0,'M8':0,'M9':0,'M10':0}
        self.m_borders = {'M1':0,'M2':0,'M3':0,'M4':0,'M5':0,'M6':0,'M7':0,'M8':0,'M9':0,'M10':0}
        for i in self.m_borders:
            self.m_borders[i] = self.motors_settings.loc[i,'max distance']
        # self.camera = Camera()
        
        self.arduino.new_message.connect(self.update_position)

    def select_objective(self, objective_name):
        n = objective_name
        self.cur_objective['distance_to_kiss'] = self.objective_settings.loc[n]['distance_to_kiss']
        self.cur_objective['focus_end'] = self.objective_settings.loc[n]['focus_end']
        self.cur_objective['focus_start'] = self.objective_settings.loc[n]['focus_start']
        print(n, self.cur_objective)

    def initArduinoSettings(self):
        n_motors = len(self.motors_settings['acceleration'])
        acceleration = 'A {} '.format(n_motors)
        for i in self.motors_settings.index:
            motor = i
            acc = self.motors_settings.loc[i,'acceleration']
            acceleration += '{}:{} '.format(motor,acc)
        # print(acceleration[:-1])
        self.arduino.send(acceleration[:-1])
        self.arduino.ready_to_eat.wait()
        
        n_motors = len(self.motors_settings['speed'])
        speed = 'S {} '.format(n_motors)
        for i in self.motors_settings.index:
            motor = i
            spd = self.motors_settings.loc[i,'speed']
            speed += '{}:{} '.format(motor,spd)
        
        self.arduino.send(speed[:-1])
        self.arduino.ready_to_eat.wait()
        n_motors = len(self.motors_settings['inverted'])
        invert = 'invert {} '.format(n_motors)
        for i in self.motors_settings.index:
            if self.motors_settings.loc[i,'inverted'] == 'yes':
                motor = i
                invert += '{} '.format(motor)
        
        self.arduino.send(invert[:-1])
        self.arduino.ready_to_eat.wait()
    
    def make_focus(self):
        # f = Focuser(
        #     motor_settings = self.motors_settings,
        #     objective = self.cur_objective,
        #     arduino_signal = self.arduino.done,
        #     camera = self.camera
        # )

        f = Focuser2(
            motor_speed = int(self.motors_settings.loc['M1','speed']),
            objective = self.cur_objective,
            arduino = self.arduino,
            camera = self.camera
        )

        f.go_to.connect(self.send_M)
        f.change_speed.connect(lambda x: self.arduino.send(x))
        f.start()
        pass

    def update_position(self,vector):
        vector = vector.split(' ')
        if vector[0] == 'M':
            vector = vector[1:]
            i = 0
            if len(vector)>10:
                print('ERROR')
                print(len(vector))
            else:
                motors = list(self.m_position.keys())
                for v in vector:
                    self.m_position[motors[i]] = v
                    i += 1
                # self.new_position_signal.emit(self.m_position)
                self.new_pos.set()

    def start(self):
        self.arduino.connect()
        # self.arduino.start()
        self.arduino.listen_to_serial_thread.start()
        from time import sleep
        sleep(1)
        self.initArduinoSettings()

        # self.camera.start()

    def step(self,motor,step):
        step_amount = int(self.m_position[motor]) + step
        if self.safety:
            if  step_amount <= self.m_borders[motor] and step_amount >= 0:
                msg = 'M 1 {}:{}'.format(motor,step_amount)
                print(msg)
                self.arduino.send(msg)
            else:
                print('nonono')
                self.unlock_buttons.emit()
        else:
            msg = 'M 1 {}:{}'.format(motor,step_amount)
            print(msg)
            self.arduino.send(msg)
             
    def home(self,motors):
        msg = instruction('H', motors)
        self.arduino.send(msg)

    def send_M(self, d):
        msg = instruction('M',d)
        self.arduino.send(msg)

class Focuser2(QtCore.QThread):
    
    go_to = QtCore.pyqtSignal(object)
    change_speed = QtCore.pyqtSignal(object)

    def __init__(self, motor_speed, objective, arduino, camera, motor='M1'):
        QtCore.QThread.__init__(self)
        self.done = Event()
        self.done.clear()
        self.new = Event()
        self.new.clear()
        self.focus_start = objective['focus_start']
        self.focus_end = objective['focus_end']
        self.m_speed = motor_speed
        self.motor = motor
        self.ard = arduino
        self.pos = 0
        self.ard.done.connect(lambda: self.done.set())
        self.ard.new_message.connect(lambda x: self.update_pos(pos = x))
        self.focus_speed = 100
        
        self.camera = camera

    def update_pos(self,pos):
        if pos.split(' ')[0] == 'M':
            self.pos = pos.split(' ')[1]
            self.new.set()


    def run(self):
        import operator
        val = {}
        self.goto(self.focus_start)
        self.change_speed.emit(instruction('S', {self.motor : self.focus_speed}))
        self.done.wait()
        self.goto(self.focus_end)
        # self.new.set()
        self.done.clear()

        while self.done.is_set() == False:
            self.new.wait()
            self.new.clear()
            blr = self.check_blur()
            val[self.pos] = blr
            print(self.pos, blr)
            
        self.focus_pos = max(val.items(), key=operator.itemgetter(1))[0]
        self.change_speed.emit(instruction('S', {self.motor : 1000}))
        self.goto(self.focus_start)
        self.done.wait()
        self.goto(int(self.focus_pos) - 3)
        print(self.focus_pos)
        self.change_speed.emit(instruction('S',{self.motor : self.m_speed}))

    def goto(self, pos):
        self.done.clear()
        self.go_to.emit(
            {self.motor : pos}
        )
        self.done.wait()

    def check_blur(self):
        self.camera.e2.wait()
        blr = self.get_blur_value(self.camera.frame)
        self.camera.e2.clear()
        return int(blr)

    def get_blur_value(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        return fm


if __name__ == "__main__":
    s = Scanner()
