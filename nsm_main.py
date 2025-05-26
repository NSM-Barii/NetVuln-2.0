# NETVULN 2.0 // THIS MODULE WILL BE RESPONSIBLE FOR MAKING SURE THE USER HAS ALL NECESSARY DEPENDENCIES AND PERFORM MULTI-MODULE LOGIC




class  Import_Handler():
    """This class will be responsible for making sure the user has all the necessary dependencies installed"""



    def __init__(self):
        pass



    def Import_checker():
        """This will try to import all needed libaries"""

        
        try:

            # UI IMPORTS
            import dns.exception
            from rich.panel import Panel
            from rich.table import Table
            from rich.live import Live
            from rich.console import Console
            import pyfiglet


            # NETWORK IMPORTS
            import socket, ipaddress, dns.resolver


            # ETC IMPORTS
            import threading, time, random, requests, os
            from concurrent.futures import ThreadPoolExecutor
            import pyttsx3
            from plyer import notification




            # NSM IMPORTS
            from nsm_utilities import Utilities
            from nsm_directory_scanner import Requests_Directory_Scanner


            # CONSTANTS & GLOBALS
            console = Console()
            terminal_width = console.size.width


            # FILE HANDLING
            from pathlib import Path
            import json
        


        except ImportError as e:
            print(e)
    

    
    @classmethod
    def import_installer(cls):
        """This method will be responsible for installing dependencies"""


        choice = input("If you want to automatically install libaries type yes: ").strip().lower()

        if choice == "yes" or choice == "y" or choice == "1":
            print("Bet now downloading Dependencies")
            #time.sleep(1)
            

            # LOOP FOR EXCEPTIONS
            while True:

                try:

                    
                    
                    # IMPORT OS SO WE CAN INSTALL LIBARIES
                    import os
                    for key, value in cls.libaries.items():
                        print(f"Now trying to install: {value}   #{key}/12")
                        os.system(f"pip install {value}")

                    

                    # NOW IMPORT LIBARIES
                    from rich.console import Console
                    import time
                    console = Console()

                    # NOW PRINT SOME CODE
                    console.print("Dependencies now installed.", style="bold blue")
                    console.print("Now Restarting cmd instance", style="bold green")
                    time.sleep(3)


                    # NOW TO BRING BACK TO MAIN MENU 
                    #from nsm_ui import MainUI
                    # MainUI.main()
    

                except Exception as e:
                    print(f"Got a Exception error will, continue: {e}")
                        





