import re
import subprocess
import sys
import usb.core
import serial.tools.list_ports


def method1():
    device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)

    print(devices)

def method2():
    # !/usr/bin/python
    # find USB devices
    dev = usb.core.find(find_all=True)
    # loop through devices, printing vendor and product ids in decimal and hex
    for cfg in dev:
        sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
        sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')

def method3():
    # find our device
    dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

    assert ep is not None

    # write the data
    ep.write('test')

def method4():
    class find_class(object):
        def __init__(self, class_):
            self._class = class_
        def __call__(self, device):
            # first, let's check the device
            if device.bDeviceClass == self._class:
                return True
            # ok, transverse all devices to find an
            # interface that matches our class
            for cfg in device:
                # find_descriptor: what's it?
                intf = usb.util.find_descriptor(
                                            cfg,
                                            bInterfaceClass=self._class
                                    )
                if intf is not None:
                    return True

            return False

    printers = usb.core.find(find_all=1, custom_match=find_class(2))
    print(printers)

def method5():
    busses = usb.busses()
    for bus in busses:
        devices = bus.devices
        for dev in devices:
            repr(dev)
            print("Device:", dev.filename)
            print("  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor))
            print("  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct))
            print("Manufacturer:", dev.iManufacturer)
            print("Serial:", dev.iSerialNumber)
            print("Product:", dev.iProduct)


def method6():
    # Find all USB devices
    devices = usb.core.find(find_all=True)

    if devices is None:
        print("No USB devices found.")
        return

    print("List of connected USB devices:")
    for device in devices:
        print(device)

def find_ports():
    ports = serial.tools.list_ports.comports()
    max = len(ports)
    # print(max,' ports found')

    for port in ports:
        if port.description == "FT232R USB UART - FT232R USB UART":
            #print('Found Reyax')
            reyax_port = port.device
        elif port.description == "VE Direct cable - VE Direct cable":
            #print('Found Charge Controller')
            charge_port = port.device
        else:
            print('Found Random Shit')
    try:
        return reyax_port, charge_port
    except UnboundLocalError:
        print('Did not find both ports')



if __name__ == '__main__':
    #method1()
    #method2()
    #method3()
    #method4()
    #method5()
    #method6()
    find_ports()
