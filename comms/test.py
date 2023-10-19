import serial
import time

PORT = "COM9"
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
    
    def waitForMovementCompletion(self):
        time.sleep(1)
        idleCounter = 0

        while True:
            self.connection.reset_input_buffer()
            
            self.sendCommand('?')
            response = self.connection.readline().strip().decode()

            if response != 'ok':
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
        self.waitForMovementCompletion()

    def moveMachine(self, x, y):
        print(f'Moving machine to X:{x}, Y:{y}')

        grbl.sendCommand(f'G00 X{x} Y{y}')

        self.waitForMovementCompletion()
        
        print(f'reached X:{x} Y:{y}')
        return True

    def goToDropOff(self):
        self.moveMachine(250, 15)
            
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


if __name__ == "__main__":

    try:
        grbl = GRBLComms(PORT, BAUD_RATE)
        grbl.connect()

        # grbl.homeMachine()
        grbl.moveMachine(50, 50)

        for i in range(100):
            grbl.ZaxisRoutine()
            print(grbl.state)

        grbl.disconnect()

    except KeyboardInterrupt:
        grbl.disconnect()
