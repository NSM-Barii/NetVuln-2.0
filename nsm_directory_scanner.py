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
    subs_with_dirs = 0
    current_sub_domain = []


    def __init__(self):
        pass


    @classmethod
    def directory_scanner(cls, sub_domain: str, dir:str, table, session):
        """This method will be responsible for performing dir scanning"""


        verbose = False
        

        try:
            url = f"https://{sub_domain}/{dir}"
            
            with session as sus:
                response = sus.get(url=url, timeout=3, allow_redirects=True)

            

            if response.status_code == 200:


                if verbose:
                    console.print(f"[bold green]Status Code:[yellow] {response.status_code}[/yellow]  -->  [bold red]{url}")
                    time.sleep(5)
                
                
                else:
                    table.add_row(f"{sub_domain}", "-->", f"{url}")


                    # APPEND TOTAL DIRS FOUND
                    cls.dirs_up += 1
                
                
                # USE THIS TO TAKE ADVANTAGE OF THE CLASS METHOD
                if sub_domain.split('.')[0] not in cls.current_sub_domain:
                    cls.current_sub_domain.append(sub_domain.split('.')[0])
                    console.print(cls.current_sub_domain)



            else:

                if verbose:
                    console.print(f"[bold red]Status Code:[yellow] {response}  -->  [bold blue]{url}", style="bold red")



        # CATCH ERRORS
        except requests.Timeout as e:
            console.print(f"[bold red]Timeout Error:[yellow] {e}")


        except requests.ConnectionError as e:
            console.print(f"[bold red]Connection Error:[yellow] {e}")
        

        except Exception as e:
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
    def threader(cls, sub_domain: str, thread_count=250, dir_path="1"):
        """This method will be responsible for using the directory_scanner <-- and threading through it"""

        

        # PULL DIR AND STORE IT WITHIN A LIST

        directories = Requests_Directory_Scanner.get_directories(dir_path=str(dir_path))
        total_directories = len(directories)

        
        
        # CREATE TABLE FOR INFO
        table = Table(title="Directory Scan", title_style="bold red", header_style="bold red", style="bold purple")
        table.add_column("Domain", style="bold blue")
        table.add_column("-->", style="bold red")
        table.add_column("Directory", style="bold green")


        # KEEP TRACK OF TIME
        time_start = time.time()

        with Live(table, console=console, refresh_per_second=100, transient=False): 

            # REQUEST SESSION
            with requests.Session() as sus:
                with ThreadPoolExecutor(max_workers=thread_count) as executor:
                    for dir in directories:
                        executor.submit(Requests_Directory_Scanner.directory_scanner, sub_domain, dir, table, sus)
                


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



    
    @classmethod
    def main(cls, sub_domains:str) -> list:
        """This method will be responsible for handling class wide logic"""



        # SET PARAMS
        thread_count = 500
        dir_path = "1"


        try:
            
            # ITERATE THROUGH EACH SUBDOMAIN WE HAVE AND FOR EACH ITERATE THROUGH DIRECTORIES
            for domain in sub_domains:

                Requests_Directory_Scanner.threader(sub_domain=domain, thread_count=thread_count, dir_path=dir_path)

        

        except Exception as e:
            console.print(f"[bold red]Exception Error:[yellow] {e}")



class Resolver_Directory_Scanner():
    """This class will be responsible for performing directory lookups using the dns.resolver libary"""

    # CLASS VARIABLES
    dirs_up = 0
    current_sub_domain = []

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

        with Live(table, console=console, refresh_per_second=8, transient=False): 
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for dir in directories:
                    executor.submit(Resolver_Directory_Scanner.directory_resolver, sub_domain, dir, table)
                


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


        for domain in sub_domains:
            Resolver_Directory_Scanner.threader(sub_domain=domain,thread_count=thread_count, dir_path=dir_path)
            





if __name__ == "__main__":

    use = 1

    if use == 1:
        
        sub_domains = ["youtube.com", "files.google.com", "printer.discord.com", "blog.discord.com", "admin.google.com", "app.discord.com", "blog.google.com", "google.com"]
        Requests_Directory_Scanner.main(sub_domains=sub_domains)
    

    if use == 2:

        sub_domains = ["youtube.com", "files.google.com", "printer.discord.com", "blog.discord.com", "admin.google.com", "app.discord.com", "blog.google.com", "google.com"]
        Resolver_Directory_Scanner.main(sub_domains=sub_domains)


        






        