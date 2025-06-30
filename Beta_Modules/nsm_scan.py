# NETVULN 2.0 // THIS MODULE WILL HOUSE THE LOGIC FOR THE TYPE OF SCAN U WILL BE DOING

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



# NSM IMPORTS
from nsm_target_scanner import Module_Controller


# CONSTANTS & GLOBALS
console = Console()
terminal_width = console.size.width


# FILE HANDLING
from pathlib import Path
import json


    # BASE DIR
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0"
base_dir.mkdir(parents=True, exist_ok=True)




class Scan_Controller():
    """This class will be responsible for directing the user towards either a default scan or custom scan of there choosing"""


    # TESTING
    verbose = True



    # 1 == scan_type=1, sub_path=1, dir_path=1
    # 2 == scan_type=2, sub_path=2, dir_path=2
    # 3 == scan_type=2, sub_path=3, dir_path=3


    def __init__(self):
        pass



    @classmethod
    def scan_type_default_1(cls):
        """This method will do a default scan otherwise known as --> scan_type == 1 <-- """


        # FOR TESTING
        if cls.verbose:
            console.print("Scan_type_1 selected")


        # DEFAULT SCAN 
        Module_Controller.controller(scan_type=1, sub_path="1", dir_path="1")


        # 1 == scan_type=1, sub_path=1, dir_path=1

        # PORT SCAN == 1-1024 PORTS
        # SUB ENUM == 1K SUB LIST
        # DIR ENUM == 1K DIR LIST

    
    @classmethod
    def scan_type_default_2(cls):
        """This method will do a defualt scan, type 2"""

        # FOR TESTING
        if cls.verbose:
            console.print("Scan_type_2 selected")


        # DEFAULT SCAN TYPE 2
        Module_Controller.controller(scan_type=2, sub_path="2", dir_path="2")


        # 2 == scan_type=2, sub_path=2, dir_path=2

        # PORT SCAN == 1-1024 PORTS
        # SUB ENUM == 1K SUB LIST
        # DIR ENUM == 1K DIR LIST

    
    @classmethod
    def scan_type_default_3(cls):
        """This method will do a default scan, type 3"""

        # FOR TESTING
        if cls.verbose:
            console.print("Scan_type_3 selected")


        # DEFAULT SCAN TYPE 3
        Module_Controller.controller(scan_type=2, sub_path="3", dir_path="3")

        
        # 1 == scan_type=2, sub_path=3, dir_path=3

        # PORT SCAN == 1-1024 PORTS
        # SUB ENUM == 1K SUB LIST
        # DIR ENUM == 1K DIR LIST

    
    @classmethod
    def scan_type_custom(cls):
        """This is where the user will have close to full control over scanner settings"""


        # FOR NESTED FUNCTIONS
        verbose = cls.verbose


        # FOR TESTING
        if cls.verbose:
            console.print("Scan_type_custom selected")
        

        # COLOR VARS
        c1 = "bold blue"
        c2 = "bold green"
        c3 = "bold yellow"

        # DEFAULT SELECTION MESSAGE
        default = f"[yellow]Invalid choice given, [bold green]Value = 1"



        # CREATED HELPER FUNCTIONS FOR SMOOTHER & CLEANER LOGIC
        @staticmethod
        def helper_portscan():
            """This will be used to determine what port the user wants"""
            

            try:
                choice = console.input(f"[{c1}]Port Scan [{c2}](1 or 2)?: ").strip().lower()


                # FOR TESTING
                if verbose:
                    console.print(f"user_choice: {choice}")

                
                # TYPE 1
                if choice == "1":
                    
                    return 1
                

                # TYPE 2
                elif choice == "2":

                    return 2
                

                # UR GOOFY
                else:

                    # TELL THE USER HOW SLOW THEY ARE
                    console.print(default)
                    return 1
            
            
            except Exception as e:
                console.print(f"[bold red]nsm_scan Module Error:[yellow] {e}")

        
        @staticmethod
        def helper_subdomain():
            """This will be used to determine what sub path to retrieve"""


            try:

                choice = console.input(f"[{c1}]Sub Path [{c2}](1, 2 or 3)?: ").strip().lower()


                # FOR TESTING
                if verbose:
                    console.print(f"user_choice: {choice}")


                # SUB PATH 1
                if choice == "1":

                    return "1"
                
                
                # SUB PATH 2
                elif choice == "2":

                    return "2"
                

                # SUB PATH 3
                elif choice == "3":

                    return "3"
                
                
                # UR GOOFY
                else:
                    
                    # TELL THE USER HOW SLOW THEY ARE
                    console.print(default)

                    return "1"
            

            except Exception as e:
                console.print(f"[bold red]nsm_scan Module Error:[yellow] {e}")

        
        @staticmethod
        def helper_directory():
            """This will be used to determine what dir path to retrieve"""



            try:

                choice = console.input(f"[{c1}]Dir Path [{c2}](1, 2 or 3)?: ").strip().lower()


                # FOR TESTING
                if verbose:
                    console.print(f"user_choice: {choice}")

                
                # DIR PATH 1
                if choice == "1":

                    return "1"
                
                
                # DIR PATH 2
                elif choice == "2":

                    return "2"
                
                
                # DIR PATH 3
                elif choice == "3":

                    return "3"
                
                
                # UR GOOFY
                else:
                    
                    # TELL THE USER HOW GOOFY THEY ARE
                    console.print(default)

                    return "1"


            except Exception as e:
                console.print(f"[bold red]nsm_scan Module Error:[yellow] {e}")        


    


        # BACK TO MAIN LOGIC
        choice_port_scan = helper_portscan() # PORT SCAN TYPE

        choice_sub_path = helper_subdomain() # SUB PATH

        choice_dir_path = helper_directory() # DIR PATH




        # FOR TESTING
        if cls.verbose:
            console.print(
                f"user_choices: {choice_port_scan}"
                f" {choice_sub_path}"
                f" {choice_dir_path}"
            
            )


        # INPUT VARIABLES
        Module_Controller.controller(
            scan_type= choice_port_scan,
            sub_path= str(choice_sub_path),
            dir_path= str(choice_dir_path) 
        )


    @classmethod
    def controller(cls):
        """This will control the direction the scan goes in"""


        # THE USERS CHOICES 
        choices = (
            f"1 == scan_type_1\n"
            f"2 == scan_type_2\n"
            f"3 == scan_type_3\n"
            f"4 == custom_scan\n"
            f"else == scan_type_1\n"
        )


        choices_panel = Panel(
            choices,
            expand=False,
            style="bold red",
            border_style="bold green",
            title="Options"
        )
        
        
        # NOW OUTPUT DEM CHOICES
        print("\n\n")
        console.print(choices_panel)
        print("\n\n\n")


        choice = console.input("[bold red]Enter scan type: ")



        # FOR TESTING
        if cls.verbose:
            console.print(f"user_choice: {choice}")

        
        
        # 1-3 == DEFAULT SCANS
        if choice == "1":
            Scan_Controller.scan_type_default_1()


        elif choice == "2":
            Scan_Controller.scan_type_default_2()
        

        elif choice == "3":
            Scan_Controller.scan_type_default_3()

        
        # CUSTOM SCAN
        elif choice == "4":
            Scan_Controller.scan_type_custom()

        
        
        # GOOFY SCAN
        else:

            console.print("your goofy")

            # DEFAULT THEY ASS
            Scan_Controller.scan_type_default_1()














