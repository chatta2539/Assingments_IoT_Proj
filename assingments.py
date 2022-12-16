from pymodbus.client import ModbusTcpClient
from tuya_connector import TuyaOpenAPI
from crate import client
import time

# Connection parameter for connect to CrateDB
connection = client.connect("http://10.0.101.116:4200/", username="crate")
cursor = connection.cursor()

#   vdevo167078400790145, vdevo167078400323929
# Creadential tuya
ACCESS_ID = "usx4njuhtkkkdaqtdnga"
ACCESS_KEY = "eac405fb79294434b5cfed4b6f0f1fb1"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Function for read Modbus TCP
#   device_ip -> input IP address of modbus device
#   device_number -> input device_number of modbus device
#   param_add -> input device_number of modbus device
def modbus_reader(device_ip, device_number, param_add):
    devices = ModbusTcpClient(device_ip, 502)
    devices.connect()
    r1 = devices.read_holding_registers(param_add, 1, unit= device_number)
    result = r1.registers[0]
    devices.close()
    return result


# Function for read tuya device from tuya cloud
# device_name -> input device_name of tuya device
def tuyu_reader(device_name):
    result = openapi.get("/v1.0/iot-03/devices/%s/status"%(device_name), dict())
    return result

# Function for write data to crateDB
def cratedb_writer(data1, data2, data3, data4):
    cursor.execute("INSERT INTO iot_sensor_demo (iaq_1, iaq_2, powermeter_1, powermeter_2) VALUES (%s, %s, %s, %s)" %(str(data1), str(data2), str(data3), str(data4)))

# Function for main task to integration all function 
def task():
    iaq_1 = tuyu_reader("vdevo167078400790145")["result"][1]["value"]/10
    iaq_2 = tuyu_reader("vdevo167078400323929")["result"][0]["value"]/10
    powermeter_1 = modbus_reader("192.168.2.1", 1, 1048)/10
    powermeter_2 = modbus_reader("192.168.2.1", 1, 1048)/10
    cratedb_writer(iaq_1, iaq_2, powermeter_1, powermeter_2)

pt_time = time.time()

while True:
    if time.time() - pt_time >= 2:
        pt_time = time.time()
        try:
            task()
        except Exception as e:
            print(e)