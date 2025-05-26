# THIS MODULE WILL BE STRICLTY FOR NMAP AND ITS LIBARY  FOR NETVULN 2.0


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress_bar import ProgressBar
from rich.console import Console
console = Console()
import pyfiglet


# NETWORK IMPORTS
import socket, nmap, ipaddress
from scapy.all import IP, TCP, ICMP, srp, sr1, sniff, conf, sr1flood, srflood, sr

# ETC IMPORTS
import threading, random, time
from datetime import datetime




class Nmap_PortScanner():
    """This class will be responsible for scanning and pulling information using mainly the nmap libary"""


    def __init__(self):
        pass


    def port_scanner(self):
        """This will use the nmap"""

        scanner = nmap.PortScanner()

        r = scanner.scan(hosts="192.168.1.1", ports="1-1025", arguments="-sS", timeout=300)
        r
        console.print(r)


conf.verbose = False
ip_ds = socket.gethostbyname("nsmbarii.com")
# FOR VARIABLES
on = False
packets = 0 

while True:

    ping = IP(dst=ip_ds) / ICMP() / b"ass" * 20
    response = sr1(ping, timeout=5, verbose=0)
    if on:
        time_start = time.time()
        
        time_took = time.time() - time_start


    # panel = Panel(title="Howdy", width=min(130, console.size.width - 130), subtitle= "ass")
        
    
        if response:
            if on != True:
                console.print(f"Device: {ip_ds} is online, with a ping of: {time_took:.2f} ms")
            
            print(f"Total Packets sent: {packets}", end="\r", flush=True)
            packets += 1
            on = True


        else:
            console.print(f"Device: {ip_ds} is offline")