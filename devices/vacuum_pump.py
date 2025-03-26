# vacuum_pump.py
import serial

class VacuumPumpController:
    def __init__(self, port="COM8", baudrate=9600, timeout=1):
        self.port = port
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        except serial.SerialException as e:
            print(f"❌ Could not open Vacuum Pump serial port: {e}")
            self.ser = None
        self.is_on = False

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def toggle_pump(self):
        if not self.is_connected():
            raise ConnectionError("Pump serial connection lost")

        cmd = b"pumpOn\n" if not self.is_on else b"pumpOff\n"
        try:
            self.ser.write(cmd)
        except Exception as e:
            print(f"❌ Error writing to pump: {e}")

    def read_status(self):
        if not self.is_connected():
            return False

        try:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode().strip()
                if response == "pumpOn":
                    self.is_on = True
                elif response == "pumpOff":
                    self.is_on = False
        except Exception as e:
            print(f"❌ Error reading pump status: {e}")
        return self.is_on

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
