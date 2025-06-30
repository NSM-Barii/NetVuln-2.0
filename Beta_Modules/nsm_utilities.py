# NETVULN 2.0 // THIS MODULE WILL HOLD THE LOGIC FOR UTILITIES


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
import pyfiglet


# NETWORK IMPORTS
import socket, ipaddress, dns.resolver, openai, shodan, vulners


# ETC IMPORTS
import threading, time, random, requests, os
from concurrent.futures import ThreadPoolExecutor
import pyttsx3
from plyer import notification


# CONSTANTS & GLOBALS
console = Console()
terminal_width = console.size.width


# FILE HANDLING
from pathlib import Path
import json


    # BASE DIR
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0"
base_dir.mkdir(parents=True, exist_ok=True)







class NetTilities():
    """This class will be responsible for housing simple Network methods"""

    
    # CLASS VARIABLES
    done = True


    def __init__(self):
        pass


    @classmethod
    def get_conn_status(cls):
        """This method will be responsible for checking if the user is online or offline and will procceed accordingly"""
        

        # METHOD VALUES
        timeout = 3
        color_1 = "bold green"
        color_2 = "bold red"



        while True:

            try:

                url = "https://google.com"

                response = requests.get(url=url, timeout=timeout)

                if response.status_code == 200:

                    # TELL THE USER THE GOOD NEWS
                    if cls.done:
                        Utilities.noty(msg="Connection Status Online\nWelcome To NetVuln 2.0")
                        threading.Thread(target=Utilities.tts, args=("Connection Status Online, Welcome to NetVuln 2.0",), daemon=True ).start()

                        cls.done = False

                    break

                
                else:
                    
                    # PANEL FOR ASS INTERNET
                    panel = Panel(renderable=f"Your INTERNET IS HOT ASS PLEASE TRY AGAIN LATER", style="bold red", expand=False)
                    console.print(panel)

            
            
            except requests.Timeout as e:
                console.print(f"[bold red]Requests Timeout Error:[yellow] {e}")


                console.input(f"\nPress [{color_1}]Enter[/{color_1}] to [{color_1}]Re-Try[/{color_1}] or [{color_2}]Ctrl[/{color_2}] + [{color_2}]C[/{color_2}] to [{color_2}]Exit:[/{color_2}] ")


            except requests.ConnectionError as e:
                console.print(f"[bold red]Requests Connection Error:[yellow] {e}")


                console.input(f"\nPress [{color_1}]Enter[/{color_1}] to [{color_1}]Re-Try[/{color_1}] or [{color_2}]Ctrl[/{color_2}] + [{color_2}]C[/{color_2}] to [{color_2}]Exit:[/{color_2}] ")


            except KeyboardInterrupt as e:
                console.print("[bold green]Sorry to see you go, [yellow]please come back with better [bold red]INTERNET")
                time.sleep(3)

            
            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

                console.input(f"\nPress [{color_1}]Enter[/{color_1}] to [{color_1}]Re-Try[/{color_1}] or [{color_2}]Ctrl[/{color_2}] + [{color_2}]C[/{color_2}] to [{color_2}]Exit:[/{color_2}] ")

    
    @staticmethod
    def talk_to_ai(prompt: str, role_user = False, role_system = False, max_characters = 400, respond=True):
        """This method will be used to submit scan info to AI, to then have it summarized and given back to the user"""


        # MAKE SURE USER IS READY TO QUERY AI // SINCE IT COST MONEY
        print('\n')
        while True:
            choice = console.input("Do you want to feed info to OpenAI[bold green](y/[bold red]n)[/bold red][bold purple]: ").strip().lower()
            
            if choice == "y" or choice == "yes" or choice == "1":
                break

            elif choice == "n" or choice == "no" or choice == "0":
                console.print("[bold green]\nOpenAI:[bold red] Fine skip me, I HATED YOU ANYWAYS")
                time.sleep(1)
                return "User Skipped Scan."
        

        # PRINT ALL THE AGGREGATED RESULTS CURRENT BEING HELD FOR USER TO SEE
        console.print(prompt)


        
        # CATCH AND DESTROY ERRORS
        try:

            console.input("\n[bold green]ARE U SURE: ")

            # GET API KEY FOR AI
            api_key_ai = File_Handler.get_api_key()["api_key_openai"]



            # ROLES
            roles = {
                1: "You are a highly skilled bug bounty hunter and cybersecurity analyst. "
                    "Your job is to review scan results, network info, service banners, subdomain directories, and known CVEs, "
                    "and help identify real-world exploitable vulnerabilities. "
                    "Always focus on actionable insights, especially ones that could lead to: RCE, XSS, SQLi, IDOR, SSRF, or authentication flaws. "
                    "If a port or directory might expose a login page, hidden file, or API endpoint — highlight that. "
                    "If something looks like a false positive, say so. "
                    "Always provide follow-up actions or payload ideas that could confirm the vuln in a real bug bounty scenario.",

                2: "You are a cybersecurity anyalasis and i need you to summarize the results i give you"
                }


            # AI MESSAGE VARIABLES
            role_system = role_system if role_system else roles[1]
            role_user = role_user if role_user else "Ok now using all the scan info i just provided you tell me whats the next best course in action i should take with this vulnerability scan. and are u able to do web lookups to help me find more info ?"
                

            
            
            # CREATE A OBJECT
            client = openai.OpenAI(api_key=api_key_ai)

            
            # TELL THE USER THE AI IS WORKING
            threading.Thread(target=Utilities.tts, args=("ChatGPT Said, Now proccessing information sir", ), daemon=True).start()
            console.print("[bold green]ChatGPT:[bold blue] Now getting to work sir")
            
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"{role_system}"},
                        {"role": "user", "content": f"{role_user}" f"{prompt}"}
                    ],
                    temperature=0.3,

                    max_tokens=max_characters
                    )
                    
                
                # CLEAN UP AND RETURN RESPONSE
                response_clean = response.choices[0].message.content.strip().replace('\\n', "\n")


                # FORMAT DATA
                response_txt = response_clean.split('\n')
                response_raw = response

 

                # IF RESPOND == TRUE, PRINT RESULTS AND ALSO SPEAK IT ALOUD               
                if respond:
                    console.print(response_clean)
                    threading.Thread(target=Utilities.tts, args=(response_clean, 5)).start()

                                
                # SAVE DATA --> FILE STORING
                from nsm_settings import File_Saving
                File_Saving.push_info(save_data=[response_txt, response_raw], save_type="9")


                return response_txt
            
            
            except Exception as e:
                console.print(f"[bold red]AI Exception Error:[yellow] {e}")


        # DESTROY ERRORS
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

    
    @staticmethod
    def get_geo_info(target_ip: str):
        """This method will be responsible for taking the targets ip and returning geo ip info along with more"""


        # GET API KEY
        print("\n")
        api_key = File_Handler.get_api_key()["api_key_ipinfo"]
        results_json = {}
        results_txt = []
        results_json = {}
        results_txt = []

        if api_key:
            url = f"https://ipinfo.io/{target_ip}?token={api_key}"
  
        else:
            url = f"https://ipinfo.io/{target_ip}"
       
        

        try:
            response = requests.get(url=url, timeout=5)

            

            if response.status_code == 200:

                # STORE INFO
                table = Table(title="GEO Lookup", title_style="bold red", header_style="bold red", style="bold purple")
                table.add_column("Key", style="bold blue")
                table.add_column("-->", style="bold red")
                table.add_column("Value", style="bold green")
                

                # ITERATE THROUGH INFO
                for key, value in response.json().items():

                    table.add_row(f"{key}", "-->", f"{value}")
                    results_json[key] = value
                    results_txt.append(f"{key} --> {value}")
                    results_json[key] = value
                    results_txt.append(f"{key} --> {value}")


                console.print(table)


                # FOR SAVING INFO
                results_txt = '\n'.join(results_txt)


                # SAVE DATA --> FILE STORING
                from nsm_settings import File_Saving
                File_Saving.push_info(save_data=[results_json, results_txt], save_type="2")

                return [results_json, results_txt]
                results_txt = '\n'.join(results_txt)


                # SAVE DATA --> FILE STORING
                from nsm_settings import File_Saving
                File_Saving.push_info(save_data=[results_json, results_txt], save_type="2")

                return [results_json, results_txt]

                 

            
            else:
                console.print("GEO LOOKUP FAILED", style="bold red")
            
        


        except requests.ConnectTimeout as e:
            console.print(f"[bold red]Connection Timeout Error:[yellow]{e}")
        
        
        except requests.ConnectionError as e:
            console.print(f"[bold red]Requests Connection Error:[yellow]{e}")

        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow]{e}")
        

    @staticmethod    # API ERRORS
    def get_shodan_info(target_ip:str):
        """This method will be responsible for querying shodan's api"""


        # GET KEY
        api_key = File_Handler.get_api_key()["api_key_shodan"]
        verbose = True
        
        if not api_key:
            console.print("Failed to find your shodan api key!", style="bold red")
            return  False
        
        try:
            sho = shodan.Shodan(key=api_key)
             
            if verbose:
              console.print(sho.info())

            results = sho.host(target_ip)
            console.print(results)

        
        except shodan.exception.APITimeout as e:
            console.print(f"[bold red]Shodan API TIMEOUT Error:[yellow] {e}")

        

        except shodan.exception.APIError as e:
            console.print(f"[bold red]Shodan API Error:[yellow] {e}")
        


        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")


    @staticmethod    # NOT YET FINISHED
    def get_WPSscan_info(target:str):
        """This method will be responsible for pulling wpsscan info"""


        #GET API KEY
        api_key = File_Handler.get_api_key()["api_key_wpsscan"]

        if not api_key:
            console.print("Failed to find your WPSscan api key!", style="bold red")
            return  False

        try:
            
            url = f"https://wpscan.com/api/v3/{target}"
            headers = {
                "Authorization": api_key
            }

            response = requests.get(url=url, headers=headers, timeout=5)


            if response.status_code == 200:
                console.print(response)

            
            else:
                console.print(f"[bold red]Failed to get API info with Status Code:[yellow] {response.status_code}")



        except requests.exceptions.Timeout as e:
            console.print(f"[bold red]Requests Timeout Error:[yellow] {e}")
        

        except requests.exceptions.ConnectionError as e:
            console.print(f"[bold red]Requests Connection Error:[yellow] {e}")
        

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

      
    @staticmethod
    def get_vulners_info(target:str):
        """This method will be responsible for pulling info from vulners"""


        # GET API_KEY
        api_key = File_Handler.get_api_key()["api_key_vulners"]

        if not api_key:
            console.print("Failed to find your Vulners api key!", style="bold red")
            return  False
        
        

        url = f"https://vulners.com/api/v3/search/lucene/"
        data = {
            "query": str({target}),
            "api_key": api_key,
        }
        
        try:
            response = requests.post(url=url, json=data, timeout=5)


            if response.status_code == 200:
                #console.print(response.json())
                response = response.json()

                # SET VARIABLES
                vulns = []
                num = 0
                vuln_data = {}
               #vuln_data = {
               #     "index": key['_index'],
               #     "id": key['_id'],
               #     "score": key['_score'],
               #    "source": key['_source'],
               #     "highlight": key['highlight'],
               #    "sort": key['sort'],
               #     "description": key['flatDescription']             
               # }

                for value in response['data']['search']:

   
                    console.print(f"NUMBER: {num}")
                    for key, val in value.items():
                        console.print(f"{key} -->  {val}")

                        vuln_data[key] = val

                        
                    #console.print(vuln_data)
                    vulns.append(vuln_data)

                    
                    num += 1

                console.print(vuln_data)
                console.print(vuln_data)
                console.print("\n\n\nSuccess",style="bold green" )
                #console.print(vuln_data)

            
            else:
                console.print(f"[bold red]Failed to get API info with Status Code:[yellow] {response.status_code}")
        

        except requests.ConnectTimeout as e:
            console.print(f"[bold red]Connection Timeout Error:[yellow] {e}")
        
        
        except requests.ConnectionError as e:
            console.print(f"[bold red]Requests Connection Error:[yellow] {e}")

        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")




class Utilities():

    """This class will be responsible for holding common utilities that i will be constantly using"""

    
    # CLASS VARIABLES
    start = False
    allowed = True
    allowed = True


    def __init__(self):
        pass



    @staticmethod
    def clear_screen():
        """This method is strictly used to clear the console screen for smoother transition"""
        

        try:
        
            # WINDOWS
            if os.name == "nt":
                os.system("cls")
            

            # LINUX / MAC
            elif os.name == "posix":
                os.system("clear")
            

            # EXCEPTION
            else:
                console.print("coudnt clear your bitch ass screen")
            
        
        except Exception as e:
            console.print(f"[bold red]Utilities Module Error:[yellow] {e}")


    @classmethod
    def noty(cls, msg, timeout=10):
        """This method will be responsible for outputting notifications to the users system"""
        

        # ONLY FOR WINDOWS FOR THE MOMENT // WILL BE DEAPPRECIATED SOON
        if cls.allowed:

            if Utilities.get_current_os() == "nt":
                try:
                    

                    notification.notify(
                        app_name ="NetVuln 2.0",
                        title = "NetVuln 2.0",
                        message = msg,
                        timeout = timeout,
                    )

                
                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")
            


    @classmethod
    def tts(cls, say, voice_rate:int = 20, voice_sound:int = 1, lock=False):
        """This will be used to output tts through the users speakers"""



        # CHECK OS THIS METHOD IS FOR WINDOWS ONLY // WILL BE DEAPPRECIATED SOON
        if cls.allowed:


            if Utilities.get_current_os() == "nt":


                # CREATE OBJECT
                try:
                    engine = pyttsx3.init()
                    
                    # SET VARIABLES
                    rate = engine.getProperty('rate')
                    voices = engine.getProperty('voices')


                

                    engine.setProperty('rate', rate - voice_rate)
                    
                    

                    # SET VOICE
                    if len(voices) > 0:
                        engine.setProperty('voice', voices[1].id)
                    
                    else:
                        engine.setProperty('voice', voices[0].id)
                    
                    # USE THREAD LOCKER
                    if lock:  
                        with lock:
                            engine.say(say)
                            engine.runAndWait()
                    
                    
                    # NO THREAD LOCKER
                    else:
                        if engine.isBusy():
                            engine.stop()
                            engine.say(say)
                            engine.runAndWait()
                        
                        else:
                            engine.say(say)
                            engine.runAndWait()
                    
                    
                         

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")
        
            
            # UNIX / LINUX
            else:
                cls.allowed = False
                console.print("Linux system found, wil not use tts engine")
                time.sleep(2)
    

    
    @staticmethod
    def get_current_os():
        """This method will be used to check wheather this program is being run on windows or throught the container, or else"""
      
        
        # WINDOWS
        if os.name == "nt":
            return "nt"
        

        # UNIX / LINUX
        elif os.name == "posix":
            return "posix"
    

    
    @classmethod
    def push_to_discord(cls, data, retry=3):
        """This method will be resposnible for pushing information to discord"""


        # DESTROY ERRORS
        verbose = False
        attempt = 1
        timeout = 5


        # GRAB DISCORD KEY
        webhook = File_Handler.get_api_key()['api_key_discord']


        headers = {"content-type": "application/json"}
        payload = {"content": data}



        
        while attempt <= retry:
            try:

                response = requests.post(webhook, data=json.dumps(payload), headers=headers, timeout=timeout)


                if response.status_code in [200, 204]:
                    console.print("Successfully pushed info to discord", style="bold green")

                    return

                
                else:
                    console.print("Failed to push info to discord", style="bold red")

                    # INCREASE TIMEOUT // INCRAMENT ATTEMPT
                    timeout += 2
                    attempt += 1




                

            # DESTROY ERROS
            except (requests.ConnectionError, requests.Timeout) as e:

                if verbose:
                    console.print(f"1 Timeout: {timeout} --> Attempt{attempt}", style='yellow')
            
                console.print(f"[bold red]Request Error:[yellow] {e}")
                

                # INCREASE TIMEOUT // INCRAMENT ATTEMPT
                timeout += 2
                attempt += 1

            

            except Exception as e:

                if verbose:
                    console.print(f"2 Timeout: {timeout} --> Attempt{attempt}", style='yellow')

                console.print(f"[bold red]Exception Error:[yellow] {e}")

                # INCREASE TIMEOUT // INCRAMENT ATTEMPT
                timeout += 2
                attempt += 1



class File_Handler():
    """This class will be responsible for pulling information for other module classess"""


    # CLASS VARIABLES
    ip_domain = ()
    ip_info = []
    ports_open = []
    sub_found = []
    dirs_found = []
    nmap_found = []


    def  __init__(self):
        self.ip_domain = ()
        self.ports_open = []
        self.sub_found = []
        


    
    
    @staticmethod
    def image_extractor(icon_path="1"):
        """This method will pull pictures ment for notifications"""


        # DEFINE FILE PATH
        file_path = Path.home() / "Documents" / "nsm tools" / "network tools" / "netvuln 2" / "app_icon"


        # CREATE MAPPING
        paths = {
            "1": "nsm.jpg"
        }


        # CHOOSE BETWEEN IMAGES
        if icon_path == "1":
            path = file_path / "nsm.jpg"
        


        if file_path.exists() and file_path.is_dir():

            with open(path, "r") as file:
                content = file.read()

                time.sleep(1)


                # TELL USER THAT U SUCCESSFULLY GOT THE FILE PATH
                console.print(f"\n\n[bold green]Successfully Retrieved:[/bold green] [bold red]{paths[icon_path]}[/bold red] from [bold blue]{path} \n")


                return content




        
        #EXCEPTION TO CREATE PATH
        else:

            file_path.mkdir(parents=True, exist_ok=True)

    

    @staticmethod
    def get_api_key(path_api = "1"):
        """This method will be responsible for pulling the users api's key, depending on what api is being used dynamically"""\
        

        # FOR DEBUGGING
        verbose = False
        loop = True


        
        # CREATE API_KEY DIR
        file_path = Path.home() / "Documents" / "nsm tools" / ".data" / "Netvuln 2.0" / "api_keys"
        
        
        # CHECK IF IT EXISTS
        while loop:
            if file_path.exists() and file_path.is_dir():

                
                # PATH WAY TO EXTRACT API_KEYS
                path = file_path / "api_keys.json"


                if verbose:
                    console.print("Created path way supposedly", style="bold red")


                # NOW TO OPEN UP THE FILE PATH WAY
                while True:
                    
                    try:
                        with open(path, "r") as file:

                            console.print("Successfully Retrieved api_key", style="bold green")
                            time.sleep(1)
                            loop = False
                            return json.load(file)
                        



                    # CREATE JSON FILE IN CASE IT CANT BE FOUND
                    except FileNotFoundError as e:
                        console.print(f"[bold red]FileNotFound Error:[yellow] {e}")


                        # CREATE DATA
                        data = {
                            "api_key_openai": "",
                            "api_key_shodan": "",
                            "api_key_ipinfo": "",
                            "api_key_vulners": "",
                            "api_key_wpsscan": "",
                            "api_key_discord": ""
                        }

                        # PATH WAY TO EXTRACT API_KEYS
                        path = file_path / "api_keys.json"


                        with open(path, "w") as file:
                            json.dump(data, file, indent=4)
                            
                            # LET THE USER KNOW THAT IT WAS SUCCESSFULL
                            console.print("Successfully created default json file", style="bold green")
                            
                    
                    
                    except Exception as e:
                        console.print(f"[bold red]Exception Error:[yellow] {e}")
                        
                        if loop == 3:
                            loop = False
                        
                        else:
                            loop += 1



    
        



            # CREATE FILE PATH
            else:
                file_path.mkdir(parents=True, exist_ok=True)



    @classmethod
    def save_scan_results(cls, save_data: str, save_type: int):
        """This method will be responsible for saving and storing scan results"""


        # ERROR DEBUGGING
        verbose = False
     

        # SAVE IP AND OR DOMAIN
        if save_type == 1:
            cls.ip_domain = save_data

        
        # SAVE GEO INFO // IPINFO
        elif save_type == 2:
            cls.ip_info = save_data
        

        # SAVE OPEN PORTS FOUND
        elif save_type == 3:
            cls.ports_open = save_data
        

        # SAVE SUBS FOUND
        elif save_type == 4:
            cls.subs_found = save_data
         
        
        # SAVE DIRS FOUND
        elif save_type == 5:
            cls.dirs_found = save_data


        # SAVE VULNS FOUND
        elif save_type == 6:
            cls.nmap_found = save_data

        

        # NOW TO AGGRAGATE RESULTS AND RETURN IT FOR AI
        # NOW TO AGGRAGATE RESULTS AND RETURN IT FOR AI
        elif save_type == 10:
 
            results = {
                "domain_ip_resolution": cls.ip_domain,
                "ipinfo": cls.ip_info,
                "ports_found": cls.ports_open,
                "subdomains_found": cls.subs_found,
                "directories_found": cls.dirs_found,
                "nmap_results": cls.nmap_found
            }
            
            if verbose:
                #console.print(f"\n\n[bold green]Successfully aggragatted results:[white] {results}", style="bold green")

                console.print("\n\n",results)

            return results
            
        

        # NOW TO AGGRAGATE RESULTS AND SAVE IT TO FILE DATA SAVING
        elif save_type == 15:

            cls.AI_SUMMARY = save_data  # JUST IN CASE // LOL

            results = {
                "domain_ip_resolution": cls.ip_domain,
                "ipinfo": cls.ip_info,
                "ports_found": cls.ports_open,
                "subdomains_found": cls.subs_found,
                "directories_found": cls.dirs_found,
                "nmap_results": cls.nmap_found,
                "AI_Generated_Summary": cls.AI_SUMMARY
            }



            # SAVE DATA --> FILE STORING
            from nsm_settings import File_Saving
            File_Saving.push_info(save_data=results, save_type="15")



            # RESET CLS VALUES
            cls.ip_domain = ()
            cls.ip_info = ()
            cls.ports_open = []
            cls.sub_found = []
            cls.dirs_found = []
            cls.nmap_found = []

            if verbose:
                console.print(f"Successfully cleaned class values", style="bold red")


            return results
        
    
    
    @classmethod
    def push_info_to_discord(cls, save_data=False, save_type=False):
        """This method will be used to save a summary view of info to then push to discord before giving the full scan results"""


        if save_type == 1:
            cls.sum_ports = save_data

        elif save_type == 2:
            cls.sum_subs = save_data

        elif save_type == 3:
            cls.sum_dirs = save_data
        
        
        elif save_type == 4:

            d1 = "NetVuln 2.0  -  Developed by NSM Barii\nThis is a summary scan report! For the full results please return to the FucKing program DUMBASS!\n\n"
            troll = "\n\nWould you like to PENETRATE  this website with maxium efficiency? "

            LINE = "-" * 50
            LINEE = "-" * 20

            

            # PARSE JSON DATA
            domain = cls.ip_domain[0]
            ip = cls.ip_domain[1]

            target = f"Target Resolution:  {domain} --> {ip}"
            
            # PARSE GEO INFO
            city = cls.ip_info.get('city', 'N/A')
            region = cls.ip_info.get('region', 'N/A')
            country = cls.ip_info.get('country', 'N/A')
            postal = cls.ip_info.get('postal', 'N/A')
            timezone = cls.ip_info.get('timezone', 'N/A')
            loc = cls.ip_info.get('loc', 'N/A')
            org = cls.ip_info.get('org', 'N/A')

            geo = (
                f"City:  {city}\n"
                f"Region:  {region}\n"
                f"Country:  {country}\n"
                f"Loc:  {loc}\n"
                f"Org:  {org}\n"
                f"Postal:  {postal}\n"
                f"Timezone:  {timezone}"
            )


            data = (
                f"{LINE}\n"
                f"{d1}\n"
                f"{LINEE}\n"
                f"{target}\n"
                f"{LINEE}\n"
                f"{geo}\n"
                f"{LINEE}\n"
                f"{cls.sum_ports}\n"
                f"{LINEE}\n"
                f"{cls.sum_subs}\n"
                f"{cls.sum_dirs}\n"
                f"{LINEE}\n"
                f"{troll}"
            )




            # PUSH INFO TO DISCORD 
            Utilities.push_to_discord(data=data)


            # FLUSH RESULTS
            cls.sum_ports = ""
            cls.sum_subs = ""
            cls.sum_dirs = ""
        

        else:
             console.print("\nI DO NOT HAVE PERMISSION TO PUSH INFO TO DISCORD", style="bold red")



    @staticmethod
    def get_program_total_lines():
        """This method will be responsible for getting the total lines of code used to create this program"""


        # DISCLAMER THIS WILL ONLY COUNT .PY FILES FROM THE BETA_MODULES FOLDER
    
        

        # WINDOWS PATH
        if Utilities.get_current_os() == "nt":

            path = Path.home() / "Documents" / "NSM Tools" / "Network Tools" / "Netvuln 2" / "beta_modules"
        
        elif Utilities.get_current_os() == "posix":
            
            return



        lines = 0

        try:
            for file in path.iterdir():


                if file.name.split('.')[1]=='py':
                    with open(file, "r") as file:

                        content = file.readlines()
                        #console.print(file.name)

                        for line in content:
                            lines += 1
                        
        except Exception as e:
            pass


        finally:
            console.print(f"[bold blue]NetVuln 2.0 is madeup of:[bold green] {lines} Lines of code\n\n")
                
        




# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":


    use = 0


    if use == 0:
        
        data = "test script"
        Utilities.push_to_discord(data=data)

    if use == 1:
        p = "sending me text back like \n "
        NetTilities.talk_to_ai(prompt=p, max_characters=30, role_system="this is a test run", role_user="test run")
    

    elif use == 2:


        File_Handler.get_api_key()
        
        # TEST DATA
        results = {
            "Also u are with my livestream so say hey to them before u start i gave kirk, g_13gee, em4072"
            "Open_ports": [21,22,23,25,53,80,443,143,3389],
            "Domain": "google.com"
        }


        results = "Also u are with my livestream so say hey to them before u start i gave kirk, g_13gee, em4072, and eli and beyonce and jordan"

        
        Utilities.tts(say="feeding info to ai")
        response = NetTilities.talk_to_ai(prompt=results, max_characters=550)
        console.print(response)
        Utilities.tts(say=response, voice_rate=20)
    

    
    elif use == 3:
        NetTilities.get_geo_info(target_ip=socket.gethostbyname("google.com"))
        NetTilities.get_shodan_info(target_ip=socket.gethostbyname("google.com"))
        NetTilities.get_vulners_info(target="google.com")



