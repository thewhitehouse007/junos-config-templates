from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from getpass import getpass
import yaml

junos_hosts = input("Devices (array) ['vMX-1', 'vMX-2']: ")
username = input("Device username: ")
password = getpass("device password: ")
template = input("Template file: ")


for host in junos_hosts:
    filename = host
    with open(filename, 'r') as fh:
        data = yaml.load(fh)
    try:
        with Device(host=host, user=username, password=password) as dev:
            try:
                with Config(dev, mode='exclusive') as conf:
                    conf.load(template_path=template, template_vars=data, format="text")
                    conf.pdiff()
                    conf.commit()
            except LockError:
                print("The config database was locked!")
    except ConnectError:
        print("Connection error!")
