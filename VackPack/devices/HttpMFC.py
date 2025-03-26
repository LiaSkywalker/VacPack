# http_mfc.py
import requests
import re


class HttpMFC:
    """
    Connects to an MKS Mass Flow Controller over HTTP.
    Parses flow and pressure data from the mfc.js endpoint.
    """

    def __init__(self, url: str):
        self.url = url
        self.last_response_text = None

    def is_connected(self):
        try:
            r = requests.get(self.url, timeout=1)
            return r.status_code == 200
        except Exception:
            return False

    def connect(self) -> bool:
        """
        Tests the connection to the MFC.
        Returns True if successful.
        """
        try:
            response = requests.get(self.url, timeout=2)
            response.raise_for_status()
            self.last_response_text = response.text
            return True
        except requests.RequestException as e:
            print(f"[HttpMFC] Connection failed: {e}")
            return False

    def fetch_data(self) -> str:
        """
        Retrieves the latest raw mfc.js data.
        """
        try:
            response = requests.get(self.url, timeout=2)
            response.raise_for_status()
            self.last_response_text = response.text
            return response.text
        except requests.RequestException as e:
            print(f"[HttpMFC] Failed to fetch data: {e}")
            return None

    def get_flow_rate(self) -> float:
        """
        Extracts and returns the flow rate in sccm.
        """
        text = self.fetch_data()
        if text:
            match = re.search(r"mfc\.flow_value\s*=\s*([\d\.]+);", text)
            if match:
                return float(match.group(1))
        return 0.0

    def get_pressure(self) -> float:
        """
        Extracts and returns pressure in Torr.
        """
        text = self.last_response_text or self.fetch_data()
        if text:
            match = re.search(r"mfc\.pressure_value\s*=\s*([\d\.]+);", text)
            if match:
                return float(match.group(1))
        return 0.0

    def get_pressure_mbar(self) -> float:
        """
        Returns the last pressure reading in mbar.
        """
        torr = self.get_pressure()
        return torr * 1.333
