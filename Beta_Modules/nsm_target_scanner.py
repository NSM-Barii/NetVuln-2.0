# THIS WILL HOLD THE LOGIC FOR NETVULN 2.0 // WILL BE ADDING IN LOTS OF NEW FEATURES


# UI IMPORTS
import dns.exception
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
import pyfiglet


# NETWORK IMPORTS
import socket, ipaddress, dns.resolver, nmap


# ETC IMPORTS
from html.parser import HTMLParser
import threading, time, random, requests, subprocess
from concurrent.futures import ThreadPoolExecutor



# NSM IMPORTS
from nsm_utilities import Utilities, File_Handler, NetTilities
from nsm_directory_scanner import Requests_Directory_Scanner
from nsm_vulnerability_scanner import Nmap_Vulnerability_Scanner



# CONSTANTS & GLOBALS
console = Console()
terminal_width = console.size.width


# FILE HANDLING
from pathlib import Path
import json


    # BASE DIR
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0"
base_dir.mkdir(parents=True, exist_ok=True)




# LETS START WITH A SOCKET SCANNER

class Socket_Port_Scanner():
    """This class will be responsible for performing a TCP port scan on the target device"""

    num = ""
    scans = {}


    class Sub_Utilities():
        """This will be a subclass set inside a class used for utilities"""


        # GLOBAL VARIABLES // WILL BE CHANGED FROM MODULE CONTROLLER // MUST CALL UPON Module_Controller.get_ip_domain() <-- to get ip & domain
        ip = ""
        domain = ""
        create_sec = False



        def __init__(self):
            pass


        @staticmethod
        def get_valid_ip():
            """This method will be responsible for returning a valid ip that can be used by the program"""


            # SET VARIABLE
            error = False
            

            # LOOP FOR EXCEPTIONS
            while True:

                try:

                    print("\n")

                    if error:
                        console.print(error)
                        error = False
                    
                    target = console.input("[bold red]Enter Domain or IP Address: ")

                    ip = socket.gethostbyname(target)
                    valid_ip = ipaddress.ip_address(ip)


                    return str(valid_ip) 

                

                except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
                    console.print(e)

                
                except socket.error as e:
                    console.print(f"[bold red]Socker Error:[yellow] {e}")
                    error = f"{target}[bold red] is not a valid target:[yellow] PLEASE TRY THE FUCK AGAIN !!!"

                
                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")


        @staticmethod
        def get_service(port) -> str:
            """This method will be used to get the service used by the port"""


            # MAP KNOWN SERVICES // FOR FALL BACK ERRORS
            known_ports = {
                465: "smtp?",
                587: "smtp?",
                2053: "cloudflare?",
                2082: "cPanel?",
                2083: "cPanel?",
                2086: "whm?",
                2087: "whm?",
                2052: "clearVisn Services?",
                2095: "cPanel Webmail?",
                2096: "cPanel Webmail?",
                2087: "cPanel whm?",
                8080: "Http Alternative?",
                8443: "Https Alternative?",
                8880: "Http Alternative?"
            }
        

            
            # GET THE SERVICE RUNNING ON THE PORT
            try:

                service = socket.getservbyport(port)
            

            except OSError as e:
                #console.print(f"[bold red]OSError Error:[yellow] {e}")
                service = known_ports.get(port, "N/A?")
            

            except Exception as e:
                console.print(f"[bold red]Service Exception Error:[yellow] {e}")

            
            finally:
                return service

        
        
        @classmethod
        def get_service_version_socket(cls, port):
            """This method will be using the scapy libary to findout the service version"""


            # DEBUGGING
            verbose = False

            
            # TARGET CHECK
            target = cls.ip

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                
                try:
                    s.settimeout(3)
                    response = s.connect_ex((target, port))

                    # SEND A HTTP HEADER REQUEST
                    if response == 0:
                        s.send(b"HEAD /HTTP/1.0\r\n\r\n")
                        version = s.recv(1024).decode().strip()


                        # PARSE INFO
                       # parser = HTMLParser
                        #parsed_info = parser.handle_data(data=version)

                        

                        return [version, version]
                    
                    return ["N/A", "N/A"]
                


                #except HTMLParser.

                

                except Exception as e:
                    if verbose:
                        console.print(f"[bold red]Exception Error:[yellow] {e}")

                    # RETURN N/A VERSION
                    return ["N/A", "N/A"]
        

        @classmethod
        def get_service_version_request(cls, port):
            """This method will be using the request libary to findout the service version"""


            # DEBUGGING
            verbose = False
            go = True

            
            # STORE DATA
            data = {}
            dataa = []


            # TARGET CHECK // CRAFT URL
            if cls.domain:
                url = f"https://{cls.domain}"
            
            else:
                url = f"https://{cls.ip}:{port}"
            
            
            if verbose:
                console.print(url)
            

            # LOOP IN CASE OF 429 // RATE LIMITING
            while go:
                try:

                    # MAKE THE REQUEST
                    response = requests.get(url=url, timeout=3, allow_redirects=True)
                    

                    if response.status_code in [200,204]:

                        # GET INFO FROM HEADERS
                        headers = response.headers
                        valid = [
                            "server", "x-powered-by", "strict-transport-security", 
                            "content-security-policy", "x-frame-options", "x-content-type-options",
                            "x-xss-protection", "set-cookie"
                            ]

                        
                        # GET HEADERS AND PARSE THAT MOTHER FUCKERRR
                        headers = response.headers
                        
                        for key, value in headers.items():


                            # LOWER FOR BETTER PARSING
                            key = key.lower().strip()

                            if key.lower() in valid:

                                data[key] = value
                        

                        # NOW FOR ETC INFO
                        # for key, value in headers.items():
                        #   data[key.lower()] = value
                        

                        # CONTROL DATA CHAR LENGTH
                        if len(data.get("content-security-policy", "")) > 50:
                            data["content-security-policy"] = "Max Chars / To many chars given from site"
                        

                        if len(data.get('set-cookie', "") ) > 500:
                            data['set-cookie'] = "Max Chars / To many chars given from site"

                        
                        # GET VARS
                        server = data.get("server", "Not found")
                        x_powered_by = data.get("x-powered-by", "Not found")
                        x_xss_protection = data.get("x-xss-protection", "Not Found")
                        strict_transport_security = data.get("strict-transport-security", "Missing")
                        content_security_policy = data.get("content-security-policy", "Missing")
                        

                        
                        # FORMAT DATA
                        dataa = [
                            (f"Server: {server}"),
                            (f"x-powered-by: {x_powered_by}"),
                            (f"x-xss-protection: {x_xss_protection}")
    
                        ]
                        

                        # CREATE A SECTION
                        cls.create_sec = True 



                        # CREATE LIST
                        DATA = [f"{k}: {v}" for k,v in data.items()]                    


                        # FORMAT DATA LOOK FOR TABLE
                        dataa = (f"{dataa[0]}\n{dataa[1]}\n{dataa[2]}")


                        
                        if verbose:
                            console.print(dataa)
                        

                        # RETURN INFO // 0 == TABLE DATA / 1 == SAVE INFO
                        return [dataa, DATA]
                    

                    elif response.status_code == 429:
                        
                        console.print(f"triggered rate limiting with port: {port}, retrying at a slower rate to pull website headers\nServer header response: {response.headers}")
                        time.sleep(3)

                        if go == 2:
                            
                            return ["N/A", "N/A"]

                        go = 2


                    

                    else:

                        if verbose:
                            console.print(f"Status code: {response.status_code}")

                        return ["N/A", "N/A"]

            
            
                # DESTROY ERRORS
                except requests.ConnectTimeout as e:

                    if verbose:
                        console.print(f"[bold red]Request Timeout Error:[yellow] {e}")
                    return ["N/A", "N/A"]
                

                except requests.ConnectionError as e:

                    if verbose:
                        console.print(f"[bold red]Requests Connection Error:[yellow] {e}")
                    return ["N/A", "N/A"]

                
                except Exception as e:

                    if verbose:
                        console.print(f"[bold red]sub_utilities Exception Error:[yellow] {e}")
                    return ["N/A", "N/A"]
        


        @staticmethod
        def get_service_version_nmap(target, port):
            """This method will be using the nmap libary to get the service version"""


            CMD = f"nmap -p {port} {target}"
            results = subprocess.run(CMD, capture_output=False, text=True)
            results = str(results.stdout)

            return results
        

        @staticmethod
        def main(port, table):
            """This will be in control of what type of service_version method is called upon"""


            # DESTROY ERRORS
            verbose = False
            

            # DEBUGGING
            if verbose:
                console.print(f"Port --> {port}")
            
            # ERRORS
            if verbose:
                console.print("using request_scanner")
            

            # USE REQUEST METHOD 
            if port in [80,443,53,2096,8443,8080]:

                return Socket_Port_Scanner.Sub_Utilities.get_service_version_request(port=port)

                    
            
            # USE RAW SOCKETS METHOD
            else:

                # ERRORS
                if verbose:
                    console.print("using socket_scanner")

                return Socket_Port_Scanner.Sub_Utilities.get_service_version_socket(port=port)




# END OF -->  sub_utilities 
    def __init__(self):

        
        # SET PORT VALUE VARIABLES
        self.ports_found_with_service = []
        self.ports_open = 0
        self.ports_closed = 0
        self.ports_filtered = 0
    

    @classmethod  # THIS METHOD WAS CREATED TO FIX HOW VERSION INFO IS PRINTED OUT
    def track_scans(cls, port=False, service=False):
        """Track what scan we are on"""


        if port:
            num = (f"{port} - {service}")
            
            return num, cls.scans

        return cls.num, cls.scans
        
    
    def port_scanner_tcp(self, ip:str, port, table) -> tuple:
        """This method will be responsible for doing a tcp scan on target device"""


        # SET VARIABLE
        print_text = False

        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:


                # SET TIMEOUT VALUE  
                s.settimeout(3)
                

                # GET PORT & SERVICE STATUS
                result = s.connect_ex((ip, port))
                service = self.Sub_Utilities.get_service(port)
                

                # OPEN
                if result == 0:

                    # GET SERVICE VERSION IF AVAILABLE
                    version = Socket_Port_Scanner.Sub_Utilities.main(port=port, table=table) 


                    # CREATE SECTION IF VALID
                    if version[0].strip() != "N/A":
                        table.add_section()
                    
                   # console.print(f"{port} --> {version}")
                    table.add_row(f"{port}", f"{service}", f"{version[0]}", "OPEN")

                    # CREATE SECTION IF VALID
                    if version[0].strip() != "N/A":
                        table.add_section()

                        # RESET VALUE
                        Socket_Port_Scanner.Sub_Utilities.create_sec = False

                    if print_text:
                        console.print(f"[bold green]Open Port:[/bold green] {port} --> {service}")
                    


                    # THIS METHOD WILL BE IN CHARGE OF MAKING THE DICT THAT WILL BE SAVED
                    num, scans = Socket_Port_Scanner.track_scans(port=port, service=service)
                    scans[num] =  version[1]


                    self.ports_open += 1


                    # THIS IS DEAPPRECIATED AND WILL NO LONGER BE USED // WILL KEEP ACTIVE FOR NOW
                    self.ports_found_with_service.append(f"{port} : {service} - {version[1]}")
                    
                
                # CLOSED
                elif result in [111, 113]:

                    if print_text:
                        console.print(f"[bold red]Closed Port:[/bold red] {port}")

                    self.ports_closed += 1



                # FILTERED
                else:

                    if print_text:
                        console.print(f"[yellow]Filtered Port:[/yellow] {port}")

                    self.ports_filtered += 1
                    
                    

        
        except socket.timeout as e:
            console.print(f"[bold red]Socket Timeout Error on Port:[/bold red] {port} --> {e}")


            # IF THIS HAPPENS ITS A TIMEOUT ERROR
            self.ports_closed += 1
  

        
        except socket.gaierror as e:
            console.print(f"[bold red]Socket Error:[yellow] {e}")

            
            # IT IS CLOSED IF U GET THIS ERROR
            self.ports_closed += 1

        
        except Exception as e:
            console.print(f"[bold red]socket scanner Exception Error:[yellow] {e}")
    
    
    def threader(self, ip: str, scan_type=1, thread_count=250) -> str:
        """This method is responsible for performing a threaded port scan"""
        

        # SPACE FROM OTHER CALLED METHOD
        print("\n")


        if scan_type == 1:
          ports = range(1,1025)
        
        elif scan_type == 2:
            ports = range(1,65536)



        # CREATE TABLE
        table = Table(title="Port Scan", title_style="bold red", header_style="bold red", style="bold purple")
        table.add_column("Port", style="bold blue")
        table.add_column("Service", style="yellow")
        table.add_column("Version", style="red")
        table.add_column("Status", style="bold green")

        
        
        # NOW TO COUNT HOW LONG SCAN HAS BEEN TAKING
        time_start = time.time()
        #scanner = Socket_Port_Scanner()  # # CLEANSE DATA // PREVENT FUCKUPS


        
        # BEGIN THREADED PORT SCAN // LOL SHII IS EASY
        with Live(table, console=console, refresh_per_second=.1):
            with ThreadPoolExecutor(max_workers=thread_count) as executor:

                try:

                    for port in ports:
                        executor.submit(self.port_scanner_tcp, ip, port, table)


                
                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")
            
        

        # NOW TO GET TIME
        time_took =  time.time() - time_start

        results = (
            f"[bold green]Total Open Ports:[/bold green] {self.ports_open}  "
            f"[yellow]Total Filtered Ports:[/yellow] {self.ports_filtered}  "
            f"[bold red]Total Closed Ports:[/bold red] {self.ports_closed}  "
             f"[yellow]Total Thread Count:[/yellow] {thread_count}    "
            f"[bold blue]Elapsed Time:[/bold blue] {time_took:.2f} Seconds"
            )
        

        # PANEL RESULTS
        panel = Panel(title="Scan Results", style="bold purple", expand=False, renderable=results, border_style="bold green")
        console.print("", panel)



        # SPEAK RESULTS ALOU
        use = False
        if use:
            say = f"Successfully completed Port scan, with a total of: {self.ports_open} Ports Open, {self.ports_filtered} Ports Filtered, and {self.ports_closed} Ports Closed"
        else:
            say = f"Successfully completed port scan"
        Utilities.tts(say=say, voice_rate=5)

        
        results_txt = (
                        f"Total Open Ports: {self.ports_open}\n"
                         f"Total Filtered Ports: {self.ports_filtered}",
                         f"Total Closed Ports: {self.ports_closed}\n",
                         f"Open Ports with Service: {self.ports_found_with_service}",
                         f"Filtered Ports with Service: Not Bound"
                         
                         )
        results_txt = '\n'.join(results_txt)


        a, scan = Socket_Port_Scanner.track_scans()
        

        results_json = {
            f"Total_Open_Ports": self.ports_open,
            f"Total_Filtered_Ports": self.ports_filtered,
            f"Total_Closed_Ports": self.ports_closed,
            f"Active_Ports_with_Service": scan                        
        }
        


        # FOR DISCORD // TRASH WAY OF DOING IT, CANT USE CLASS WHEN ITS A SELF
        Socket_Port_Scanner.track_ports(open=self.ports_open, filtered=self.ports_filtered, closed=self.ports_closed)

        if use:        
            a, scan = Socket_Port_Scanner.track_scans()

            console.print(scan)


        # PUSH RESULTS
        return [results_json, results_txt]
        

    
    @classmethod
    def track_ports(cls, open=False, filtered=False, closed=False, clean=False): 
        """This method's sole purpose is to provide port info to main method from <-- threader to then pass to discord"""
        

        # CLEAN IT
        if clean:
            cls.dis_open = ""
            cls.dis_filtered = ""
            cls.dis_closed = ""

            return
        
        
        # SHOW TIME // GIVE IT TO DISCORD
        if open == False:

            return cls.dis_open, cls.dis_filtered, cls.dis_closed


        # SAVE IT
        cls.dis_open = open
        cls.dis_filtered = filtered
        cls.dis_closed = closed



    @staticmethod
    def main(target, scan_type=2, thread_count=2000):
        """This method will be responsible for calling upon module logic"""


        # SCAN TYPE 1 == (1, 1024)
        # SCAN TYPE 2 == (1, 65536) 



        # PERFORM GREATNESS
        result = Socket_Port_Scanner().threader(ip=target, scan_type=scan_type, thread_count=thread_count)


        # DISCORD SUMMARY --> FILE SENDING
        from nsm_utilities import File_Handler
        open, filtered, closed = Socket_Port_Scanner.track_ports()
        data = (f"Open Ports: {open}\nFiltered Ports: {filtered}\nClosed: {closed}")
        File_Handler.push_info_to_discord(save_data=data, save_type=1)


        return result



class Requests_Subdomain_Scanner():
    """This class will be responsible for performing a subdomain scan"""
    
    
    # CLASS VARIABLES // FIRST TIME USING PRETTY COOL
    subs_up = 0
    subs_active = []
    results_json = {}
    results_txt = []


    def __init__(self):
        self.subs_up = 0
        self.sups_down = 0
    



    @staticmethod
    def get_website_status(sub_domain:str, timeout=1):
        """This method was created to fix the problem where i get subdomains that end up being a 404"""


        # DESTROY ERRORS
        verbose = False

        valid = [200, 301, 302, 403]
        loop = 1

        if verbose:
            print("hey", sub_domain)
        
        while True:
            try:

                url = f"https://{sub_domain}"

                response = requests.get(url=url, timeout=timeout, allow_redirects=False)


                if response.status_code in valid:

                    if verbose:
                        console.print(f"Url: {url} --> Valid")
                    
                    return True
                

                else:
                    return False

        

            except Exception as e:

                if verbose:
                    console.print(f"Failed: {sub_domain} --> Timeout: {timeout}")

                if loop < 3:
                    timeout += 1
                    loop +=1

                else:
                    return False


    @staticmethod
    def get_headers(sub, domain, timeout=3):
        """This method is used to pull and parse headers for the subdomain"""


        # ERRORS
        verbose = False


        # STORE DATA
        data = {}
        dataa = []

        sub_domain= (f"{sub}.{domain}")
        url = f"https://{sub_domain}"
        

        try:
            response = requests.get(url=url, timeout=timeout)
     

        

        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            if verbose:
                console.print(f"[bold red]Requests Connection or Timeout Error:[yellow] {e}")
                                                      
            console.print(f"Failed To Fetch Headers -->[bold red] {sub_domain}", style="yellow")
            return False
        

        except Exception as e: 
            if verbose:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
            
            console.print(f"Failed To Fetch Headers -->[bold red] {sub_domain}", style="yellow")
            return False 
        
       

        try:
            # GET HEADERS AND PARSE THAT MOTHER FUCKERRR
            headers = response.headers

            valid_keys = [
                    "server", "x-powered-by", "x-frame-options", 
                    "content-security-policy", "strict-transport-policy", "refer-policy", 
                    "x-xss-protection", "set-cookie"
                    ]         
            

            for key, value in headers.items():


                # LOWER FOR BETTER PARSING
                key = key.lower().strip()

                if key.lower() in valid_keys:

                    data[key] = value
                
            
            # FOR MISSING KEYS
            for key in valid_keys:
                if key not in data:
                    data[key] = "Missing"
                
            

            # DEBUG ME
            if verbose:
                console.print(data)
            

            # CONTROL DATA CHAR LENGTH
            if len(data['content-security-policy']) > 50:
                console.print(f"max char length triggered --> [yellow]{sub_domain}", style="bold red")
                data["content-security-policy"] = f"{len(data['content-security-policy'])} Chars"
                

          
            # GET VARS
            server = data['server']
            x_powered_by = data['x-powered-by']
            x_frame_options = data['x-frame-options']
            content_security_policy = data['content-security-policy']
            strict_transport_security = data['strict-transport-policy']
            refer_policy = data['refer-policy']
            x_xss_protection = data["x-xss-protection"]
            set_cookie = data["set-cookie"]
            


            dataa = [

                (f"Server: {server}"),
                (f"x-powered-by: {x_powered_by}"),
                (f"x-frame-options: {x_frame_options}"),
                (f"content-security-policy: {content_security_policy}"),
                (f"strict-transport-security: {strict_transport_security}"),
                (f"refer-policy: {refer_policy}"),
                (f"x-xss-protection: {x_xss_protection}"),
                (f"set-cookie: {set_cookie}")

            ]        

            

            res = (f"{dataa[0]}  |   {dataa[1]}\n{dataa[2]}   |   {dataa[3]}\n{dataa[4]}   |   {dataa[5]}\n{dataa[6]}   |   {dataa[7]}") 



            # RETURN RESULTS 
            return res
        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

            return "Failed to Fetch Headers, Might be a 200 --> 404"

    
  
    @staticmethod
    def get_subdomains(sub_path):
        """This method will be responsible for pulling subdomains // might be from json or hardcoded"""

        
        # CREATE SUBDOMAIN FILE PATH
        file_path = Path.home() / "Documents" / "nsm tools" / "network tools" / "Netvuln 2" / "subdomains"



        # FOR MAPPING
        paths = {
            "1": "sub_1k.txt",
            "2": "sub_20k.txt",
            "3": "sub_100k.txt"
        }

        
        # USE THIS TO DETERMINE THE FILE WE WILL BE USING
        if sub_path == "1":
            path = file_path / "sub_1k.txt"
        
        elif sub_path == "2":
            path = file_path / "sub_20k.txt"
        
        elif sub_path == "3":
            path = file_path / "sub_100k.txt"
        
        
        # ERROR FALL BACK
        else:
            path = file_path / "sub_1k.txt"

        
        while True:

            try:

                if base_dir.exists() and file_path.exists() and file_path.is_dir() and path.exists():

                    
                    with open(path, "r") as file:
                        content = [line.strip() for line in file]
                        
                        
                        # TELL THE USER CONTENT HAS SUCCESSFULLY BEEN PULLED
                        console.print(f"\n\n[bold green]Successfully Retrieved:[/bold green] [bold red]{paths[sub_path]}[/bold red] from [bold blue]{path} \n")
                        time.sleep(1)

                        return content
                

                # USE THIS ELSE STATEMENT TO CREATE FILE PATHS
                else:
                    
                    # CREATE BASE DIR
                    base_dir.mkdir(exist_ok=True, parents=True)

                    
                    # CREATE SUBDOMAIN FILE PATH
                    file_path.mkdir(parents=True, exist_ok=True)


            
            except FileNotFoundError as e:
                console.print(e)
                time.sleep(3)
                break


            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
    

    
    @classmethod
    def subdomain_scanner(cls, sub:any , domain: str, current, sub_amount, table, sus) -> str:
        """This method will be responsible for scanning the subdomains for a active connections"""

         
        # CHOOSE WEATHER TO USE REQUEST OR DNS.RESOLVER LIBARY FOR QUERIES
        method = 1

        # STOP OUTPUT PRINT // THINK OF THIS AS VERBOSE CONTROL LOL
        use = False

        
        try:
            

            # DNS RESOLVER METHOD // LITERALLY MADE FOR THIS // LOL 
            if method == 1:

                
                # CREATE DOMAIN AND ITERATE THROUGH IT
                sub_domain = f"{sub}.{domain}"

                rdata = dns.resolver.resolve(sub_domain, "A")

                if rdata:


                    # CHECK IF THE SUB-DOMAIN IS ACTUAL VALID
                    if Requests_Subdomain_Scanner.get_website_status(sub_domain=f"{sub}.{domain}") == False:
                        return


                    data = ', '.join([str(r) for r in rdata])

                    # NOW TO GET THE IP OF THE SUBDOMAIN AND INCREASE SUB COUNT
                    ip = socket.gethostbyname(f"{sub}.{domain}")
                    cls.subs_up += 1
                   



                    # GET HEADERS INFO
                    headers = Requests_Subdomain_Scanner.get_headers(sub=sub, domain=domain)
   


                    if use:
                        console.print(f"[bold green]Active --> [bold blue]{url}")

                    else:
                        
                        # OUTPUT DATA TO TABLE AND APPEND TO LIST
                        c1 = "bold green"
                        c2 = "bold blue"
                        
                        
                        table.add_row(f"{sub}.{domain}", "-->", f"{data}", f"{headers}") 
                        table.add_section()
                        cls.subs_active.append(f"{sub}.{domain}")


                        # SAVE DATA
                        subdomain = f"{sub}.{domain}"
                        cls.results_json[subdomain] = data
                        cls.results_txt.append(f"{subdomain} --> {data}\n")
            


            
            # REQUEST METHOD // DEAPPRECIATED, INCONSISTENT WITH RESULTS
            elif method == 2:


                # FORM URL 
                url = f"https://{sub}.{domain}"
                
                with sus:
                    response = sus.get(url=url, timeout=3)
                

                if response.status_code == 200:


                    # NOW TO GET THE IP OF THE SUBDOMAIN AND INCREASE SUB COUNT
                    ip = socket.gethostbyname(f"{sub}.{domain}")
                    cls.subs_up += 1

                    if use:
                        console.print(f"[bold green]Active --> [bold blue]{url}")

                    else:

                        table.add_row(f"{sub}.{domain}", "-->", f"{ip}")       

            def error(type, error_message):
                """error"""

                console.print(f"[bold red]{type}:[yellow] {error_message}")
        
        # DNS EXCEPTIONS
        except  dns.resolver.NXDOMAIN as e:
            if use:
                console.print(f"[bold red]DNS Resolver Error:[yellow] {e}")

        except  dns.resolver.Timeout as e:
            if use:
                console.print(f"[bold red]DNS Resolver Timeout Error:[yellow] {e}")        

        except  dns.exception.DNSException as e:
            if use:
                console.print(f"[bold red]DNS Resolver DNSException Error:[yellow] {e}")
    
  
        
        
        # REQUEST EXCEPTIONS
        except requests.ConnectTimeout as e:
            if use:
                console.print(f"[bold red]Timeout Error:[yellow] {e}")

        
        
        except requests.ConnectionError as e:
            if use:
                console.print(f"[bold red]Requests Error:[yellow] {e}")
        

        except Exception as e:
            if use:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
        

        finally:
            if use:
                console.print(f"[bold green]Current Subdomain Count:[bold blue] {current}/{sub_amount}")

        
    
    @classmethod
    def threader(cls, domain:str , sub_path: str, thread_count=250, delay = .05):
        """This method will be responsible for performing a threaded subdomain scan // making the scan faster for bigger text files"""



        # PULL SUBDOMAINS // TRACK LOOP // CREATE INSTANCE
        sub_scanner = Requests_Subdomain_Scanner()
        subdomains = Requests_Subdomain_Scanner.get_subdomains(sub_path=str(sub_path))
        subdomain_count = len(subdomains)
        current = 0     # THIS VARIABLE IS DEAPPRECIATED // NO LONGER IN USE | REPLACEMENT IS --> cls.subs_up
        cls.subs_up = 0 # RESET THIS
        lock = threading.Lock()



        # CREATE PANEL FOR DATA INSERTATION
        panel = Panel(renderable=f"[bold green]Subdomain Count:[/bold green] {current}/{subdomain_count}", border_style="bold green", style="bold purple", expand=False)
        

        # CREATE TABLE FOR DATA OUTPUT
        table = Table(title="Subdomain Scan", title_style="bold red", style="bold purple", border_style="bold purple", header_style="bold red")
        table.add_column("Subdomain",style="bold blue")
        table.add_column("-->", style="bold red")
        table.add_column("IP Address", style="bold green")
        table.add_column("Header Info")


        # START TIMER
        time_start = time.time()
        lol = 0


        # MAKE SURE THE USER DOESNT OVERWHELM THERE ROUTER
        if sub_path in ["2", "3"] and delay < .5:
            delay = 1
            console.print(f"[bold red]Your delay was overriden and changed to:[/bold red] {delay}\n[bold green]This was done to prevent Network Exshaustion")

        # BEGIN THREADING SCAN  
        try:  
            with Live(table, console=console, refresh_per_second=.01):
                with requests.Session() as sus:     
                    with ThreadPoolExecutor(max_workers=thread_count) as executor:
                        for sub in subdomains:
                            executor.submit(sub_scanner.subdomain_scanner, sub, domain, current, subdomain_count, table, sus)


                            # THIS WILL BE USED TO LIMIT THE AMOUNT OF REQUESTS SENT PER SECOND
                            if lol == 30: 
                                time.sleep(delay)
                                lol = 0

                            lol += 1
                            current += 1

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")
            input("[bold red]errorrrrrrrrrrrrrrrrrr: ")



        # TELL THE USER SCAN ELAPSED TIME
        time_took = time.time() - time_start
        panel = Panel(f"[bold green]Total Subdomains Found:[/bold green] {cls.subs_up}/{subdomain_count}    [yellow]Total Threads Used:[/yellow] {thread_count}    "
                     f"[bold blue]Elapsed Time:[/bold blue] {time_took:.2f} Seconds",
                       border_style="bold green", style="bold purple", expand=False)
        
        console.print("", panel)


        
        # SPEAK ALOUD THE RESULTS
        use = False
        if use:
            say = f"Successfully completed subdomain enumeration scan, with a total of: {cls.subs_up} out of {subdomain_count} subdomains found"
        else:
            say = f"Successfully completed subdomain enumeration scan"
        Utilities.tts(say=say, voice_rate=10)


        # FORMAT TXT


        # RETURN SUBDOMAIN RESULTS // NEXT STEP DIR ENUM
        return cls.subs_active


    
    @classmethod
    def main(cls, target, sub_path="1", thread_count=250, delay=.3):
        """This method will be responsible for calling upon class wide logic"""

        # CLEANSE DATA // PREVENT INFO FUCKUPS 
        cls.subs_active = []
        cls.results_json = {}
        cls.results_txt = []

        
        # FUTURE LOGIC WILL USE THIS LINE TO PULL INFO FROM THE SETTINGS MODULE TO GET USER SETTINGS

        
        
        # CHECK IF THERE IS A DOMAIN TO SCAN IF NOT | TARGET == FALSE (SKIP)
        if  target:
            domain = str(target) 


            # PERFORM GREATNESS
            results = Requests_Subdomain_Scanner.threader(domain=domain, sub_path=sub_path, thread_count=thread_count, delay=delay)

            
            # FORMAT DATA
            cls.results_txt = '\n'.join(cls.results_txt)

            # SAVE DATA --> FILE STORING
            from nsm_settings import File_Saving
            File_Saving.push_info(save_data=[cls.results_json, cls.results_txt], save_type="4")


            # DISCORD SUMMARY --> FILE SENDING
            from nsm_utilities import File_Handler
            data = (f"Total Subdomains Found: {cls.subs_up} out of {len(Requests_Subdomain_Scanner.get_subdomains(sub_path=str(sub_path)))}")
            File_Handler.push_info_to_discord(save_data=data, save_type=2)


            return results
        

        else:
            console.print("\n[bold red]Sub-Domain Enumeration Skipped Due To:[yellow] False Domain given")



class Module_Controller():
    """This class will be responsible for calling upon Mulit-Module wide logic to consistently and cleanly perform NetVuln Scan"""


    def __init__(self):
        pass


    
    @staticmethod
    def get_domain_newer(target: str):
        """This will be the better and up-to-date method to help get domain from ip"""
        

        # MAKE THIS TRUE IF U WANT THE USER TO ONLY BE ABLE TO SCAN FOR ACTUAL DOMAINS ONLY // MIGHT HAVE TO CHANGE CLASS LOGIC
        domain_only = False



        # COMPLETELY BACKWARDS BUT IT WORKS LOL
        try:
            result = ipaddress.ip_address(str(target))
            
            if result and domain_only == False:
                console.print(f"[bold red]IP Address Detected:[/bold red] [yellow]Failed To Validate Domain")
                return False
            
            elif result and domain_only == True:
                console.print(f"[bold green]Successfully Validated IP Address")
                return target
        


        except Exception as e:

            if domain_only:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

                return False
            
            else:
                console.print(f"[bold green]Successfully Validated Domain")
                return target
        

    @staticmethod  # THIS METHOD IS DEAPPRECIATED FOR CONSISTENT UP TO DATE RESULTS USE --> get_domain_newer 
    def get_domain_request(target: str) -> tuple:
        """This will be a helper method for get_ip_domain <- to check if the user has provided a domain"""

        
        go = False
        verbose = True
        
      
        
        try:
            
            
            url = f"https://{target}"

            response = requests.get(url=url, timeout=2.5, allow_redirects=True)

            if response.status_code == 200:
                go = True
                console.print("[bold green]Successfully Validated Domain")
            
            elif response.status_code == 304:
                console.print(f"[bold green]Successfully Validated Domain")
            
            else:
                if verbose:
                    console.print(f"[bold red]Invalid Status code for: [yellow]{url}[/yellow] with: {response.status_code}")
  

        except requests.Timeout as e:
            if verbose:
                console.print(f"[bold red]Requests Timeout Error:[yellow] {e}")

        
        except requests.ConnectionError as e:
            if verbose:
                console.print(f"[bold red]Requests Connection Error:[yellow]{e}")
                time.sleep(2)
            

        
        except Exception as e:
            if verbose:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
        

        finally:

            if go == False:
                console.print("[bold red]Failed To Validate Domain")

            return target if go else False

    
    @staticmethod
    def get_ip_domain() -> tuple:
        """This method will be responsible for taking the user inputted target and returning a valid stringed ip along with the domain if one was provided"""


        # DESTROY ERRORS
        verbose = True

      

        # PANEL FOR GIVEN DOMAIN
        table_domain = Table(title="Target Validation",title_style= "bold red", border_style="bold purple",style="bold purple", header_style="bold red")
        table_domain.add_column(f"Target Domain", style="bold blue")
        table_domain.add_column(f"-->", style="bold red")
        table_domain.add_column(f"Target IP", style="bold green")


        # ELSE PANEL FOR GIVEN IP
        table_ip = Table(title="Target Validation",title_style= "bold red",border_style="bold purple", style="bold purple", header_style="bold red")
        table_ip.add_column("Given IP")
        table_ip.add_column("-->", style="bold red")
        table_ip.add_column(f"Valid IP", style="bold green")


        # PREVENT MODULE SWITCHING ERRORS
        target = ""


        
        # LOOP FOR EXCEPTIONS
        while True:

            try:


                target = console.input("\n[bold red]Enter Domain or IP Address: ").strip().lower()

                
                # IF THE USER WANTS TO EXIT
                if target in ["exit", "leave", "bye", "1"]:
                    
                    # SEND BACK TO UI MODULE
                    console.print("bye bye", style="bold red")
                    time.sleep(1)
                    from nsm_ui import MainUI
                    MainUI.main()
                    
                

                # CHECK TO SEE IF THE TARGET CAN BE RESOLVED TO A VALID IP
                ip = socket.gethostbyname(target)
                valid_ip = ipaddress.ip_address(ip)
                console.print("\n[bold green]Successfully Validated IP Address")
                

                # CHECK TO SEE IF THERE WAS A VALID DOMAIN GIVEN
                domain = Module_Controller.get_domain_newer(target)

                
                # PRINT CONFIRMATION
                if domain:
                    table_domain.add_row(f"{domain}", "--> ", f"{ip}")
                    console.print("\n" ,table_domain)
                
                else:
                    table_ip.add_row(f"{ip}", "--> ", f"{valid_ip}")
                    console.print("\n", table_ip)
                

                
                # PASS VALUES TO SUBTILITIES MODULE // FOR VERSION LOOKUP
                Socket_Port_Scanner().Sub_Utilities.ip = ip
                Socket_Port_Scanner().Sub_Utilities.domain = domain


                # FORMAT RESULTS 
                results_json = {
                    "ip": ip,
                    "domain": domain
                }

                results_txt = [
                    f"ip: {ip}",
                    f"domain: {domain}"
                ]
                

                # FORMAT DATA
                results_txt = '\n'.join(results_txt)

                # SAVE DATA --> FILE STORING
                from nsm_settings import File_Saving
                File_Saving.push_info(save_data=[results_json, results_txt], save_type="1")

                

      
                return str(valid_ip), domain

            

            except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
                console.print(e)

                if verbose:
                    console.print("im in get_ip_domain")


            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

                if verbose:
                    console.print("im in get_ip_domain")

    

    @staticmethod
    def module_ui(text="  Ethical\n  Hacker", font="bloody", style="bold purple"):
        """This will house simple logic to output a module message"""
        

        welcome = pyfiglet.figlet_format(text=text, font=font)
        console.print(f"\n\n{welcome}\n\n", style=style) 


    
    @staticmethod
    def controller(scan_type=2, sub_path="1", dir_path="1"):
        """This will be in charge of Multi-Module Logic"""


        # OUTPUT WELCOMING UI
        Module_Controller.module_ui()
        File_Handler.get_program_total_lines() # SHOW TOTAL LINES OF CODE
        

        # USER VALIDATION CHECK
        ip, domain = Module_Controller.get_ip_domain()


        # NOTIFY USER THAT THE SCAN IS STARTING
        Utilities.noty(msg="Now Starting NetVuln scan")
        threading.Thread(target=Utilities.tts, args=("Now Beginning NetVuln scan", 15 ), daemon=True).start()



        
        # GET GEO INFO N MORE
        results_geo_info = NetTilities.get_geo_info(target_ip=ip.strip())
        

        # PERFORM PORT SCAN
        results_open_ports = Socket_Port_Scanner.main(target=ip, scan_type=scan_type)


        # PERFORM SUBDOMAIN ENUMERATION
        results_sub_domains = Requests_Subdomain_Scanner.main(target=domain, sub_path=sub_path)


        # PERFORM DIRECTORY ENUMERATION
        results_directories = Requests_Directory_Scanner.main(sub_domains=results_sub_domains, dir_path=dir_path)


        # PERFORM NMAP VULNERABILITY SCAN // NSE
        results_nmap = Nmap_Vulnerability_Scanner.nmap_vuln_scanner(target=ip, ports=results_open_ports) 



        # LOG RESULTS
        File_Handler.save_scan_results(save_data=(domain, ip), save_type=1)     # DOMAIN --> IP RESOLUTION
        File_Handler.save_scan_results(save_data=results_geo_info[0], save_type=2)  # IPINFO DATA
        File_Handler.save_scan_results(save_data=results_open_ports[0], save_type=3) # PORTS DATA
        File_Handler.save_scan_results(save_data=results_sub_domains, save_type=4) # SUBDOMAINS DATA
        File_Handler.save_scan_results(save_data=results_directories[0], save_type=5)  # DIRECTORY DATA
        File_Handler.save_scan_results(save_data=results_nmap[0], save_type=6)  # NMAP DATA 



        # PUSH SUMMARY TO DISCORD
        File_Handler.push_info_to_discord(save_type=4)
        
        
        # NOW TO FEED SAVED SCAN INFO TO AI // AND PUSH FINAL INFO TO SAVE DATA FILE
        AI_GENERATED_SUMMARY = NetTilities.talk_to_ai(prompt=File_Handler.save_scan_results(save_data=False,save_type=10), max_characters=1500, respond=True)
        File_Handler.save_scan_results(save_data=AI_GENERATED_SUMMARY, save_type=15)
        

        # EXIT // WHILE TRUE IN CASE OF ACCIDENTAL ENTER PRESS
        print('\n')
        while True:
            choice = console.input("[bold red]Type exit to leave: ").strip().lower()
            
            if choice == "y" or choice == "yes" or choice == "1" or choice == "exit" or choice == "leave":
                break




# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":


    start = 1


    if start == 1:

        Module_Controller.controller()


    elif start == 2:

        ip = "youtube.com"

        Requests_Subdomain_Scanner.main(target="carmax.com")



    elif start == 3:

        ip = socket.gethostbyname("google.com")
        Socket_Port_Scanner.Sub_Utilities.ip = socket.gethostbyname("discord.com")
        Socket_Port_Scanner.Sub_Utilities.domain = "discord.com"
        Socket_Port_Scanner().threader(
            ip=ip, 
            thread_count=700, 
            scan_type=1
            )
    
    
    elif start == 4:

        ip = socket.gethostbyname("google.com")


        ip, domain = Module_Controller.get_ip_domain()

        open_ports = Socket_Port_Scanner.main(target=ip, scan_type=1)

        #console.print(open_ports)
        
    
    elif start == 5:
        #Utilities.tts(say="hello youtube, subscribe for more streams", voice_rate=5)

        Module_Controller.get_domain_newer(target="nsmbarii.com")
        Module_Controller.get_domain_newer(target="192.168.1.1")












# AI QUESTSION

#1 = "Please ask me clarifying questions until you are 95% confident that you can complete the task successfully"

#2 = "What would someone in the top 0.1% of this field think?"