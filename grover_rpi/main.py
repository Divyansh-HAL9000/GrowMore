import requests
import time
import numpy as np
from firebase import firebase
import serial


serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1)
time_to_sleep = 0.5

# structure of parameter {"name":{"lower_lim":ll, "upper_lim":ul, "unit":"unt", "rounding_factor":rf]}
def is_valid(d: dict):
    if len(d.keys()) == 3:
        if "T" in d.keys() and "B" in d.keys() and "H" in d.keys():
            return True

    return False


class Grover:
    def __init__(self, params):
        self.payload = dict()
        self.params = params

    def get_values(self):
        for key in self.params.keys():
            val = np.random.uniform(self.params[key]["lower_lim"], self.params[key]["upper_lim"])
            val = round(val, self.params[key]["rounding_factor"])
            self.payload[key] = str(val) + " " + self.params[key]["unit"]
        return self.payload


tomato_ranges = {"Temperature": {"lower_lim": 10, "upper_lim": 25, "unit": "\xB0C", "rounding_factor": 2},
                 "Pressure": {"lower_lim": 0.9, "upper_lim": 1.15, "unit": "Bar", "rounding_factor": 4},
                 "Humidity": {"lower_lim": 50, "upper_lim": 70, "unit": "%", "rounding_factor": 2},
                 "pH": {"lower_lim": 5.5, "upper_lim": 6.8, "unit": "", "rounding_factor": 1},
                 "Brightness": {"lower_lim": 1390, "upper_lim": 1410, "unit": "Lumen", "rounding_factor": 2},
                 }
grover_tomato = Grover(tomato_ranges)
init = False
name = "-MXX-vyI7qd0M2VMQ0Ce"

if __name__ == "__main__":
    firebase = firebase.FirebaseApplication('https://igrow-ac1d6-default-rtdb.firebaseio.com/', None)

    if init:
        payload = grover_tomato.get_values()
        payload["time"] = time.time()
        print("sernding request : ", payload)
        result = firebase.post("/igrow-ac1d6-default-rtdb/Sensor_Value", payload)
        print(result)
        name = result["name"]
        time.sleep(time_to_sleep)

    prev_data = None
    while True:
        generate = False
        serialPort.write(b"")
#        data = serialPort.read(30)
        data = serialPort.readline()
        print(data)
        try:
            data = eval(data.decode('ascii'))
            if not is_valid(data):
                generate = True
        except:
            data = prev_data
            continue

        prev_data = data
        print(data)
        payload = grover_tomato.get_values()
        if not generate:
            payload["Temperature"] = data["T"] + tomato_ranges["Temperature"]["unit"]
            payload["Humidity"] = data["H"] + tomato_ranges["Humidity"]["unit"]
            payload["Brightness"] = data["B"] + " " + tomato_ranges["Brightness"]["unit"]
        payload["time"] = str(time.time())
#        resp = requests.post("http://127.0.0.1:8000/sensor_vals_input/", json=payload)
        print("sernding request : ", payload)
#        resp = requests.get("http://127.0.0.1:8000/atmosphere_regulation/")
#        print(resp.json())
        for key in payload.keys():
            try:
                result = firebase.put("/igrow-ac1d6-default-rtdb/Sensor_Value/"+name, key, payload[key])
            except requests.exceptions.ConnectionError:
                print("connection failed, will try again")
                continue
        print(result)
        time.sleep(time_to_sleep)


