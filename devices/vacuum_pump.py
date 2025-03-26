# vacuum_pump.py
import serial

class VacuumPumpController:
    """
    Controls a vacuum pump via an Arduino over serial.
    Commands:
        - "pumpOn\n"  -> turns pump ON
        - "pumpOff\n" -> turns pump OFF
    Expects response: "pumpOn" or "pumpOff"
    """

    def __init__(self, port="COM8", baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.is_on = False

    def toggle_pump(self):
        if self.ser.is_open:
            cmd = b"pumpOn\n" if not self.is_on else b"pumpOff\n"
            self.ser.write(cmd)

    def read_status(self):
        if self.ser.in_waiting > 0:
            response = self.ser.readline().decode().strip()
            if response == "pumpOn":
                self.is_on = True
            elif response == "pumpOff":
                self.is_on = False
        return self.is_on

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
