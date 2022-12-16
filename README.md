# Assingments

Python script for getting data from 2 Energy power meters via Modbus TCP and 2 Tuya IAQ Sensors and recording to CrateDB.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pymodbus.

```bash
pip install foobar
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install tuya-connector-python.

```bash
pip install tuya-connector-python
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install crate.

```bash
pip install crate
```

## Usage
You can change the parameter of device to connect in this function
```python
def task():
    iaq_1 = tuyu_reader("vdevo167078400790145")["result"][1]["value"]/10
    iaq_2 = tuyu_reader("vdevo167078400323929")["result"][0]["value"]/10
    powermeter_1 = modbus_reader("192.168.2.1", 1, 1048)/10
    powermeter_2 = modbus_reader("192.168.2.1", 1, 1048)/10
    cratedb_writer(iaq_1, iaq_2, powermeter_1, powermeter_2)
```
![alt text](https://sv1.picz.in.th/images/2022/12/16/GMyqnR.png)
