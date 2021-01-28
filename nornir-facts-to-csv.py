from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.tasks.files import write_file
import csv
import time
from datetime import datetime

start = time.time()
# current date and time
now = datetime.now()

t = now.strftime("%H:%M:%S")
dt = now.strftime("%d/%m/%Y, %H:%M:%S")

with open('test.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["----------" + dt + "----------"])
    #writer.writerow("IP ADDRESS", "Device Name", "Serial Number", "Number of Interfaces", "Version", "Uptime", "Image")

def dev_info(task):
    r = task.run(netmiko_send_command, command_string="show version", use_genie=True)
    task.host["facts"] = r.result
    hoster = task.host['facts']['version']['hostname']
    serial = task.host['facts']['version']['chassis_sn']
    interno = task.host['facts']['version']['number_of_intfs']
    version = task.host['facts']['version']['version']
    up = task.host['facts']['version']['uptime']
    image = task.host['facts']['version']['system_image']
    with open('test.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        csvdata =(hoster, task.host.hostname, serial, interno, version, up, image)
        writer.writerow(csvdata)
def main() -> None:
    nr = InitNornir(config_file="config.yml")
    result = nr.run(task=dev_info)
    print_result(result)
    end = time.time()
    delta = end - start
    print("Time took to execute: " + str(delta))

if __name__ == "__main__":
    main()
