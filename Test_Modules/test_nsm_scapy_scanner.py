# THIS IS THE BEGINNING OF SOMETHING GREAT, SOMETHING SPECTACULAR, SOMETHING THAT WILL BLOW YOUR FUCKING SOCKS OFF...
# INTRODUCING NETVULN 2.0... THE LATTER BETTER VERSION OF NETVULN 1.0


# UI IMPORTS
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
console = Console()


# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import TCP, sr1, IP, sr, sniff, send


# ETC IMPORTS
import threading, time, random, requests


# FILE HANDLING
from pathlib import Path
import json



class Port_Scanner():
    """This class will be responsible for scanning TCP ports, using a variety of flags this will be NetVuln 2.0"""


    def __init__(self, target = "192.168.1.1"):
        self.target = target
        self.lock = threading.Lock()
        pass


    def spoofed_source_ip(self): 
        """This will return a random source ip that will be used for spoofing or hiding the actual source ip"""
        

        # CREATE THE SPOOFED IP THAT WILL THEN BE RETURNED
        spoofed_ip = (f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
        return spoofed_ip
    
    def spoofed_source_port(self):
        """Like the previous method this will be responsible for spoofing/hiding the source port"""

        
        # CREATE THE SPOOFED PORT THAT WILL BE RETURNED
        spoofed_port = (f"{random.randint(1050,65535)}")
        return spoofed_port
    
    
   # def sniff_packet(self, pkt):
        """This method will be used along with spoofed IP and source port to get the response that was returned to that IP"""

       # console.print(pkt.summary())


    def port_scanner(self, port):
        """This method will be responsible for scanning the IP for open ports"""

        ip = "192.168.1.1"
        dport = [80, 25, 21, 443, 53, 22]

        # GET OUR SPOOFED SPORT AND SRCIP
        source_ip = self.spoofed_source_ip()
        source_port = int(self.spoofed_source_port())



        
        
        try:

            # CRAFT AND SEND THE PACKET
            #with self.lock:
            syn_packet = IP(dst=self.target) / TCP(dport=port, sport=source_port, flags="S")
            response = sr1(syn_packet, timeout=1, verbose=0)
            
            #console.print("hii")


            # IF THE PORT IS OPEN
            if response and response.haslayer("TCP") and response[TCP].flags == 0x12:
                
                # ACK RESPONSE
                ack_packet = IP(dst=self.target) / TCP(dport=port, sport=source_port, flags="A")  #send(ack_packet, verbose=0)
                
                # PARSE THE PACKET SUMMARY TO GET THE SERVICE THAT IS BEING RAN    // service = response.summary().split('/')[1].split('>')[0].partition(':')[2]
                service = response.sprintf("%TCP.sport%")
                sum = (response.summary())
                version = "N/A"

                use = True
            
                # CREATE A SOCKET CONNECTION TO GET BANNER
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    #console.print(self.target, port)
                    
                    if use:
                        # PERFORM BANNER GRAB
                        response = s.connect_ex((str(self.target), int(port)))
                        if response == 0:
                            s.send(b"HEAD /HTTP/1.0\r\n\r\n")
                            version = s.recv(1024).decode().strip()
                        else:
                            version = "N/A"

                console.print(f"{port} --> {service} --> {version}  /  Packet Summary: {sum}")
        
        except Exception as e:
            console.print(e)
        
    
    def threader(self):
        """This will be used to implement a faster way of port scanning"""

        ports = range(1, 1025)
        threads = []
        
        try:

            for port in ports:

                t = threading.Thread(target=self.port_scanner, args=(port,), daemon=True)
                threads.append(t)
                console.print("starting on", port)
            
            for thread in threads:
                thread.start()
                
            for thread in threads:
                thread.join()
        
        except Exception as e:
            console.print(e)



ip = socket.gethostbyname("google.com")
console.print(ip)
ip = "192.168.1.38"
p = Port_Scanner(target=ip)

p.threader()