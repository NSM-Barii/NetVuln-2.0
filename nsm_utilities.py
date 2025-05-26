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
                console.input(f"[bold red]Requests Timeout Error:[yellow] {e}")


                console.input(f"Press [{color_1}]Enter[/{color_1}] to [{color_1}]Re-Try[/{color_1}] or [{color_2}]Ctrl[/{color_2}] + [{color_2}]C[/{color_2}] to [{color_2}]Exit:[/{color_2}] ")


            except requests.ConnectionError as e:
                console.input(f"[bold red]Requests Connection Error:[yellow] {e}")


            
            except KeyboardInterrupt as e:
                console.print("[bold green]Sorry to see you go, [yellow]please come back with better [bold red]INTERNET")
                time.sleep(3)

            
            except Exception as e:
                console.input(f"[bold red]Exception Error:[yellow] {e}")

    
    
    @staticmethod
    def talk_to_ai(prompt: str, role_user = False, role_system = False, max_characters = 400):
        """This method will be used to submit scan info to AI, to then have it summarized and given back to the user"""

        
        # CATCH AND DESTROY ERRORS
        try:

            # GET API KEY FOR AI
            api_key_ai = File_Handler.get_api_key()["api_key_openai"]


            # AI MESSAGE VARIABLES
            role_system = role_system if role_system else "You are a cybersecurity anyalasis and i need you to summarize the results i give you"
            role_user = role_user if role_user else "Can you simply explain this for me plz like im a baby, u dont have to repeat back to me things i already know like subs found"
                

            
            
            # CREATE A OBJECT
            client = openai.OpenAI(api_key=api_key_ai)

            
            # TELL THE USER THE AI IS WORKING
            threading.Thread(target=Utilities.tts, args=("ChatGPT Said, Now proccessing information sir", ), daemon=True).start()
            console.print("[bold green]ChatGPT:[bold blue] Now getting to work sir")
            
        
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"{role_system}"},
                    {"role": "user", "content": f"{role_user}" f"{prompt}"}
                ],
                temperature=0.5,

                max_tokens=max_characters
            )
            
            # CLEAN UP AND RETURN RESPONSE
            response_clean = response.choices[0].message.content.strip()
            return response_clean
        
        
        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

    

    @staticmethod
    def get_geo_info(target_ip: str):
        """This method will be responsible for taking the targets ip and returning geo ip info along with more"""


        # GET API KEY
        print("\n")
        api_key = File_Handler.get_api_key()["api_key_ipinfo"]

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

                
                console.print(table)

            
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
    def get_WPSscan_info():
        """This method will be responsible for pulling wpsscan info"""


        #GET API KEY
        api_key = File_Handler.get_api_key()["api_key_wpsscan"]

        if not api_key:
            console.print("Failed to find your WPSscan api key!", style="bold red")
            return  False

        try:
            
            url = f"https://suckmydick"
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

        try:
            

            notification.notify(
                app_name ="NetVuln 2.0",
                title = "NetVuln 2.0",
                message = msg,
                timeout = timeout,
            )

        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")

    

    @staticmethod
    def tts(say, voice_rate:int = 20, voice_sound:int = 1, lock=False):
        """This will be used to output tts through the users speakers"""

        # CREATE OBJECT
        engine = pyttsx3.init()
        
        # SET VARIABLES
        rate = engine.getProperty('rate')
        voices = engine.getProperty('voices')



        try:

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
                engine.say(say)
                engine.runAndWait()
            
            

        

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")



class File_Handler():
    """This class will be responsible for pulling information for other module classess"""


    # CLASS VARIABLES
    ip_domain = ()
    ports_open = []
    sub_found = []


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


                # USE THIS FOR DYNAMIC API KEY SELECTION
                if path_api == 1:
                    key = file_path / "api_key_openai"
                
                elif path_api == 2:
                    key = file_path / "api_key_shodan"

                
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
                            "api_key_wpsscan": ""
                        }

                        # PATH WAY TO EXTRACT API_KEYS
                        path = file_path / "api_keys.json"


                        with open(path, "w") as file:
                            json.dump(data, file, indent=4)
                            
                            # LET THE USER KNOW THAT IT WAS SUCCESSFULL
                            console.print("Successfully created default json file", style="bold green")
                            
                    
                    
                    except Exception as e:
                        console.print(f"[bold red]Exception Error:[yellow] {e}")

    
        



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
        

        # SAVE OPEN PORTS FOUND
        elif save_type == 2:
            cls.ports_open = save_data
        

        # SAVE SUBS FOUND
        elif save_type == 3:
            cls.sub_found = save_data
         
        
        # SAVE DIRS FOUND
        elif save_type == 4:
            cls.sub_found = save_data

        

        # NOW TO AGGRAGATE RESULTS AND RETURN IT
        elif save_type == 10:
 
            results = {
                "domain_ip_resolution": cls.ip_domain,
                "open_ports": cls.ports_open,
                "subdomains_found": cls.sub_found,
                "directories_found": "Not Yet in Use"
            }
            
            if verbose:
                console.print(f"\n\n[bold green]Successfully aggragatted results:[white] {results}", style="bold green")


            # RESET CLS VALUES
            cls.ip_domain = ()
            cls.ports_open = []
            cls.sub_found = []

            if verbose:
                console.print(f"Successfully cleaned class values", style="bold red")


            return results
        
        #console.print(f"[bold green]Successfully Saved:[bold blue] {save_data}")








# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":


    use = 3

    if use == 1:
        File_Handler.image_extractor()
    

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



