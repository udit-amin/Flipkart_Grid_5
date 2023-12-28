import serial
import time

PORT = "COM7"
BAUD_RATE = 115200

class GRBLComms:
    def __init__(self, port, baudRate):
        self.port = port
        self.baudRate = baudRate
        self.state = False # for Z-axis toggle
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudRate)
        self.wakeupMachine()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        
        print("Machine disconnected successfuly")

    def sendCommand(self, command):
        if not self.connection:
            raise Exception("GRBL is not connected!")
        
        self.connection.write(f"{command}\r\n".encode())
    
    def waitForMovementCompletion(self, message="Idle"):
        time.sleep(1)
        idleCounter = 0

        while True:
            self.connection.reset_input_buffer()
            
            self.sendCommand('?')
            response = self.connection.readline().strip().decode()

            # when homing checks for "ok"
            if response == message:
                break

            # when moving to (x, y) checks for "Idle"
            if response != 'ok':
                # print(response)
                if 'Idle' in response:
                    # machine has reached desired location
                    idleCounter += 1

            if idleCounter >= 10:
                # count no of times machine reported to be idle
                break
        return
            

    def homeMachine(self):
        print(f'Homing machine')
        self.sendCommand("$H")
        self.waitForMovementCompletion(message="ok")

    def moveMachine(self, x, y):
        print(f'Moving machine to X:{x}, Y:{y}')

        self.sendCommand(f'G00 X{x} Y{y}')

        self.waitForMovementCompletion()
        
        print(f'reached X:{x} Y:{y}')
        return True

    def goToDropOff(self):
        self.moveMachine(275, 20)
            
    def wakeupMachine(self):
        self.connection.write(b"\r\n\r\n")
        time.sleep(2)
        self.connection.flushInput()

    def isIdle(self):
        response = grbl.sendCommand("?")
        if 'Idle' in response:
            return True
        return False
    
    def ZaxisRoutine(self):
        if self.state:
            self.sendCommand("M3 S0") # can also be changed to "M5"
        else:
            self.sendCommand("M3 S1000")
        self.state = not self.state
        time.sleep(1) # this will require some fine tuning

    def disableHardLimit(self):
        self.sendCommand('$21 = 0')

    def enableHardLimit(self):
        self.sendCommand('$21 = 1')

    def setZOff(self):
        self.state = False
        self.sendCommand("M3 S0")


if __name__ == "__main__":

    try:
        grbl = GRBLComms(PORT, BAUD_RATE)
        grbl.connect()

        grbl.homeMachine()
        grbl.setZOff()
        # grbl.moveMachine(100,270)
        # time.sleep(60)
        grbl.moveMachine(518, 518)

        # for i in range(100):
        #     grbl.ZaxisRoutine()
        #     print(grbl.state)
        # grbl.moveMachine(590,590)
        
        

        grbl.disconnect()

    except KeyboardInterrupt:
        grbl.disconnect()
