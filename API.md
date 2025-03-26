vacpack/
├── main.py              # Starts the app, GUI + device logic
├── vacpack_gui.py       # Main GUI class (QMainWindow or QWidget)
├                           Contains VacPackGUI class
├── devices/
│   ├── vacuum_pump.py   # VacuumPumpController class
│   ├── mfc.py           # MKS_MFC class (Ethernet)
│   └── pdr900.py        # PDR900 class (USB)
└── assets/