# THIS WILL HOLD THE LOGIC FOR BEING ABLE TO PULL CVE AND SERVICE VERSION INFO FROM EXTERNAL API TOOLS


# UI IMPORTS
import dns.exception
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
import pyfiglet


# NETWORK IMPORTS
import socket, ipaddress, dns.resolver, nmap, shodan


# ETC IMPORTS
from html.parser import HTMLParser
import threading, time, random, requests, subprocess
from concurrent.futures import ThreadPoolExecutor

import shodan.exception



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





class API_Puller():
    """This class will be responsible for pulling api info to then aggregate and feed to OpenAI"""

    # CLASS VARIABLES



    def __init__(self):
        pass


    
    @staticmethod
    def pull_vulners_info(target:str, timeout=5, retry=2):
            """This method will be responsible for pulling info from vulners"""
            

            # FOR ERRORS
            verbose = False


            # GET API_KEY
            api_key = File_Handler.get_api_key()["api_key_vulners"]

            if not api_key:
                console.print("Failed to find your Vulners api key!", style="bold red")
                return  False
            
            

            url = f"https://vulners.com/api/v3/search/lucene/"
            data = {
                "query": str({target}),
                "api_key": api_key,
                "maxsearchsize": 500
            }
            
            try:
                response = requests.post(url=url, json=data, timeout=timeout)


                if response.status_code == 200:
                    

                    # FORMAT DATA AND RETURN IN
                    response_json = response.json()


                    if verbose:
                        console.print(response.json())
                        input("\n\nPress to go: ")

                    # RETURN DATA
                    return response_json
                
                else:
                    console.print(f"[bold red]Failed to get API info with Status Code:[yellow] {response.status_code}")
            

            except requests.ConnectTimeout as e:
                console.print(f"[bold red]Connection Timeout Error:[yellow] {e}")
            
            
            except requests.ConnectionError as e:
                console.print(f"[bold red]Requests Connection Error:[yellow] {e}")

            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

    
    @staticmethod   # SADLY CANT USE YET, WILL COME BACK TO TO ADD LOGIC FOR SETTINGS
    def pull_censys_info(target:any, timeout=3, retry=2):
        """This method will be responsible for pulling censys info for cve info"""


        # VARS
        api_key = File_Handler.get_api_key()["api_key_censys"]
        url = f"https://search.censys.io/api/v2/hosts/{target}"
        params = {
            "bearer": api_key
        }


        try:

            # MAKE THE REQUESTS
            response = requests.get(url=url, timeout=timeout, params=params)


            if response.status_code == 200:

                response_json = response.json()



                # RETURN DATA
                return response_json




        
        except requests.exceptions.ConnectTimeout as e:
            console.print(f"[bold red]Requests Connection Timeout Error:[yellow] {e}")


        
        except requests.ConnectionError as e:
            console.print(f"[bold red]Requests Connection Error:[yellow] {e}")

        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")



    @staticmethod
    def pull_shodan_info(target:any, retry=2):
        """This method will be used to retrieve shodan info"""


        # GET API KEY
        api_key = File_Handler.get_api_key()["api_key_shodan"]

        # CREATE OBJECT
        sd = shodan.Shodan(key=api_key)
        
        try:
            response_json = sd.host(ips=target, minify=True)
            sd.Exploits.search



            # RETURN DATA 
            return response_json
        
        


        # DESTROY ERRORS
        except shodan.exception.APITimeout as e:
            console.print(f"[bold red]Shodan Timeout Error:[yellow] {e}")

        
        except shodan.exception.APIError as e:
            console.print(f"[bold red]Shodan API Error:[yellow] {e}")
        

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")



    @staticmethod   # THIS WILL BE COMPLETED ONCE WE GET pull_shodan_info <-- completed   
    def pull_nvd_info(target:any, timeout=3, retry=2):
        """This method will be responsible for pulling censys info for cve info"""


        # VARS
        api_key = File_Handler.get_api_key()["api_key_censys"]
        url = f"https://search.censys.io/api/v2/hosts/{target}"
        params = {
            "bearer": api_key
        }


        try:

            # MAKE THE REQUESTS
            response = requests.get(url=url, timeout=timeout, params=params)


            if response.status_code == 200:

                response_json = response.json()



                # RETURN DATA
                return response_json




        
        except requests.exceptions.ConnectTimeout as e:
            console.print(f"[bold red]Requests Connection Timeout Error:[yellow] {e}")

        
        except requests.ConnectionError as e:
            console.print(f"[bold red]Requests Connection Error:[yellow] {e}")

        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")




# FOR MODULER TESTING ONLY
if __name__ == "__main__":
    
    use = 2 
     
    
    if use == 1:
        # TARGET
        target = socket.gethostbyname("discord.com")
    
        results_vulners = API_Puller.pull_vulners_info(target=target)
        console.print(results_vulners)
        results_shodan = API_Puller.pull_shodan_info(target=target)
        
        while True:
            NetTilities.talk_to_ai(prompt=results_vulners)
    







