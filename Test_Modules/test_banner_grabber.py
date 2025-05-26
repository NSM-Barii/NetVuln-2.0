# UTILTIES MODULE FOR // NETVULN 2.0


# UI IMPORTS
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
console = Console()
console_width = console.size.width


# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import TCP, sr1, IP, sr, sniff, send
import smtplib, paramiko, ftplib, dns, platform

# ETC IMPORTS
import threading, time, random, requests


# FILE HANDLING
from pathlib import Path
import json



class Banner_grabber():
    """This class will house any and all external tools/libaries that will be called upon from main program logic to get certain info"""

    def __init__(self):
        pass
    

    # SOCKET METHOD
    def get_http_socket(self, target_ip: str, target_port: int):
        """This will be responsible for getting the service version // Socket Version"""
       
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                
                result = s.connect_ex((target_ip, target_port))
                if result == 0:

                    # CREATE AND SEND A HEADER REQUEST
                    payload = b"HEAD HTTP/1.0\r\n\r\n"
                    s.send(payload)
                    version = s.recv(1024).decode().strip()
                
                else:
                   version = "N/A"
        
        except Exception as e:
            console.print(e)
        
        finally:
            return version if version else "N/A"
    
    def get_http_request(self, target_ip: str, target_port:int = 80, table = None):
        """This will be responsible for getting the service version // Requests Version"""
        

        # CREATE THE URL TO THEN QUERY
        url = f"http://{target_ip}"
        banner_info = []
        

        # ATTEMPT TO PERFORM A CONNECTION TO GRAB BANNER AND MAYBE SOME MORE INFO
        try:
            
            # ATTEMPT CONNECTION
            response = requests.get(url, timeout=2, verify=False)

            # PARSE INFO
            for hddr, value in response.headers.items():

                # FOR MODULE TESTING
                if table:

                    if hddr.lower() == "Server":
                        console.print(f"Server: {hddr} --> {value}")
                    table.add_row(f"{hddr} -->  {value} ")

                else:
                    
                    if hddr.lower().strip() == "server":
                        server = value

                    else:
                        info_format = f"{hddr} --> {value}"
                        banner_info.append(info_format)

        
        except (requests.ConnectionError, requests.JSONDecodeError)as e:
            console.print(f"[bold red]Request Error: [/bold red][yellow]{e}[/yellow]")
        
        except Exception as e:
            console.print(f"[bold red]Exception Error: [/bold red][yellow]{e}[/yellow]")
        

        # RETURN VALUES TO THE USER
        finally:
            
            server = server if server else "N/A" 
            banner_info = banner_info if banner_info else "N/A"

            return server, banner_info
    

    def get_ftp(self, target_ip: str, target_port: int = 21):
        """This method will be use to pull the banner for telnet connections"""


        try:

            banner = "N/A"

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)

                result = s.connect_ex((target_ip, target_port))

                if result == 0:

                    banner = s.recv(1024).decode().strip()
                
                else:

                    console.print("closed")

        except Exception as e:
            console.print(e)            
        
        
        finally:
            return banner 
        

    def get_smtp(self, target_ip: str, target_port: int = 25):
        """This will be responsible for getting smtp banner info"""

        banner = "N/A"

        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.bind(("192.168.1.92", 3003))

                result = s.connect_ex((target_ip, target_port))

                if result == 0:
                    console.print("open")
                  #  s.sendall(b'\r\n')
                    s.sendall(b"HEAD HTTP/1.1\r\n\r\n")

                    banner = s.recv(1024).decode(errors="ignore").strip()

        except (socket.gaierror) as e:
            console.print(f"[bold red]Socket Error: [/bold red][yellow]{e}[/yellow]")        
        
        except Exception as e:
            console.print(f"[bold red]Exception Error: [/bold red][yellow]{e}[/yellow]")
        
        finally:

            return banner


class Port_connection():
    """This class will house methods that will allow us as the user to connect said port"""

    def __init__(self):
        pass


    def get_ftp(self, target_ip: str, target_port: int = 21):
        """This will be used to connect to ftp"""


        server = "N/A"

        # GET INFO FOR TELNET USING THE TELNET LIBARY LOL 
        try:
            with ftplib.FTP() as f:

                f.connect(host=target_ip, port=target_port, timeout=3)
                server = f.getwelcome()
                f.quit()

        
        except Exception as e:
            console.print(e)


        return server if server else "N/A"
   



use = 4


# FOR MODULE TESTING
if __name__ == "__main__":

    
    # HTTP TESTING
    if use == 1:

        table = Table(title="HTTP INFO", style="bold purple", title_style="bold red", width=min(130, console_width))
        table.add_column("Port", style= "bold blue")
        table.add_column("Service", style="bold green")
        table.add_column("Version")
        table.add_column("Banner info", style="bold red")
        

        target = f"192.168.1.1"
        port = 80
        server, banner_info = Banner_grabber().get_http_request(target_ip=target)

        banner_info = '\n'.join(banner_info)

        table.add_row(f"{port}", "http", f"{server}", f"{banner_info}")

        console.print(table)
    
    
    # FTP TESTING
    elif use == 2:

        target = "212.229.82.136"

        base_dir = Path.home() / "Documents" / "nsm tools" /  "network tools" / "random ip scanner" /"multi_script"
        file_path = base_dir / "active_ip_list.txt"


        server = Banner_grabber().get_ftp(target_ip=target)
        
        console.print(server)
   

    # FTP CONNECTION TESTING 
    elif use == 3:
      
        target = "198.12.124.36"
        
        while True:
            target = input("enter: ")
            Banner_grabber().get_ftp(target_ip=target, target_port=80)
    

    elif use == 4:

        target = "192.168.1.199"
        ports = [21, 22, 23, 25, 53, 80, 143, 563, 587, 110]

        for port in ports:
            banner = Banner_grabber().get_smtp(target_ip=target, target_port=port)
            
            console.print(banner)
            console.print("\n-----------------\n")
            



