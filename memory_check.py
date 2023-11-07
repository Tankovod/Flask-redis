import subprocess
from time import sleep
import requests
from src.settings import ALARM_MEMORY_VALUE


while ...:
    sleep(10)
    system_data = subprocess.check_output(("top", "-b", "-n", "1"), text=True)
    used_memory = int(system_data.split("Mem:")[1].split("K used")[0])

    if used_memory > ALARM_MEMORY_VALUE:
        requests.post("http://127.0.0.1:8080/api/v1/memory-alarm", json={"used_memory": used_memory,
                                                                         "alarm_memory_value": ALARM_MEMORY_VALUE})
        sleep(300)
