#!/usr/bin/env python
import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an target, use --help for more info")
    return options


def scan(ip):
    print("\n[+] Scanning network for " + ip)
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_results(result_list):
    print("\nIP\t\t\tMAC Address\n-----------------------------------------------")
    for client in result_list:
        print(client["ip"]+"\t\t"+client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_results(scan_result)
