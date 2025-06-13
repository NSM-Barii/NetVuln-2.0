# NETVULN 2.0 // THIS MODULE WILL BE RESPONSIBLE FOR OUTPUTTING END USER UI

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
from nsm_utilities import Utilities, NetTilities
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






class MainUI():
    """This class will be responsible for controlling how and when the ui is outputted"""

    def __init__(self):
        pass

    
     
    @staticmethod
    def main_title():
        """This method will be responsible for creating the main menu welcome message"""


        # CLEAR SCREEN
        Utilities.clear_screen()
        
        

        # LOOK FOR A FONT
        look = False


        if look == False:
            art = pyfiglet.figlet_format(text="        Net\n  Vuln 2.0", font="dos_rebel")
            artt = pyfiglet.figlet_format(text="      2.0", font="dos_rebel")

            console.print(f"\n\n{art}", style="bold blue")
            #console.print(f"{artt}\n\n\n", style="bold red")

        
        elif look:

            count = 0 
            colors = {
            "1": "bold red",
            "2": "bold red",
            "3": "bold blue",
            "4": "cyan",
            "5": "yellow"
        }

            while True:
                fonts = pyfiglet.FigletFont.getFonts()

                for f in fonts:

                    color = colors[str(random.randint(1,5))]
                    
                    art = pyfiglet.figlet_format(text="NetVuln 2.0", font=f)
                    console.print(f"Current Font: {f}\n{art} \n",style=color)
                    time.sleep(1.5)

                    if count == 5:
                        console.input("[bold green]\n\nPress Enter to Continue: ")
                        count = 0

                    count += 1

 
    

    @staticmethod
    def main_menu():
        """This method will be responsible for directing user to appropiate direction"""



        # PRINT MAIN MENU
        MainUI.main_title()
        print("\n\n\n\n\n")


        # CHOOSE COLOR
        color_out = "[bold red]"
        color_in = "[bold blue]"



        # CREATE OPTIONS
        options = (
            f"      {color_out}[1] {color_in}Perform Vulnerability Scan\n"
            f"      {color_out}[2] {color_in}Not Bound\n\n"
            f"      {color_out}[3] {color_in}Scan Results\n\n"
            f"      {color_out}[4] {color_in}About\n"
            f"      {color_out}[5] {color_in}Help\n"
            f"      {color_out}[6] {color_in}Settings\n\n"
            f"      {color_out}[7] {color_in}EXIT\n"

        ) 
        
        # CREATE CLEAR SCREEN OPTIONS
        cc = ["1"]
        error = False
        construction = False
    
        console.print(options)


        while True:

            # FOR ERRORS
            if error:
                console.print(f"\n[bold red]    EHH:[yellow] {choice}[bold red] Is not a valid choice, please pick between [bold green](1-7)!")
            
            elif construction:
                console.print("\n    This option is under construction, come back later", style="yellow")
                construction = False

            else:
                print("")

            

            # USER SELECTION 
            choice = console.input("[bold red]    Enter Your Choice Here: ").strip().lower()
            
            if choice in cc:
                Utilities.clear_screen()


            if choice == "1":
                Module_Controller.controller()

                break


            elif choice == "2":
                construction = True

            
            # FOR SCAN RESULTS
            elif choice == "3":
                construction = True


            
            # ABOUT 
            elif choice == "4":
                construction = True

            
            # HELP
            elif choice == "5":
                construction = True
            

            # SETTINGS
            elif choice == "6":
                construction = True


            # FOR EXIT
            elif choice == "7":
                console.print("\n    See you later.....",style="bold blue")
                time.sleep(2)
                exit()
           
            

            # EXCEPTIONS
            else:
                #console.print(f"[bold red]    EHH:[yellow] {choice}[bold red] Is not a valid choice, please pick between(1-7)!")
                error = True

    


    def main():
        """This method will be responsible for looping through core procedures"""

        
        # LOOP THROUGH MULTI-MODULE PROGRAM LOGIC
        while True:
            Utilities.clear_screen()
            NetTilities.get_conn_status()
            MainUI.main_menu()








# FOR MODULE TESTING
if __name__ == "__main__":
    MainUI.main()
