# NETVULN 2.0 // THIS MODULE WILL HOLD THE LOGIC FOR DIRECTORY ENUMERATION AND MAYBE EVEN DIRECTORY BRUTEFORCING

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
import pyfiglet


# NETWORK IMPORTS
import socket, ipaddress, dns.resolver


# ETC IMPORTS
import threading, time, random, requests
from concurrent.futures import ThreadPoolExecutor


# CONSTANTS & GLOBALS
console = Console()
terminal_width = console.size.width


# FILE HANDLING
from pathlib import Path
import json


    # BASE DIR
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0"
base_dir.mkdir(parents=True, exist_ok=True)






class Requests_Directory_Scanner():
    """This class will be responsible for performing directory enumeration"""

    
    # CLASS VARIABLES
    dirs_up = 0
    dirs_text = ""
    errors = 0 
    current_sub_domain = []
    delete = False          

    # TRACK TOTAL TIME
    time_total_start = 0
    
    # TRACK THREAD LOOP
    subs_given = 0
    subs_finished = 0
    baseline_len_map = ''  # BASELINE FOR 404 WEBPAGES 

    # THIS WILL BE USED TO STORE RESULTS
    results_dir_json = {}
    results_dir_txt = []

    # SET BASE SERVER & X-POWERED-BY
    root_url = ""


    def __init__(self):
        pass


    
    @classmethod
    def track_status_codes(cls, dir, sub=False, get=False, timeout=5):
        """This method will be responsible for keeping track of status codes"""


        # DESTROY ERRORS
        verbose = False

        
        # FORMAT THE CODES
        if get:

            c1 = "bold blue"
            c2 = "bold green"
            c3 = "yellow"

            codes = (
                f"[{c2}]Status Codes: "
                f"[{c3}]200/204:[{c2}] {cls.codes[200]}  "
                f"[{c3}]301/302:[{c2}] {cls.codes[300]}  "
                f"[{c3}]400-403/405:[{c2}] {cls.codes[400]}  "
                f"[{c3}]500/503:[{c2}] {cls.codes[500]}  "

            )

            return codes

        
        # REFRESH THE CLASS DICT
        if sub:
            cls.codes = {}

            cls.codes[200] = 0
            cls.codes[300] = 0
            cls.codes[400] = 0
            cls.codes[500] = 0

            console.print("codes made", style="bold green")


            return


        url = f"https://{dir}"
        

        try:
            response = requests.get(url=url, timeout=timeout ,allow_redirects=False)


            code = response.status_code


            if code in [200,204]:
                cls.codes[200] += 1


            elif code in [301,302]:
                cls.codes[300] += 1


            elif code in [400,401,403,405]:
                cls.codes[400] += 1

            
            elif code in [500,503]:
                cls.codes[500] += 1

            
            if verbose:
                console.print(cls.codes)
        


        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if verbose:
                console.print(f"[bold red]Request Error:[yellow] {e}")


        except Exception as e:
            if verbose:
                console.print(f"[bold red]Exception Error:[yellow] {e}")


    @classmethod
    def track_scans(cls, dir, headers, status_code=False):
        """This class will soley be responsible for creating json file and correctly storing it"""


        count = []
        verbose = False


        if verbose:
            console.print("im in")


        try:

            data = {
            # "dir": dir,
                "status_code": status_code,
                "headers":{

                    "server": headers['server'],
                    "x-powered-by": headers['x-powered-by'],
                    "x-frame-options": headers['x-frame-options'],            # Directly enables clickjacking if missing 
                    "content-security-policy": headers['content-security-policy'],    #  CSP // Missing/weak CSP = easy path to XSS or iframe abuse
                    "strict-transport-policy": headers['strict-transport-policy'],                                  # HSTS // Missing = can allow downgrade attacks or MITM
                    "refer-policy":  headers['refer-policy'],                                                   # Can leak sensitive internal URLs via headers
                    "x-xss-protection": headers['x-xss-protection'],
                    "set-cookie": headers['set-cookie']

                }
            
            }


        except Exception as e:
            console.print(e)


        if verbose:
            console.print("track scans worked", data)


        # NOW TO RETURN DATA
        return dir, data



    @classmethod
    def directory_scanner(cls, sub_domain: str, dir: str, table, session, timeout):
        """This method will be responsible for performing dir scanning"""

        verbose = False
        rep = False


        
        try:

            # MAKE FAKE REQUEST TO 404 PAGE TO GET A BASELINE
            if cls.baseline_len_map == "":
                cls.baseline_len_map = {}

            if sub_domain not in cls.baseline_len_map:
                fake_path = f"https://{sub_domain}/this_should_not_exist_404_test"
                with session as sus:
                    baseline_response = sus.get(url=fake_path, timeout=3, allow_redirects=True)
                cls.baseline_len_map[sub_domain] = len(baseline_response.text)

            baseline_len = cls.baseline_len_map[sub_domain]


            # PERFORM DIR SCAN
            url = f"https://{sub_domain}/{dir}"
            with session as sus:
                response = sus.get(url=url, timeout=timeout, allow_redirects=False)


            content_len = len(response.text)

            
            # USED AS A WAY TO FILTER FOR STATUS CODES
            if response.status_code in [200,204,400,401,403,405,500,503,301,302,307,]:
                rep = True
            

            
            # TRACK THE STAT CODE
            Requests_Directory_Scanner.track_status_codes(dir=f"{sub_domain}/{dir}")


            # CHECK TO MAKE SURE RESPONSE STATUS CODE IS VALID
            if rep and abs(content_len - baseline_len) > 20:

                if verbose:
                    console.print(f"[bold green]Status Code:[yellow] {response.status_code}[/yellow]  -->  [bold red]{url}")
                    time.sleep(5)
            
                    

                else:
                    if cls.delete == False and cls.dirs_up < 25:
                         
                        # VALIDATE HEADERS
                        headers_unvalidated = Requests_Directory_Scanner.get_headers(headers=response.headers)
                        headers_validated = Requests_Directory_Scanner.track_headers(url=sub_domain, headers=headers_unvalidated)

 
                        # ADD SECTION IF ROOT != SUB
                        if headers_validated != "[bold blue]Dir[/bold blue] == [bold green]Sub[/bold green]":
                            table.add_section() 
 
                        # APPEND TO TABLE
                        table.add_row(f"{url}", "-->", f"{response.status_code}", f"{headers_validated}")

                        
                        # AND AGAIN
                        if headers_validated != "[bold blue]Dir[/bold blue] == [bold green]Sub[/bold green]":
                            table.add_section() 

                    
                    elif cls.delete == False:
                        cls.delete = True
                        console.print(f"Found over 25 dir's no longer outputting to terminal, check scan results in saved data for more info", style="bold red")


                    # APPEND TOTAL DIRS FOUND
                    cls.dirs_up += 1



                    # SAVE DATA // TEMP FALSE POS CATCHER
                    if cls.dirs_up < 50:

                        path, data = Requests_Directory_Scanner.track_scans(
                                        dir=f"{sub_domain}/{dir}" ,
                                        headers=headers_unvalidated, 
                                        status_code=response.status_code
                                    )
                        
                        
                        cls.results_dir_json[path] = data   # JSON
                        cls.results_dir_txt.append(f"{sub_domain}/{dir} --> Status Code: {response.status_code}\n")  # TXT

                    elif cls.dirs_up == 51:                       
                        console.print('[bold red]WARNING:[yellow] Over 50 Dirs were found, No longer Adding data in case of False Pos')


                # USE THIS TO TAKE ADVANTAGE OF THE CLASS METHOD
                if sub_domain.split('.')[0] not in cls.current_sub_domain:
                    cls.current_sub_domain.append(sub_domain.split('.')[0])


                    if verbose:
                        console.print(cls.results_dir_txt)
                        console.print(cls.results_dir_json)


            else:
                if verbose:
                    console.print(f"[bold red]False Positive/404-Like Response --> {url} (len: {content_len})", style="bold red")
        

        # CATCH ERRORS
        except requests.Timeout as e:
            if verbose:
                console.print(f"[bold red]Timeout Error:[yellow] {e}")
            cls.errors += 1

        except requests.ConnectionError as e:
            if verbose:
                console.print(f"[bold red]Connection Error:[yellow] {e}")
            cls.errors += 1

        except Exception as e:
            if verbose:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
            cls.errors += 1
      

    @classmethod
    def get_directories(cls, dir_path="1"):
        """This method will be responsible for retrieving dir txt file and returning it"""


        # CREATE FILE PATH
        file_path = Path.home() / "Documents" / "nsm tools" / "network tools" / "NetVuln 2" / "Directories"


        # FOR MAPPING
        paths = {
            "1": "dir_1k.txt",
            "2": "dir_20k.txt",
            "3": "dir_100k.txt"
        }
        

        # GET DIR PATH WAY
        if dir_path == "1":
            path = file_path / "dir_1k.txt"

        elif dir_path == "2":
            path = file_path / "dir_20k.txt"

        elif dir_path == "3":
            path = file_path / "dir_100k.txt"
        
        else:
            path = file_path / "dir_1k.txt"

        
        while True:
            try:

                if base_dir.exists() and file_path.exists() and file_path.is_dir() and path.exists():

                    with open(path, "r") as file:
                        content = [dir.strip() for dir in file]

                        console.print(f"\n\n[bold green]Successfully Retrieved:[/bold green] [bold red]{paths[dir_path]}[/bold red] from [bold blue]{path} \n")
                        time.sleep(1)
                        
                        cls.dirs_text = content
                        return content
                    
                
                # USE THIS ELSE STATEMENT TO CREATE FILE PATHS
                else:


                    # CREATE BASE DIR
                    base_dir.mkdir()

                    # CREATE FILE PATH
                    file_path.mkdir()

            

            except FileNotFoundError as e:
                console.print(f"[bold red]File not found Error:[yellow] {e}")
                time.sleep(3)
                break



            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")


    @classmethod
    def threader(cls, sub_domain: str, dir_path="1", thread_count=250, timeout=1, delay=1):
        """This method will be responsible for using the directory_scanner <-- and threading through it"""
         

        # PULL DIR AND STORE IT WITHIN A LIST
        if cls.dirs_text == "":
            directories = Requests_Directory_Scanner.get_directories(dir_path=str(dir_path))
            #total_directories = len(directories)

            # TRACK TIME
            cls.time_total_start = time.time()

        
        # NO NEED TO KEEP PULLING INFO
        else:
            directories = cls.dirs_text
           # total_directories = len(cls.dirs_text)
            cls.delete = False

        
        # GET SUB
        sub = sub_domain.split('.')[0]

        
        
        # CREATE TABLE FOR INFO
        table = Table(title=f"Directory Scan --> {sub}", title_style="bold red", header_style="bold red", style="bold purple")
        table.add_column("Directory", style="bold blue")
        table.add_column("-->", style="bold red")
        table.add_column("Status Code", style="bold green")
        table.add_column("Header Info")


        # KEEP TRACK OF TIME
        time_start = time.time()
        cls.delete = False
        lol = 0

        
        try:
            with Live(table, console=console, refresh_per_second=.01, transient=cls.delete ): 

                # REQUEST SESSION
                with requests.Session() as sus:
                    with ThreadPoolExecutor(max_workers=thread_count) as executor:
                        for dir in directories:
                            executor.submit(Requests_Directory_Scanner.directory_scanner, sub_domain, dir, table, sus, timeout)
                            
                            # SLOW DOWN BUDDY // LOL
                            if lol == 30:
                                time.sleep(delay)
                                lol = 0
                            
                            time.sleep(.01) # TO PREVENT RENDER FUCKUPS
                            lol += 1

                        
        
        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")
                


        # GET FINAL TIME
        time_took = time.time() - time_start


        # TOTAL TIME
        cls.subs_finished += 1

        # PRINT DIR INFO
        console.print(f"[bold blue]Total chosen dirs found:[/bold blue] {cls.dirs_up}/{len(cls.dirs_text)}   ",
                      Requests_Directory_Scanner.track_status_codes(get=True, dir=False)    # PRINT STATUS CODES
                      )


        


        # OUTPUT OR CONTINUE
        if cls.subs_given == cls.subs_finished:

            time_total_took = time.time() - cls.time_total_start

            
            console.print(f"\n\n\n[bold red]Subs with Active Dirs:[bold green] {cls.current_sub_domain}\n")
            # PANEL FOR FINAL STATS
            results = (
                f"[bold green]Total Sub-domains with active Directories:[/bold green] {len(cls.current_sub_domain)} out of {(cls.subs_given)}    "
                #f"[bold green]Total Directories Found:[/bold green] {cls.dirs_up}/{total_directories}    "
                f"[yellow]Total Threads Used:[/yellow] {thread_count}    "    
                f"[bold red]Total Errors Occurred:[/bold red] {cls.errors}    "    
                f"[bold blue]Total Elapsed Time:[/bold blue] {time_total_took:.2f} Seconds"
            )
        
        
        
            panel = Panel(title="Scan Results", style="bold purple", expand=False, renderable=results, border_style="bold green")
            console.print(panel)
            cls.errors = 0
        

        else:
            print("\n")


        # RESET DIRECTORIES FOUND  // ERRORS
        cls.dirs_up = 0
        cls.delete = False
    
    
    @staticmethod
    def get_headers(headers:str, verbose=False):
        """This method will be responsible for actually pulling the header info"""


        # DESTROY ERRORS
        verbose = verbose


        # ITER THROUGH HEAD
        data = {}
        valid_keys = [
                "server", "x-powered-by", "x-frame-options",
                  "content-security-policy", "strict-transport-policy", "refer-policy" ,
                  "x-xss-protection", "set-cookie"
                ]



        # PARSE DATA
        for key, value in headers.items():

            if key.strip().lower() in valid_keys:
                data[key.strip().lower()] = value if value else "Missing"


        # FOR KEYS NOT GIVEN
        for key in valid_keys:

            if key not in data:
                data[key] = "Missing"

        
        if verbose:
            console.print(data)

        
        # RETURN DATA
        return data


    @classmethod
    def track_headers(cls, url:str, timeout=3, headers=False):
        """
        This method will be responsible for seeing if the dir headers is equal to or differnt then the root headers
        """


        # DESTROY ERROS
        verbose = False
        cls.failed = False

        

        if cls.root_url != url:


            # IMPORTANT VARIABLES // LEARN THESE HEADERS AND THE ATTACKS ASSOCIATED WITH THEM VIA EXPLOIT
            cls.server = ""
            cls.x_powered_by = ""
            cls.x_frame_options = ""         # Directly enables clickjacking if missing 
            cls.content_security_policy = ""  #  CSP // Missing/weak CSP = easy path to XSS or iframe abuse
            cls.strict_transport_policy = ""  # HSTS // Missing = can allow downgrade attacks or MITM
            cls.refer_policy = ""           # Can leak sensitive internal URLs via headers
            cls.x_xss_protection = ""
            cls.set_cookie = ""


            # I AM ROOT
            cls.root_url = url


            if verbose:
                console.print(f"Successfully changed root_url --> {url}", style="bold green")


            # VALID KEYS
            valid_keys = [
                "server", "x-powered-by", "x-frame-options", 
                "content-security-policy", "strict-transport-policy", "refer-policy",
                "x-xss-protection", "set-cookie"
                ]
            
            valid_status_codes = [200, 301, 302, 403]

            
            # GIVE THE PROGRAM 3 TRIES TO TRY AND REACH THE SUB // THESE HEADERS ARE IMPORTANT // LOL 
            loop = 1

            while True:
                try:
                    
                    
                
                    # GET ROOT HEADERS
                    root_url = f"https://{url}"
                    response = requests.get(url=root_url, timeout=timeout, allow_redirects=False)

                    if response.status_code in valid_status_codes:

                        # GET HEADERS AND GET TO PARSING
                        data = {}
                        headers = response.headers
                        
                        
                        if verbose:
                            console.print("got a valid status code")


                        # PARSE DATA
                        for key, value in headers.items():

                            if key.strip().lower() in valid_keys:
                                data[key.strip().lower()] = value if value else "Missing"


                        # FOR KEYS NOT GIVEN
                        for key in valid_keys:

                            if key not in data:
                                data[key] = "Missing"
                        
                        
                        
                        # MAP METHOD VARIABLES FOR ELSE TRIGGERS
                        cls.server = data.get('server', 'Not Found')
                        cls.x_powered_by = data.get('x-powered-by', 'Not Found')
                        cls.x_frame_options = data.get('x-frame-options', 'Missing')
                        cls.content_security_policy = data.get('content-security-policy', 'Missing')
                        cls.strict_transport_policy = data.get('strict-transport-policy', 'Missing')
                        cls.refer_policy = data.get('refer-policy', 'Missing')
                        cls.x_xss_protection = data.get('x-xss-protection', "Missing")
                        cls.set_cookie = data.get('set-cookie', "Missing")
                        


                        if verbose:
                            console.print(data)


                        
                        # OUTPUT SUB HEADERS
                        console.print(f"[bold green]Sub Headers:[/bold green] {data}")

                        break

                    else:
                        console.print("Root sub was not a valid status code\nSwitching Sub to != Dir")
                        cls.failed = True
                        break


                
                except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:

                    if verbose:
                        console.print(f"[bold red]Requests Timeout or Connection Error:[yellow] {e}")

                    if loop < 3:
                        console.print("[bold green]Failed to get sub headers: [yellow]Reattempting...", style='yellow')
                        loop += 1
                        timeout +=1
                    
                    else:
                        console.print("[bold green]3 Failed Attempts: [yellow]I GIVE UP\nDir output by default will be Dir != Sub")
                        cls.failed = True # TELL THE ELIF STATEMENT TO SHOW HEADERS // ROOT != SUB
                        break

                except Exception as e:
                    console.print(f"[bold red]Exception Error:[yellow] {e}")
                    console.print("Dir output by default will be Dir != Sub")
                    cls.failed = True # TELL THE ELIF STATEMENT TO SHOW HEADERS // ROOT != SUB
                    break
        

        
        # CHECK IF DIR_HEADERS == ROOT_HEADERS
        elif headers:


            try:
                # IF ALL FIELDS ARE VALID
                root_sub = 0
                
                # SET CHECKERS
                headers_server = True if cls.server == headers['server'] else False
                headers_x_powered_by = True if cls.x_powered_by == headers['x-powered-by'] else False

                
                # IF ANY OF THESE GIVE FALSE COULD BE SIGN OF A VULN
                headers_x_frame_options = True if cls.x_frame_options == headers['x-frame-options'] else False
                headers_content_security_policy = True if cls.content_security_policy == headers['content-security-policy'] else False
                headers_strict_transport_policy = True if cls.strict_transport_policy == headers['strict-transport-policy'] else False
                headers_refer_policy = True if cls.refer_policy == headers['refer-policy'] else False
                headers_x_xss_protection = True if cls.x_xss_protection == headers['x-xss-protection'] else False
                headers_set_cookie = True if cls.set_cookie == headers['set-cookie'] else False
            
            except Exception as e:
                console.print(e)


    

            # AGGREGATE RESULTS
            sub_data = {
                "Server": headers_server,
                "x-powered-by": headers_x_powered_by,
                "x-frame-options": headers_x_frame_options,
                "content-security-policy": headers_content_security_policy,
                "strict-transport-policy": headers_strict_transport_policy,
                "refer-policy": headers_refer_policy,
                "x-xss-protection": headers_x_xss_protection,
                "set-cookie": headers_set_cookie
            }

            
     
            # THIS WILL TELL THE USER IF SERVER & X-POWERED-BY != ROOT
            if headers_server == True and headers_x_powered_by == True:

                if verbose:
                    console.print(f"server is: {headers_server} & x-powered-by is: {headers_x_powered_by}")


                root_sub += 1
            
            else:

                if verbose:
                    console.print(f"[bold red]server and x-powered-by are not Valid[/bold red]\nRoot != Sub\nServer: {headers_server}  -  X-Powered-By: {headers_x_powered_by}")
            
            

            # FOR OTHER SECURITY HEADERS
            try:
                if headers_x_frame_options == True and headers_content_security_policy == True and headers_strict_transport_policy == True and headers_refer_policy == True and headers_x_xss_protection == True and headers_set_cookie == True:

                    if verbose:
                        console.print(f"Server Security Headers are Valid\n Root == Sub")
                    

                    root_sub += 1
                
                else:

                    if verbose:
                        console.print(f"[bold red]Server Security Headers are not Valid[/bold red]\nRoot != Sub\n{sub_data}")
            
            except Exception as e:
                console.print(e)

            

            # GENERAL DEBUGGING
            if verbose:
                console.print(f"Validation: {sub_data}")
            

            # FORMAT OUTPUT FOR ROOT != SUB
            sub_return = [
                f"Server: {headers['server']}   |   X-Powered-By: {headers['x-powered-by']}",
                f"X-Frame-Options: {headers['x-frame-options']}  |   Content-Security-Policy: {headers['content-security-policy']}",
                f"Strict-Transport-Policy: {headers['strict-transport-policy']}   |   Refer-Policy: {headers['refer-policy']}",
                f"X-Xss-Protection: {headers['x-xss-protection']}   |   Set-Cookie: {headers['set-cookie']}"
            ]
             
            sub_return = '\n'.join(sub_return)
            
            
            # THIS WILL ACTIVATE IF THE SUB HEADER FAILED TO CAPTURE // MAKING ROOT != SUB BY DEFAULT
            if cls.failed:
                root_sub = 0
                cls.failed = False
            
            
            # FOR TESTING
            RANDOM = False
            
            if RANDOM:
                from random import randint

                root_sub = randint(0,2) # USE THIS TO TEST LOGIC 



            return "[bold blue]Dir[/bold blue] == [bold green]Sub[/bold green]" if root_sub == 2 else sub_return 
       
        
        

        # IF HEADERS != TRUE
        else:

            console.print(f"Failed to find valid headers --> {url} ")
            return "[bold red]No valid headers was given or found"

            
    
    @classmethod
    def main(cls, sub_domains:str, dir_path="1", thread_count=2000, delay=.7, timeout=1) -> list:
        """This method will be responsible for handling class wide logic"""


        # CLEANSE DATA // PREVENT FUCKUPS
        cls.results_dir_json = {}
        cls.results_dir_txt = []
        cls.dirs_text = ""
        cls.subs_given = 0
        cls.subs_finished = 0
        cls.current_sub_domain = []


        # CHECK TO MAKE SURE LIST IS VALID
        if sub_domains:


            # ERROR DESTROYER
            verbose = False


            # FOR THREADER PANEL CONTROL
            cls.subs_given = len(sub_domains)


            try:
                

                # ITERATE THROUGH EACH SUBDOMAIN WE HAVE AND FOR EACH ITERATE THROUGH DIRECTORIES
                for domain in sub_domains:
                    
                    # DELAY TO PREVENT OVERWHELMING
                    time.sleep(delay)


                    # SET STATUS CODE TRACKER
                    Requests_Directory_Scanner.track_status_codes(sub=domain, dir=False)

                    Requests_Directory_Scanner.track_headers(url=domain,timeout=3) # TRACK THAT BIHc
                    Requests_Directory_Scanner.threader(sub_domain=domain, thread_count=thread_count, dir_path=dir_path, timeout=timeout, delay=delay)


                    Requests_Directory_Scanner.root_url = ""   # RESET ROOT FOR NEXT SUBDOMAIN

                    
                if verbose:
                    console.print(f"JSON Results: {cls.results_dir_json}")
                    console.print(f"TEXT Results: {cls.results_dir_txt}")

                
                # FORMAT DATA
                cls.results_dir_txt = '\n'.join(cls.results_dir_txt)
                
                # SAVE DATA --> FILE STORING
                from nsm_settings import File_Saving
                File_Saving.push_info(save_data=[cls.results_dir_json, cls.results_dir_txt], save_type="5")



                # DISCORD SUMMARY --> FILE SENDING
                from nsm_utilities import File_Handler
                data = (f"Total Subs with active Dirs: {len(cls.current_sub_domain)} out of {cls.subs_given}")
                File_Handler.push_info_to_discord(save_data=data, save_type=3)


                
                # RETURN SAVE DATA 
                return cls.results_dir_json, cls.results_dir_txt
            

            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")
                
        

        else:
            console.print("\n[bold red]Directory Enumeration Skipped Due To:[yellow] No Sub-Domains given")
            return ["None", "None"]




# THIS CLASS IS DEAPPRECIATED // USE THE Request_Directory_Scanner <--  for functional directory enumeration
class Resolver_Directory_Scanner():

    """This class will be responsible for performing directory lookups using the dns.resolver libary"""

    # CLASS VARIABLES
    dirs_up = 0
    current_sub_domain = []


    # SAVE DIRS FOUND // INFO
    found_dirs_txt = []
    found_dirs_json = {}

    def __init__(self):
        pass

    
    @classmethod
    def directory_resolver(cls, sub_domain:str, dir:str, table):
        """This is where all the magic will happen and by magic i mean directory enumeration"""
        

        # CONTROL ERROR MESSAGES
        verbose = True

        # MARK THIS DIR
        if sub_domain.split('.')[0] not in cls.current_sub_domain:
            cls.current_sub_domain.append(sub_domain.split('.')[0])

        
        try:

            # USE THE DNS LIBARY
            domain = f"{sub_domain}/{dir}"
            rdata = dns.resolver.resolve(domain, "A")
            

            # ITERATE THROUGH RESULTS
            if rdata:
                for r in rdata:
                    table.add_row(f"{sub_domain}", "-->" , f"{r}" )


                    # SAVE DATA
                    #cls.found_dirs_txt.append(f"")
        

        except Exception as e:

            if verbose:
                console.print(f"[bold red]Exception Error:[yellow] {e}")

    

    @classmethod
    def get_directories(cls, dir_path="1"):
        """This method will be responsible for retrieving dir txt file and returning it"""


        # CREATE FILE PATH
        file_path = Path.home() / "Documents" / "nsm tools" / "network tools" / "NetVuln 2" / "Directories"


        # FOR MAPPING
        paths = {
            "1": "dir_1k.txt",
            "2": "dir_20k.txt",
            "3": "dir_100k.txt"
        }
        

        # GET DIR PATH WAY
        if dir_path == "1":
            path = file_path / "dir_1k.txt"

        elif dir_path == "2":
            path = file_path / "dir_20k.txt"

        elif dir_path == "3":
            path = file_path / "dir_100k.txt"
        
        else:
            path = file_path / "dir_1k.txt"

        
        while True:
            try:

                if base_dir.exists() and file_path.exists() and file_path.is_dir() and path.exists():

                    with open(path, "r") as file:
                        content = [dir.strip() for dir in file]

                        console.print(f"\n\n[bold green]Successfully Retrieved:[/bold green] [bold red]{paths[dir_path]}[/bold red] from [bold blue]{path} \n")
                        time.sleep(1)

                        return content
                    
                
                # USE THIS ELSE STATEMENT TO CREATE FILE PATHS
                else:


                    # CREATE BASE DIR
                    base_dir.mkdir()

                    # CREATE FILE PATH
                    file_path.mkdir()

            

            except FileNotFoundError as e:
                console.print(f"[bold red]File not found Error:[yellow] {e}")
                time.sleep(3)
                break



            except Exception as e:
                console.print(f"[bold red]Exception Error:[yellow] {e}")



    @classmethod
    def threader(cls,sub_domain:str, thread_count=250, dir_path="1"):
        """Use this method to thread through the directory_resolver <-- instances"""


         # PULL DIR AND STORE IT WITHIN A LIST

        directories = Resolver_Directory_Scanner.get_directories(dir_path=str(dir_path))
        total_directories = len(directories)

        
        
        # CREATE TABLE FOR INFO
        table = Table(title="Directory Scan", title_style="bold red", header_style="bold red", style="bold purple")
        table.add_column("Domain", style="bold blue")
        table.add_column("-->", style="bold red")
        table.add_column("Directory", style="bold green")


        # KEEP TRACK OF TIME
        time_start = time.time()

        with Live(table, console=console, refresh_per_second=8, transient=False) as live: 
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for dir in directories:
                    executor.submit(Resolver_Directory_Scanner.directory_resolver, sub_domain, dir, table)
                
                    if cls.current_sub_domain > 500:
                        live.transient = True
                        console.print("False Positive Triggered, Results will be Destroyed", style="bold red")


                


        # GET FINAL TIME
        time_took = time.time() - time_start

        
        # PANEL FOR FINAL STATS
        results = (
            f"[bold green]Total Sub-domains with active Directories:[/bold green] {len(cls.current_sub_domain)}    "
            f"[bold green]Total Directories Found:[/bold green] {cls.dirs_up}/{total_directories}    "
            f"[yellow]Total Threads Used:[/yellow] {thread_count}    "    
            f"[bold blue]Elapsed Time:[/bold blue] {time_took:.2f} Seconds"
        )

        panel = Panel(title="Scan Results", style="bold purple", expand=False, renderable=results, border_style="bold green")
        console.print(panel)


        # RESET DIRECTORIES FOUND 
        cls.dirs_up = 0
    


    @staticmethod
    def main(sub_domains:str):
        """This method will be responsible for calling upon module wide logic"""


        # SET VARIABLES
        thread_count = 250

        dir_path = "1"


        # CHECK FOR IF SUBDOMAINS WAS GIVEN
        if sub_domains:

            for domain in sub_domains:
                Resolver_Directory_Scanner.threader(sub_domain=domain,thread_count=thread_count, dir_path=dir_path)
        
        
        # IF NOTHING WAS GIVEN 
        else:
            console.print("[bold red]Dir Enumeration Skipped Due:[yellow] to no Subs given")
            





if __name__ == "__main__":

    use = 1


    if use == 1:

        from nsm_target_scanner import Requests_Subdomain_Scanner

        url = "GMAIL.com"
        
        subs = Requests_Subdomain_Scanner.main(target=url)
        Requests_Directory_Scanner.main(sub_domains=subs)

    

    elif use == 3:


        url = "https://weseeuinc.org/wp-admin"
        

        use = False
        if use:
            response = requests.get(url=url, allow_redirects=True)

            for key, value in response.headers.items():

                console.print(f"{key} --> {value}")


        
        headers = {
            "log": "password",
            "pwd": "123"
        }
        print("\n\n")
        response = requests.post(url=url, json=headers)
        console.print(response.status_code,"\n\n") 
        for key, val in response.headers.items():

            console.print(f"{key} --> {val}")
    







        