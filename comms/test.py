import serial
import time

PORT = "COM8"
BAUD_RATE = 115200

class GRBLComms:
    def __init__(self, port, baudRate):
        self.port = port
        self.baudRate = baudRate
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudRate)
        self.wakeupMachine()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def sendCommand(self, command):
        if not self.connection:
            raise Exception("GRBL is not connected!")
        
        self.connection.write(f"{command}\r\n".encode())
        message = ""
        while self.connection.inWaiting():
            message += self.connection.readline().decode()
        return message

    def homeMachine(self):
        self.sendCommand("$H")

    def moveMachine(self, x, y):
        print(f'Moving machine to X:{x}, Y:{y}')

        grbl.sendCommand(f'G00 X{x} Y{y}')
        idleCounter = 0

        while True:
            # TODO: add error handling and return False
            # if machine does not reach desired location by chance
            grbl.connection.reset_input_buffer()
            response = grbl.sendCommand("?")
            
            print(f'Moving to X:{x} Y:{y}')
            print(idleCounter)
            # print(response)

            if response != 'ok':
                if 'Idle' in response:
                    # machine has reached desired location
                    idleCounter += 1

                if idleCounter >= 10:
                    # count no of times machine reported to be idle
                    break
        
        print(f'reached X:{x} Y:{y}')
        return True

    def goToDropOff(self):
        self.moveMachine(250, 0)
            
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
        pass


if __name__ == "__main__":
    grbl = GRBLComms(PORT, BAUD_RATE)
    grbl.connect()

    grbl.homeMachine()
    grbl.moveMachine(250, 50)
    time.sleep(1)
    grbl.goToDropOff()

    
    grbl.disconnect()
