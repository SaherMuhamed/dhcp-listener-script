import scapy.all as scapy
import datetime as dt
import sys

if sys.version_info < (3, 0):
    sys.stderr.write("\nYou need python 3.0 or later to run this script\n")
    sys.stderr.write(
        "Please update and make sure you use the command python3 dhcp_listener.py\n\n")
    sys.exit(0)


def sniff():
    """function to start sniff packets and filtering them using Berkeley Packet Filter (BPF) syntax
    https://biot.com/capstats/bpf.html"""
    scapy.sniff(store=False, prn=process_sniffed_packet, filter='udp and (port 67 or port 68)')


def process_sniffed_packet(packet):
    device_mac, requested_ip, hostname, vendor_id = [None] * 4
    if packet.haslayer(scapy.Ether):
        device_mac = packet.getlayer(scapy.Ether).src

    dhcp_options = packet[scapy.DHCP].options  # get the options from DHCP layer

    for item in dhcp_options:
        try:
            key, value = item  # because it returns tuple with 2 values
        except ValueError:
            continue

        if key == 'requested_addr':
            requested_ip = value  # get the requested IP
        elif key == 'hostname':
            hostname = value.decode()  # get the hostname of the device
        elif key == 'vendor_class_id':
            vendor_id = value.decode()  # get the vendor ID

    if device_mac and vendor_id and hostname and requested_ip:
        print(f"[{str(dt.datetime.now().strftime('%H:%M:%S'))}] - {hostname} / {vendor_id} requested {requested_ip} at {device_mac}")


if __name__ == "__main__":
    sniff()
