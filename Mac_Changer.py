#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for new ")
    parser.add_option("-m", "--new_mac", dest="new_mac", help ="Enter your mac_address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("enter the interface or --help")
    elif not options.new_mac:
        parser.error("enter the mac add or --help")
    return options


# the above function will give us 'eth0' and Mac address' as options


def change_mac(interface, new_mac):
    print("[+]changing mac address")
    subprocess.call(["ifconfig", interface, "down"]) # [] is more secure format,for eg:wlan0,ls cannot be writtten
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# the inputs 'eth0 and mac address' will be called later on using this function

def get_current_macaddress(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # Do not forget to use use '[]' in the above statement
    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search:
        return mac_address_search.group(0)
    else:
        print("[-]could not read mac address")


options = get_arguments()

current_mac = get_current_macaddress(options.interface)
print("the mac address was : ", current_mac)
change_mac(options.interface, options.new_mac)
current_mac = get_current_macaddress(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address was changed successfully to : " + str(current_mac))
    # added str to return None for lo which doesnot have mac add
else:
    print("[-] MAC Address did not change")
