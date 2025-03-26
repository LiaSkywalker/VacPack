# pdr900.py
import serial
import time

class PDR900:
    def __init__(self, port='COM6', baudrate=9600, timeout=0.2):
        self.port = port
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        except serial.SerialException as e:
            print(f"❌ Could not open PDR900 serial port: {e}")
            self.ser = None

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def read_pressure(self):
        if not self.is_connected():
            raise ConnectionError("PDR900 serial connection lost")

        try:
            self.ser.reset_input_buffer()
            self.ser.write(b'@253PR4?;FF')
            time.sleep(0.05)

            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode(errors='ignore').strip()
                if response.startswith('@253ACK'):
                    value_str = response.replace('@253ACK', '').replace(';FF', '').strip()
                    return float(value_str)
        except Exception as e:
            print(f"❌ Error reading PDR900: {e}")

        return None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
