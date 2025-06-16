# NETVULN 2.0 // THIS MODULE WILL HOLD THE LOGIC FOR STORING SCAN RESULTS ALONG WITH MUCH MORE AND SETTINGS LOGIC


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
import pyfiglet


# NETWORK IMPORTS
import socket, ipaddress, dns.resolver, openai



import requests, socket, scapy, ipaddress, dns.resolver, threading


# ETC IMPORTS
import threading, time, random, requests, os, time
from concurrent.futures import ThreadPoolExecutor
import pyttsx3
from plyer import notification
from datetime import datetime


# NSM IMPORTS
from nsm_utilities import NetTilities
from nsm_target_scanner import Socket_Port_Scanner


# CONSTANTS & GLOBALS
console = Console()
terminal_width = console.size.width


# FILE HANDLING
from pathlib import Path
import json


    # BASE DIR
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0"
base_dir.mkdir(parents=True, exist_ok=True)




# SCAN TREE
#
#  .data
#     Netvuln 2
#       api_keys
#         api_keys.json
#       scan_results
#         05-01-2025_16_06_40        # MAKE A FOLDER FOR EACH SCAN INITIATED
#           raw_save_socket_scan
#           raw_save_subdomain_scan
#           raw_save_nmap
#           raw_save_ffuf
#           raw_save_vulners
#           raw_save_shodan
#           raw_save_ipinfo
#           raw_save_openai
#           AI_GENERATED_SUMMARY
#           How_To_NetVuln.txt    # THIS WILL EXPLAIN HOW TO USE THE GIVEN SAVED INFO
#
#



# import ctypes
# ctypes.windll.kernel32.SetConsoleTitleW("Your New Title")


class File_Saving():
    """This method will be responsible for saving and storing scan results"""


    # GLOBAL VARIABLES
    filename = ""
    paths_made = False


    def __init__(self):
        pass

    
    
    
    @staticmethod
    def get_path_way(save_type: str):
        """This will be a sub method for the push_info method <-- to give the method the valid pathway to use """


        # STATIC PATH
        base_path = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0" / "scan_results" 


        # GET PATHS
        paths = File_Saving.create_folders(method_type="2", target_ip="False")
                

        # GET DYNAMIC PATH
        if save_type == "1" or save_type == "resolve":
            return paths["domain_ip"]
        
        elif save_type == "2" or save_type == "ipinfo":
            return paths["ipinfo"]
        
        elif save_type == "3" or save_type == "socket":
            return paths["socket"]

        elif save_type == "4" or save_type == "subdomain":
            return paths["subdomain"]
        
        elif save_type == "5" or save_type == "directory":
            return paths["directory"]
        
        elif save_type == "6" or save_type == "shodan":
            return paths["shodan"]
        
        elif save_type == "7" or save_type == "vulners":
            return paths["vulners"]

        elif save_type == "8" or save_type == "nmap":
            return paths["nmap"]

        elif save_type == "9" or save_type == "openai":
            return paths["openai"]
        
        elif save_type == "15" or save_type == "all":
            return paths["all"]
        

        # SCAN TREE
        #
        #  .data
        #     Netvuln 2
        #       api_keys
        #         api_keys.json
        #       scan_results
        #         05-01-2025_16_06_40        # MAKE A FOLDER FOR EACH SCAN INITIATED
        #           raw_save_domain_ip_resolve
        #           raw_save_socket_scan
        #           raw_save_subdomain_scan
        #           raw_save_nmap
        #           raw_save_ffuf
        #           raw_save_vulners
        #           raw_save_shodan
        #           raw_save_ipinfo
        #           raw_save_openai
        #           AI_GENERATED_SUMMARY
        #           How_To_NetVuln.txt    # THIS WILL EXPLAIN HOW TO USE THE GIVEN SAVED INFO


    @classmethod
    def get_time_stamp(cls, target_ip:str):
        """This is another helper method for the create_folders helper method to then help that method and maybe more"""

       
        try:

            # MAKE IP FILE SAVEABLE // NOT IN USE AS OF THE MOMENT
            path_ip = '_'.join(target_ip.split('.'))


            if cls.filename != "":
                return cls.filename



            # CREATE STATIC FILE NAME
            else:

                while True:
                    time_stamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")  # I == 12 H == 24
                    cls.filename = f"{time_stamp}"

                    if cls.filename:
                        return cls.filename


        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")       


    @classmethod
    def create_folders(cls, method_type:str, target_ip: str = "NOT_IN_USE"):
        """This method will be a sub method for push_info <- to create all necessary folders to put scan results in"""


        # VARIABLES
        verbose = False
 
        
        # SHOUDNT BE ANY ERRORS BUT JUST IN CASE
        try:


            file_name = File_Saving.get_time_stamp(target_ip=target_ip)
            folder_dirs = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0" / "scan_results" / str(file_name)
            folder_dirs.mkdir(parents=True, exist_ok=True)

            
            # A DEDICATED FOLDER FOR EACH TYPE OF SCAN
            raw_save_domain_ip_resolve = folder_dirs / "raw_save_domain_ip_resolve"
            raw_save_ipinfo = folder_dirs / "raw_save_ipinfo"
            raw_save_socket_scan = folder_dirs / "raw_save_socket_scan"
            raw_save_subdomain_scan = folder_dirs / "raw_save_subdomain_scan"
            raw_save_directory_scan = folder_dirs / "raw_save_directory_scan"
            raw_save_nmap = folder_dirs / "raw_save_nmap"
            raw_save_vulners = folder_dirs / "raw_save_vulners"
            raw_save_shodan = folder_dirs / "raw_save_shodan"
            raw_save_openai = folder_dirs / "raw_save_openai"
            raw_save_everything = folder_dirs / "raw_save_everything"


            paths = [
                raw_save_domain_ip_resolve,
                raw_save_socket_scan,
                raw_save_subdomain_scan,
                raw_save_nmap,
                raw_save_directory_scan,
                raw_save_vulners,
                raw_save_shodan,
                raw_save_ipinfo,
                raw_save_openai,
                raw_save_everything
            ]
            
            
            # CREATE ALL NECESSARY FOLDERS
            if method_type == "1" or method_type == "make":
                for path in paths:
                    path.mkdir(parents=True, exist_ok=True)
                    
                    # FOR DEBUGGING
                    if verbose:
                        console.print(f"Successfully made path for: {path}", style="bold green")
                
                if cls.paths_made == False:
                    console.print("Successfully made all dedicated file folders", style="bold green")
                    cls.paths_made = True
            

            # GIVE PATHS AS JSON
            elif method_type == "2" or method_type == "get":

                paths = {
                    "domain_ip": raw_save_domain_ip_resolve,
                    "socket": raw_save_socket_scan,
                    "subdomain": raw_save_subdomain_scan,
                    "nmap": raw_save_nmap,
                    "directory": raw_save_directory_scan,
                    "vulners": raw_save_vulners,
                    "shodan": raw_save_shodan,
                    "ipinfo": raw_save_ipinfo,
                    "openai": raw_save_openai,
                    "all": raw_save_everything
                }
                    

                return paths



        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")


    @classmethod
    def push_info(cls, save_data, save_type:str):
        """This is where info will be pushed to then be stored"""


        # CLEAN PARAMS
        if save_type == "1":
            cls.paths_made = False
            File_Saving.filename = ""



        # ERROR DEBUGGING
        verbose = False


        # FILE SAVING VALUES
        indent = 4
        ascii = False
        encoding = "utf-8"



        # CREATE PATH WAYS
        File_Saving.create_folders(method_type="1", target_ip="False")

        
        # GET PATH
        path = File_Saving.get_path_way(save_type=save_type)

         
        while True:

            # CHECK TO MAKE SURE PATH WAYS EXISTS
            if path.exists() and  path.is_dir() and base_dir.exists():




                # FOR SAVING OPENAI RESPONSES
                if save_type == "9":

                    # CREATE PATHS
                    path_way_json = path / "response.json"

                    path_way_txt = path / "response.txt"

                    path_raw = path / "response_raw.txt"



                    # SAVE CLEANED AI RESPONSE
                    with open(path_way_txt, "w", encoding=encoding) as file:   
                        file.write(str(save_data[0]))  # 1 == TEXT
                        

                        if verbose:
                            console.print(f"Successfully Saved txt info --> {file}")
                    
                    

                    if verbose:
                        console.print(f"BOOM --> {path}", style="bold red") 
                    

                    
                    # SAVE RAW AI RESPONSE
                    with open(path_raw, "w", encoding=encoding) as file:   
                        file.write(str(save_data[1]))  # 1 == TEXT
                        

                        if verbose:
                            console.print(f"Successfully Saved txt info --> {file}")
                    
                    

                    if verbose:
                        console.print(f"BOOM --> {path}", style="bold red")

                    
                    # ALMOST DONE
                    console.print(f"\n[bold green]Successfully Saved Results --> Scan Type:[bold green] {save_type}") 
                
                

                # FOR ALL DATA PUT TOGETHER
                elif save_type == "15":
                   
                    
                    # PATH FOR ALL RESULTS
                    path_way_json = path / "results_all.json"
                    path_way_txt = path / "results_all.txt"


                    with open(path_way_json, "w", encoding=encoding) as file:

                        json.dump(save_data, file, indent=indent, ensure_ascii=ascii)    # 0 ==  JSON
                        
                        if verbose:
                            console.print(f"Successfully Saved json info --> {file}")
                    

                    # SAVE RAW AI RESPONSE
                    with open(path_way_txt, "w", encoding=encoding) as file:   
                        file.write(str(save_data))  # 1 == TEXT
                        

                        if verbose:
                            console.print(f"Successfully Saved txt info --> {file}")
                    
                    

                    if verbose:
                        console.print(f"BOOM --> {path}", style="bold red") 

                    
                    # BOOM END OF SCAN
                    console.print(f"\n[bold green]Successfully Saved Results --> Scan Type:[bold green] {save_type}")



  
                
                # FOR RESULTS FROM SCANS // ENUMERATIONS
                elif type(save_data) == list:
                    
                    path_way_json = path / "results.json"

                    path_way_txt = path / "results.txt"


                    with open(path_way_json, "w", encoding=encoding) as file:

                        json.dump(save_data[0], file, indent=indent, ensure_ascii=ascii)    # 0 ==  JSON
                        
                        
                        if verbose:
                            console.print(f"Successfully Saved json info --> {file}")

                    with open(path_way_txt, "w", encoding=encoding) as file:   
                        file.write(str(save_data[1]))  # 1 == TEXT
                        

                        if verbose:
                            console.print(f"Successfully Saved txt info --> {file}")
                    
                    

                    if verbose:
                        console.print(f"BOOM --> {path}", style="bold red")
           
                    
                    console.print(f"\n[bold green]Successfully Saved Results --> Scan Type:[bold green] {save_type}")
                

                break

            
            # CREATE PATH WAYS
            else:
                

                if verbose:
                    # FOLDER HANDLER // LOL
                    console.print("ELSE STATEMENT TRIGGERED", style="bold red")

                File_Saving.create_folders()


                break







# STRICTLY FOR MODULER TESTING
if __name__ == "__main__":

    use = 2

    if use == 1:
        File_Saving.create_folders()

    
    elif use == 2:

        loop = 0
        targets = ["google.com", "youtube.com", "gmail.com"]

        while loop < 3:
            File_Saving.filename = targets[loop].split('.')[0]
            ip_info = NetTilities.get_geo_info(target_ip=socket.gethostbyname(targets[loop]))
            File_Saving.push_info(save_data=ip_info, save_type="2")

            socket_info = Socket_Port_Scanner.main(target=socket.gethostbyname(targets[loop]))
            File_Saving.push_info(save_data=socket_info, save_type="3")


            # CHANGE LOOP VALUE
            loop += 1