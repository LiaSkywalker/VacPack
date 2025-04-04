from PyQt5.QtCore import QThread, pyqtSignal

class DataReaderThread(QThread):
    data_updated = pyqtSignal(float, float, float)  # flow, mfc_pressure, pdr900_pressure

    def __init__(self, mfc, pdr900):
        super().__init__()
        self.mfc = mfc
        self.pdr900 = pdr900
        self._running = True

    def run(self):
        import time
        while self._running:
            try:
                flow = self.mfc.get_flow_rate() if self.mfc else 0.0
                mfc_pressure = self.mfc.get_pressure() if self.mfc else 0.0
                pdr_pressure = self.pdr900.read_pressure() if self.pdr900 else 0.0
                if pdr_pressure is None:
                    pdr_pressure = 0.0
            except Exception as e:
                print("❌ Error in DataReaderThread:", e)
                flow, mfc_pressure, pdr_pressure = 0.0, 0.0, 0.0

            self.data_updated.emit(flow, mfc_pressure, pdr_pressure)
            time.sleep(1)

    def stop(self):
        self._running = False
        self.quit()
        self.wait()
