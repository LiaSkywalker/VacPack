# VacPack: Vacuum and Gas Flow Lab Controller

A Python-based desktop application to control and monitor:
- ✅ Mass Flow Controller (MFC) over Ethernet
- ✅ Pressure Gauge (MKS PDR900) over Serial
- ✅ Vacuum Pump (via Arduino over USB)

---

## 🔧 Features

- 📉 Real-time plotting of MFC flow and pressure
- 🧪 Live pressure display from PDR900
- 🟢 Vacuum pump control with state indicator
- 🚨 Emergency stop & safety handling
- 💻 One-click desktop app (`.exe`) for Windows

---

## 📦 Folder Structure

| Folder/File          | Description                                      |
|----------------------|--------------------------------------------------|
| `main.py`            | Application entry point                          |
| `vacpack_gui.py`     | Main GUI layout and logic                        |
| `build.bat`          | One-click build script for Windows `.exe`        |
| `vacpack.ico`        | Custom desktop icon                              |
| `README.md`          | Project documentation                            |
| `requirements.txt`   | Python dependencies                              |
| `LICENSE`            | MIT license or your chosen license               |
| `devices/`           | Drivers and interfaces for MFC, PDR900, pump     |
| `utils/`             | Optional helpers like `system_initializer.py`    |
| `DataReaderThread.py`| Background thread for real-time device polling   |

---

## 📥 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
