# vacpack_gui.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QRadioButton,
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
import numpy as np
import time
from devices.HttpMFC import HttpMFC
from devices.pdr900 import PDR900
from devices.vacuum_pump import VacuumPumpController
from DataReaderThread import DataReaderThread

class VacPackGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VacPack: Lab Device Control")
        self.resize(1200, 800)

        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        self.init_ui()
        self.apply_styles()

        # Dummy data buffer
        self.t0 = time.time()
        self.x_data = []
        self.flow_data = []
        self.pressure_data = []

        self.mfc = HttpMFC("http://192.168.2.155/mfc.js")
        if self.mfc.connect():
            print("✅ MFC connected")
        else:
            print("❌ MFC connection failed")

        self.pdr900 = PDR900(port='COM6')  # Update port if needed
        self.pdr900_data = []

        self.pump = VacuumPumpController(port="COM8")
        self.setup_pump_timer()

        # Start thread to read data
        self.reader_thread = DataReaderThread(self.mfc, self.pdr900)
        self.reader_thread.data_updated.connect(self.update_data)
        self.reader_thread.start()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        # ========== TOP ROW ==========
        top_layout = QHBoxLayout()

        # -------- Left: Pump + Pressure Gauge --------
        left_column = QVBoxLayout()

        self.pump_status_label = QLabel("Status: Unknown")
        self.pump_toggle_button = QPushButton("Toggle Pump")
        self.pump_toggle_button.setFixedWidth(150)

        pump_layout = QVBoxLayout()
        pump_layout.addWidget(self.pump_status_label, alignment=Qt.AlignCenter)
        pump_layout.addWidget(self.pump_toggle_button, alignment=Qt.AlignCenter)

        pump_group = QGroupBox("Vacuum Pump")
        pump_group.setLayout(pump_layout)
        left_column.addWidget(pump_group)

        self.pressure_display = QLineEdit()
        self.pressure_display.setReadOnly(True)

        gauge_layout = QVBoxLayout()
        gauge_layout.addWidget(QLabel("Current Pressure:"), alignment=Qt.AlignCenter)
        gauge_layout.addWidget(self.pressure_display)

        gauge_group = QGroupBox("Pressure Gauge")
        gauge_group.setLayout(gauge_layout)
        left_column.addWidget(gauge_group)

        top_layout.addLayout(left_column, 1)

        # -------- Center: MFC Measurements --------
        self.flow_rate_display = QLineEdit()
        self.flow_rate_display.setReadOnly(True)
        self.pressure_torr_display = QLineEdit()
        self.pressure_torr_display.setReadOnly(True)
        self.pressure_mbar_display = QLineEdit()
        self.pressure_mbar_display.setReadOnly(True)

        measurements_layout = QGridLayout()
        measurements_layout.addWidget(QLabel("Flow rate:"), 0, 0)
        measurements_layout.addWidget(self.flow_rate_display, 0, 1)
        measurements_layout.addWidget(QLabel("sccm"), 0, 2)

        measurements_layout.addWidget(QLabel("Pressure (torr):"), 1, 0)
        measurements_layout.addWidget(self.pressure_torr_display, 1, 1)
        measurements_layout.addWidget(QLabel("torr"), 1, 2)

        measurements_layout.addWidget(QLabel("Pressure (mbar):"), 2, 0)
        measurements_layout.addWidget(self.pressure_mbar_display, 2, 1)
        measurements_layout.addWidget(QLabel("mbar"), 2, 2)

        measurements_group = QGroupBox("Measurements")
        measurements_group.setLayout(measurements_layout)
        top_layout.addWidget(measurements_group, 1)

        # -------- Right: Control + Valve --------
        right_column = QVBoxLayout()

        self.target_pressure_input = QLineEdit()
        self.set_pressure_button = QPushButton("Set Pressure")
        self.set_pressure_button.setFixedWidth(150)
        self.gas_type_combo = QComboBox()
        self.gas_type_combo.addItems(["Nitrogen", "Argon", "Helium", "CO2", "Oxygen"])

        control_layout = QVBoxLayout()
        control_layout.addWidget(QLabel("Set Target pressure (torr):"))
        control_layout.addWidget(self.target_pressure_input)
        control_layout.addWidget(self.set_pressure_button, alignment=Qt.AlignCenter)
        control_layout.addWidget(QLabel("Select gas type:"))
        control_layout.addWidget(self.gas_type_combo)

        control_group = QGroupBox("Control")
        control_group.setLayout(control_layout)

        self.normal_radio = QRadioButton("Normal")
        self.close_radio = QRadioButton("Close")
        self.open_radio = QRadioButton("Open")
        self.normal_radio.setChecked(True)

        valve_layout = QHBoxLayout()
        valve_layout.addWidget(self.normal_radio)
        valve_layout.addWidget(self.close_radio)
        valve_layout.addWidget(self.open_radio)

        valve_group = QGroupBox("Valve Override")
        valve_group.setLayout(valve_layout)

        right_column.addWidget(control_group)
        right_column.addWidget(valve_group)
        right_column.addStretch()

        top_layout.addLayout(right_column, 1)

        self.main_layout.addLayout(top_layout, 2)

        # ========== BOTTOM ROW (pyqtgraph) ==========
        graph_layout = QHBoxLayout()

        # Pressure graph
        self.pressure_plot = pg.PlotWidget(title="Pressure (Torr)")
        self.pressure_plot.showGrid(x=True, y=True)
        self.pressure_curve = self.pressure_plot.plot(pen='y')

        # Flow graph
        self.flow_plot = pg.PlotWidget(title="Flow Rate (sccm)")
        self.flow_plot.showGrid(x=True, y=True)
        self.flow_curve = self.flow_plot.plot(pen='c')

        graph_layout.addWidget(self.pressure_plot)
        graph_layout.addWidget(self.flow_plot)

        self.main_layout.addLayout(graph_layout, 3)
        self.setLayout(self.main_layout)

    def update_data(self, flow, mfc_pressure, pdr_pressure):
        t = time.time() - self.t0
        self.x_data.append(t)
        self.flow_data.append(flow)
        self.pressure_data.append(mfc_pressure)

        # Trim to last 60 points
        if len(self.x_data) > 60:
            self.x_data = self.x_data[-60:]
            self.flow_data = self.flow_data[-60:]
            self.pressure_data = self.pressure_data[-60:]

        # Update GUI fields (MFC)
        self.flow_rate_display.setText(f"{flow:.2f}")
        self.pressure_torr_display.setText(f"{mfc_pressure:.2f}")
        self.pressure_mbar_display.setText(f"{mfc_pressure * 1.333:.2f}")

        # Update MFC graphs
        self.flow_curve.setData(self.x_data, self.flow_data)
        self.pressure_curve.setData(self.x_data, self.pressure_data)

        # ✅ Only update PDR900 pressure box if value is valid
        if pdr_pressure is not None and pdr_pressure != 0.0:
            self.pressure_display.setText(f"{pdr_pressure:.2f} Torr")

    def setup_pump_timer(self):
        self.pump_toggle_button.clicked.connect(self.toggle_pump)

        self.pump_timer = QTimer()
        self.pump_timer.timeout.connect(self.update_pump_status)
        self.pump_timer.start(500)

    def toggle_pump(self):
        self.pump.toggle_pump()

    def update_pump_status(self):
        status = self.pump.read_status()
        if status:
            self.pump_status_label.setText("Pump is ON")
            self.pump_status_label.setStyleSheet("background-color: green; color: white; font-weight: bold;")
            self.pump_toggle_button.setText("Turn OFF Pump")
        else:
            self.pump_status_label.setText("Pump is OFF")
            self.pump_status_label.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            self.pump_toggle_button.setText("Turn ON Pump")

    def apply_styles(self):
        # Bold and larger group titles
        for group in self.findChildren(QGroupBox):
            group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 13pt; }")

        # Uniform font for labels and line edits
        for widget in self.findChildren((QLabel, QLineEdit, QPushButton, QComboBox, QRadioButton)):
            widget.setStyleSheet("font-size: 12pt;")