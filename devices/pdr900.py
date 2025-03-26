# pdr900.py
import serial

class PDR900:
    """
    Reads pressure from the PDR900 via RS-232.
    Assumes channel PR4 is connected to a pressure sensor.
    """

    def __init__(self, port='COM6', baudrate=9600, timeout=1.5):
        self.port = port
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def read_pressure(self):
        """
        Sends the PR4 command and reads back the pressure in Torr.
        Returns float or None.
        """
        try:
            cmd_string = '@253PR4?;FF'
            self.ser.write(cmd_string.encode())
            response = self.ser.readline().decode(errors='ignore').strip()

            if response.startswith('@253ACK'):
                value_str = response.replace('@253ACK', '').replace(';FF', '').strip()
                return float(value_str)
        except Exception as e:
            print(f"❌ Error reading PDR900: {e}")

        return None

    def close(self):
        self.ser.close()
